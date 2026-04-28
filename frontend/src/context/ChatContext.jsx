import { createContext, useContext, useState } from 'react'
import { chatService } from '../services/chatService'

const ChatContext = createContext(null)

export const ChatProvider = ({ children }) => {
  const [sessions, setSessions] = useState([])
  const [currentSession, setCurrentSession] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const loadSessions = async () => {
    try {
      setLoading(true)
      const data = await chatService.getSessions()
      if (Array.isArray(data)) {
        setSessions(data)
      } else {
        console.error('Expected array of sessions, received:', data)
        setSessions([])
      }
    } catch (error) {
      console.error('Failed to load sessions:', error)
      setSessions([])
    } finally {
      setLoading(false)
    }
  }

  const loadSession = async (sessionId) => {
    try {
      setLoading(true)
      const data = await chatService.getSession(sessionId)
      setCurrentSession(data)
      setMessages(data.messages || [])
    } catch (error) {
      console.error('Failed to load session:', error)
    } finally {
      setLoading(false)
    }
  }

  const createNewSession = async (title, contentType) => {
    try {
      const session = await chatService.createSession(title, contentType)
      setSessions((prev) => [session, ...prev])
      setCurrentSession(session)
      setMessages([])
      return session
    } catch (error) {
      console.error('Failed to create session:', error)
      throw error
    }
  }

  const sendMessage = async (prompt, contentType, useStreaming = false, options = {}) => {
    const { tone = 'professional', length = 'auto', language = 'English' } = options

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: prompt,
      createdAt: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])

    try {
      if (useStreaming) {
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: '',
          createdAt: new Date().toISOString(),
          streaming: true,
        }

        setMessages((prev) => [...prev, assistantMessage])

        await chatService.sendMessageStream(
          prompt,
          contentType,
          currentSession?.id,
          tone,
          length,
          language,
          (chunk) => {
            // Handle different chunk formats
            if (chunk.chunk) {
              // Handle chunk format from AI service
              setMessages((prev) => {
                const newMessages = [...prev]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage.streaming) {
                  lastMessage.content += chunk.chunk
                }
                return newMessages
              })
            } else if (chunk.content) {
              // Handle content format
              setMessages((prev) => {
                const newMessages = [...prev]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage.streaming) {
                  lastMessage.content += chunk.content
                }
                return newMessages
              })
            } else if (chunk.done) {
              // Handle completion
              setMessages((prev) => {
                const newMessages = [...prev]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage.streaming) {
                  delete lastMessage.streaming
                }
                return newMessages
              })
            }
          }
        )

        // Ensure streaming flag is removed
        setMessages((prev) => {
          const newMessages = [...prev]
          const lastMessage = newMessages[newMessages.length - 1]
          if (lastMessage.streaming) {
            delete lastMessage.streaming
          }
          return newMessages
        })
      } else {
        const response = await chatService.sendMessage(
          prompt,
          contentType,
          currentSession?.id,
          tone,
          length,
          language
        )

        const assistantMessage = {
          id: response.messageId,
          role: 'assistant',
          content: response.content,
          modelUsed: response.modelUsed,
          tokensUsed: response.tokensUsed,
          provider: response.provider,
          wordCount: response.wordCount,
          charCount: response.charCount,
          contentType: contentType,
          createdAt: new Date().toISOString(),
        }

        setMessages((prev) => [...prev, assistantMessage])

        if (!currentSession) {
          setCurrentSession({ id: response.sessionId })
        }
      }

      await loadSessions()
    } catch (error) {
      console.error('Failed to send message:', error)
      
      // Remove the user message if sending failed
      setMessages((prev) => prev.filter(msg => msg.id !== userMessage.id))
      
      throw error
    }
  }

  const deleteSession = async (sessionId) => {
    try {
      await chatService.deleteSession(sessionId)
      setSessions((prev) => prev.filter((s) => s.id !== sessionId))
      if (currentSession?.id === sessionId) {
        setCurrentSession(null)
        setMessages([])
      }
    } catch (error) {
      console.error('Failed to delete session:', error)
      throw error
    }
  }

  const deleteAllSessions = async () => {
    try {
      await chatService.deleteAllSessions()
      setSessions([])
      setCurrentSession(null)
      setMessages([])
    } catch (error) {
      console.error('Failed to delete all sessions:', error)
      throw error
    }
  }

  const clearCurrentSession = () => {
    setCurrentSession(null)
    setMessages([])
  }

  const value = {
    sessions,
    currentSession,
    messages,
    loading,
    loadSessions,
    loadSession,
    createNewSession,
    sendMessage,
    deleteSession,
    deleteAllSessions,
    clearCurrentSession,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

export const useChat = () => {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within ChatProvider')
  }
  return context
}
