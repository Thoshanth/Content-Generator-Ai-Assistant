import api from './api'

export const chatService = {
  async sendMessage(prompt, contentType, sessionId = null, tone = 'professional', length = 'auto', language = 'English', sessionTitle = null) {
    const response = await api.post('/chat/message', {
      prompt,
      contentType,
      sessionId,
      sessionTitle,
      tone,
      length,
      language,
    })
    return response.data
  },

  async sendMessageStream(prompt, contentType, sessionId = null, tone = 'professional', length = 'auto', language = 'English', onChunk) {
    const token = localStorage.getItem('accessToken')
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api'
    
    const response = await fetch(`${API_BASE_URL}/chat/message/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        prompt,
        contentType,
        sessionId,
        tone,
        length,
        language,
      }),
    })

    if (!response.ok) {
      throw new Error('Stream request failed')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data.trim()) {
            try {
              const parsed = JSON.parse(data)
              onChunk(parsed)
            } catch (e) {
              console.error('Failed to parse SSE data:', e)
            }
          }
        }
      }
    }
  },

  async getSessions() {
    const response = await api.get('/chat/sessions')
    return response.data
  },

  async getSession(sessionId) {
    const response = await api.get(`/chat/sessions/${sessionId}`)
    return response.data
  },

  async createSession(title, contentType) {
    const response = await api.post('/chat/sessions', { title, contentType })
    return response.data
  },

  async deleteSession(sessionId) {
    const response = await api.delete(`/chat/sessions/${sessionId}`)
    return response.data
  },

  async deleteAllSessions() {
    const response = await api.delete('/chat/sessions')
    return response.data
  },
}
