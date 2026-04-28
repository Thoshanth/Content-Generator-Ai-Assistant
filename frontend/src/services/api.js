import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api'
const AI_SERVICE_URL = import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// AI Service API client (no auth needed for AI service)
const aiApi = axios.create({
  baseURL: AI_SERVICE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Flag to prevent multiple refresh attempts
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  
  failedQueue = []
}

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If already refreshing, queue the request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }).catch(err => {
          return Promise.reject(err)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (!refreshToken) {
          throw new Error('No refresh token')
        }

        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refreshToken: refreshToken
        })

        const { accessToken, refreshToken: newRefreshToken } = response.data
        
        localStorage.setItem('accessToken', accessToken)
        localStorage.setItem('refreshToken', newRefreshToken)
        
        // Update default authorization header
        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
        
        processQueue(null, accessToken)
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${accessToken}`
        return api(originalRequest)
        
      } catch (refreshError) {
        processQueue(refreshError, null)
        
        // Refresh failed, logout user
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
        
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

// ── AI Service API Methods ──────────────────────────────────────────────────

/**
 * Stream AI response for content generation (Direct to AI Service)
 * @param {Object} request - Chat request object
 * @returns {EventSource} - SSE event source for streaming
 */
export function streamAiResponse(request) {
  const params = new URLSearchParams()
  params.append('prompt', request.prompt)
  params.append('content_type', request.content_type || 'general')
  params.append('tone', request.tone || 'professional')
  params.append('length', request.length || 'auto')
  params.append('language', request.language || 'English')
  params.append('regenerate', request.regenerate || false)
  
  if (request.user_id) params.append('user_id', request.user_id)
  if (request.custom_instructions) params.append('custom_instructions', request.custom_instructions)
  if (request.uploaded_text) params.append('uploaded_text', request.uploaded_text)

  return new EventSource(`${AI_SERVICE_URL}/chat/stream?${params}`)
}

/**
 * Generate content using convenience endpoints
 * @param {string} contentType - Type of content (email, blog_post, resume, etc.)
 * @param {Object} request - Generation request
 * @returns {Promise} - Generated content
 */
export async function generateContent(contentType, request) {
  const response = await aiApi.post(`/generate/${contentType}`, request)
  return response.data
}

/**
 * Export content to different formats
 * @param {string} content - Content to export
 * @param {string} format - Export format (plain_text, html, markdown)
 * @param {string} contentType - Type of content
 * @returns {Promise} - Export response with converted content
 */
export async function exportContent(content, format, contentType) {
  const response = await aiApi.post('/tools/export', {
    content,
    format,
    content_type: contentType
  })
  return response.data
}

/**
 * Export content as PDF
 * @param {string} content - Content to export
 * @param {string} contentType - Type of content (resume, cover_letter)
 * @param {string} candidateName - Name for PDF filename
 * @returns {Promise<Blob>} - PDF blob for download
 */
export async function exportPdf(content, contentType, candidateName = 'document') {
  const response = await aiApi.post('/tools/export-pdf', {
    content,
    content_type: contentType,
    candidate_name: candidateName
  }, {
    responseType: 'blob'
  })
  return response.data
}

/**
 * Get available AI providers
 * @returns {Promise} - List of available providers
 */
export async function getAiProviders() {
  const response = await aiApi.get('/chat/providers')
  return response.data
}

/**
 * Check if bot should ask follow-up questions
 * @param {string} contentType - Type of content
 * @param {string} userMessage - User's message
 * @param {Array} conversationHistory - Previous messages
 * @param {string} userId - User ID (optional)
 * @returns {Promise} - Object with should_ask boolean and reason
 */
export async function checkShouldAskFollowUp(contentType, userMessage, conversationHistory = [], userId = '') {
  const response = await aiApi.post('/followup/check', {
    content_type: contentType,
    user_message: userMessage,
    conversation_history: conversationHistory,
    user_id: userId
  })
  return response.data
}

/**
 * Generate bot follow-up questions message
 * @param {string} contentType - Type of content
 * @param {string} userMessage - User's message
 * @param {Array} conversationHistory - Previous messages
 * @param {string} userId - User ID (optional)
 * @returns {Promise} - Object with message, content_type, and has_questions
 */
export async function generateBotFollowUp(contentType, userMessage, conversationHistory = [], userId = '') {
  const response = await aiApi.post('/followup/generate', {
    content_type: contentType,
    user_message: userMessage,
    conversation_history: conversationHistory,
    user_id: userId
  })
  return response.data
}

// ── Backend API Methods (Through Java Backend) ──────────────────────────────

/**
 * Send chat message to backend (with auth and database storage)
 * @param {Object} request - Chat request
 * @returns {Promise} - Chat response
 */
export async function sendChatMessage(request) {
  const response = await api.post('/chat/message', {
    prompt: request.prompt,
    contentType: request.contentType || 'general',
    sessionId: request.sessionId,
    sessionTitle: request.sessionTitle,
    tone: request.tone || 'professional',
    length: request.length || 'auto',
    language: request.language || 'English',
    regenerate: request.regenerate || false,
    customInstructions: request.customInstructions,
    uploadedText: request.uploadedText
  })
  return response.data
}

/**
 * Send chat message with streaming (through backend)
 * @param {Object} request - Chat request
 * @param {Function} onMessage - Callback for each message chunk
 * @param {Function} onError - Callback for errors
 * @param {Function} onComplete - Callback when stream completes
 */
export async function sendChatMessageStream(request, onMessage, onError, onComplete) {
  try {
    const token = localStorage.getItem('accessToken')
    const response = await fetch(`${API_BASE_URL}/chat/message/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        prompt: request.prompt,
        contentType: request.contentType || 'general',
        sessionId: request.sessionId,
        sessionTitle: request.sessionTitle,
        tone: request.tone || 'professional',
        length: request.length || 'auto',
        language: request.language || 'English',
        regenerate: request.regenerate || false,
        customInstructions: request.customInstructions,
        uploadedText: request.uploadedText
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        if (onComplete) onComplete()
        break
      }

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.substring(6))
            if (onMessage) onMessage(data)
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  } catch (error) {
    if (onError) onError(error)
  }
}

/**
 * Get all chat sessions for user
 * @returns {Promise} - List of chat sessions
 */
export async function getChatSessions() {
  const response = await api.get('/chat/sessions')
  return response.data
}

/**
 * Get specific chat session with messages
 * @param {string} sessionId - Session ID
 * @returns {Promise} - Session with messages
 */
export async function getChatSession(sessionId) {
  const response = await api.get(`/chat/sessions/${sessionId}`)
  return response.data
}

/**
 * Create new chat session
 * @param {string} title - Session title
 * @param {string} contentType - Content type
 * @returns {Promise} - Created session
 */
export async function createChatSession(title, contentType = 'general') {
  const response = await api.post('/chat/sessions', { title, contentType })
  return response.data
}

/**
 * Delete chat session
 * @param {string} sessionId - Session ID
 * @returns {Promise} - Success message
 */
export async function deleteChatSession(sessionId) {
  const response = await api.delete(`/chat/sessions/${sessionId}`)
  return response.data
}

/**
 * Delete all chat sessions
 * @returns {Promise} - Success message
 */
export async function deleteAllChatSessions() {
  const response = await api.delete('/chat/sessions')
  return response.data
}

// ── Content Type Constants ──────────────────────────────────────────────────

export const CONTENT_TYPES = {
  GENERAL: 'general',
  BLOG_POST: 'blog_post',
  EMAIL: 'email',
  SOCIAL_MEDIA: 'social_media',
  AD_COPY: 'ad_copy',
  TWEET_THREAD: 'tweet_thread',
  RESUME: 'resume',
  COVER_LETTER: 'cover_letter',
  YOUTUBE_SCRIPT: 'youtube_script',
  PRODUCT_DESC: 'product_desc',
  ESSAY: 'essay',
  CODE_EXPLAINER: 'code_explainer'
}

export const TONES = {
  PROFESSIONAL: 'professional',
  CASUAL: 'casual',
  FORMAL: 'formal',
  PERSUASIVE: 'persuasive',
  FRIENDLY: 'friendly',
  WITTY: 'witty',
  EMPATHETIC: 'empathetic'
}

export const LENGTHS = {
  SHORT: 'short',
  MEDIUM: 'medium',
  LONG: 'long',
  AUTO: 'auto'
}

export const LANGUAGES = {
  ENGLISH: 'English',
  HINDI: 'Hindi',
  TELUGU: 'Telugu',
  SPANISH: 'Spanish',
  FRENCH: 'French',
  GERMAN: 'German',
  PORTUGUESE: 'Portuguese',
  ARABIC: 'Arabic',
  JAPANESE: 'Japanese',
  CHINESE: 'Chinese (Simplified)',
  KOREAN: 'Korean'
}

export const EXPORT_FORMATS = {
  PLAIN_TEXT: 'plain_text',
  HTML: 'html',
  MARKDOWN: 'markdown'
}

export default api
