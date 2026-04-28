import { useState, useEffect, useCallback } from 'react'
import { getFollowUpQuestions } from '../services/api'

/**
 * Custom hook for managing follow-up questions state
 * @param {string} contentType - Current content type
 * @param {Array} messages - Chat messages array
 * @param {string} userId - User ID
 * @returns {Object} Hook state and methods
 */
export const useFollowUpQuestions = (contentType, messages, userId = '') => {
  const [questions, setQuestions] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showQuestions, setShowQuestions] = useState(false)

  // Determine if we should show follow-up questions
  const shouldShowQuestions = useCallback(() => {
    // Don't show for general content type
    if (contentType === 'general') return false
    
    // Show if chat is empty
    if (messages.length === 0) return true
    
    // Show if only one user message exists (no AI response yet)
    if (messages.length === 1 && messages[0].role === 'user') return true
    
    // Don't show during active conversation
    return false
  }, [contentType, messages])

  // Load follow-up questions
  const loadQuestions = useCallback(async (initialPrompt = '') => {
    if (!shouldShowQuestions()) {
      setShowQuestions(false)
      setQuestions([])
      return
    }

    try {
      setIsLoading(true)
      setError(null)
      
      const response = await getFollowUpQuestions(
        contentType,
        initialPrompt,
        userId
      )
      
      setQuestions(response.questions || [])
      setShowQuestions(true)
    } catch (err) {
      console.error('Failed to load follow-up questions:', err)
      setError(err.message)
      // Silently fail - questions are optional
      setQuestions([])
      setShowQuestions(false)
    } finally {
      setIsLoading(false)
    }
  }, [contentType, userId, shouldShowQuestions])

  // Auto-load questions when conditions change
  useEffect(() => {
    if (shouldShowQuestions()) {
      // Get the last user message as context
      const lastUserMessage = messages.length > 0 && messages[messages.length - 1].role === 'user'
        ? messages[messages.length - 1].content
        : ''
      
      loadQuestions(lastUserMessage)
    } else {
      setShowQuestions(false)
      setQuestions([])
    }
  }, [contentType, messages.length, loadQuestions])

  // Hide questions (called when user sends a message)
  const hideQuestions = useCallback(() => {
    setShowQuestions(false)
  }, [])

  // Refresh questions manually
  const refreshQuestions = useCallback((initialPrompt = '') => {
    loadQuestions(initialPrompt)
  }, [loadQuestions])

  return {
    // State
    questions,
    isLoading,
    error,
    showQuestions,
    
    // Methods
    hideQuestions,
    refreshQuestions,
    
    // Computed
    hasQuestions: questions.length > 0,
    shouldShow: showQuestions && questions.length > 0,
  }
}

export default useFollowUpQuestions