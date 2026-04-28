import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useChat } from '../context/ChatContext'
import { useAuth } from '../context/AuthContext'
import { useNotifications } from '../hooks/useNotifications'
import Sidebar from '../components/chat/Sidebar'
import ChatWindow from '../components/chat/ChatWindow'
import InputBar from '../components/chat/InputBar'
import ImageGenerator from '../components/chat/ImageGenerator'
import ContentTypeSelector from '../components/chat/ContentTypeSelector'
import ToneSelector from '../components/chat/ToneSelector'
import LengthSelector from '../components/chat/LengthSelector'
import LanguageSelector from '../components/chat/LanguageSelector'
import DailyResetIndicator from '../components/chat/DailyResetIndicator'
import NotificationDemo from '../components/ui/NotificationDemo'
import toast from 'react-hot-toast'
import { Settings, Sparkles, Bell } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const ChatPage = () => {
  const [contentType, setContentType] = useState('general')
  const [tone, setTone] = useState('professional')
  const [length, setLength] = useState('auto')
  const [language, setLanguage] = useState('English')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showImageGenerator, setShowImageGenerator] = useState(false)
  const [showNotificationDemo, setShowNotificationDemo] = useState(false)
  const [isGeneratingImage, setIsGeneratingImage] = useState(false)
  const { user, isAuthenticated } = useAuth()
  const { loadSessions, sendMessage, currentSession, messages, addMessage } = useChat()
  const { 
    notifyError, 
    notifySuccess, 
    notifyWarning, 
    notifyImageGenerated, 
    notifyImageGenerationError,
    notifyValidationError,
    notifyAuthError
  } = useNotifications()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated) {
      console.log('ChatPage: Loading sessions for authenticated user')
      loadSessions().catch(err => {
        console.error('ChatPage: Failed to load sessions:', err)
        notifyError('Failed to load chat history', 'Connection Error')
      })
    }
  }, [isAuthenticated, loadSessions])

  const handleSendMessage = async (prompt) => {
    if (!isAuthenticated) {
      notifyAuthError()
      navigate('/login', { state: { from: '/chat' } })
      return
    }

    if (!prompt.trim()) {
      notifyValidationError('Please enter a message')
      return
    }

    // Check daily limit
    if (user?.dailyMessageCount >= 10) {
      notifyWarning('Daily message limit reached (10/day)', 'Limit Reached')
      return
    }

    try {
      // Send with all v5.0 parameters
      // The AI service will automatically check if follow-up questions should be asked
      await sendMessage(prompt, contentType, false, {
        tone,
        length,
        language
      })
    } catch (error) {
      console.error('Send message error:', error)
      notifyError(error.response?.data?.error || error.message || 'Failed to send message', 'Message Error')
    }
  }

  const handleImageGenerate = async (imageRequest) => {
    if (!isAuthenticated) {
      notifyAuthError()
      navigate('/login', { state: { from: '/chat' } })
      return
    }

    setIsGeneratingImage(true)
    
    try {
      // Add user message for image request
      const userMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: `Generate image: ${imageRequest.prompt}`,
        messageType: 'image_request',
        createdAt: new Date().toISOString()
      }
      addMessage(userMessage)

      // Call backend API
      const response = await fetch('http://localhost:8080/api/images/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: JSON.stringify(imageRequest)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Failed to generate image')
      }

      const imageResponse = await response.json()

      // Add assistant message with generated image
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Generated image',
        messageType: 'image',
        imageUrl: imageResponse.imageUrl,
        imagePrompt: imageResponse.prompt,
        imageModel: imageResponse.modelUsed,
        imageParameters: {
          ...imageResponse.parameters,
          generation_time: imageResponse.generationTime
        },
        createdAt: new Date().toISOString()
      }
      addMessage(assistantMessage)

      notifyImageGenerated()
      setShowImageGenerator(false)

    } catch (error) {
      console.error('Image generation error:', error)
      notifyImageGenerationError(error.message || 'Failed to generate image')
    } finally {
      setIsGeneratingImage(false)
    }
  }

  return (
    <div className="flex h-screen bg-bg overflow-hidden">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative w-full">
        {/* Header */}
        <div className="bg-bg border-b border-border px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <div className="flex-1">
              <motion.h1 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-xl md:text-2xl font-heading font-bold text-white flex items-center gap-2"
              >
                <Sparkles className="w-6 h-6 text-peach" />
                {currentSession ? currentSession.title || 'Creo Chat' : 'Creo'}
              </motion.h1>
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="text-xs md:text-sm font-body text-text-secondary"
              >
                {isAuthenticated ? 'AI-powered content generation and image creation at your fingertips' : 'Login to save your conversations'}
              </motion.p>
            </div>
            <div className="flex items-center space-x-3">
              {isAuthenticated && (
                <DailyResetIndicator 
                  dailyMessageCount={user?.dailyMessageCount || 0} 
                  maxMessages={10} 
                />
              )}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowNotificationDemo(true)}
                className="btn-icon flex items-center space-x-2 text-sm"
              >
                <Bell className="w-4 h-4" />
                <span className="hidden md:inline">Notifications</span>
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05, rotate: 90 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="btn-icon flex items-center space-x-2 text-sm"
              >
                <Settings className="w-4 h-4" />
                <span className="hidden md:inline">{showAdvanced ? 'Hide' : 'Options'}</span>
              </motion.button>
            </div>
          </div>

          {/* Content Type Selector - Always Visible */}
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex items-center space-x-4"
          >
            <ContentTypeSelector value={contentType} onChange={setContentType} />
          </motion.div>

          {/* Advanced Options - Collapsible */}
          {showAdvanced && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="mt-4 pt-4 border-t border-border"
            >
              <div className="flex flex-wrap items-center gap-4">
                <ToneSelector value={tone} onChange={setTone} />
                <LengthSelector value={length} onChange={setLength} />
                <LanguageSelector value={language} onChange={setLanguage} />
              </div>
              <div className="mt-3 text-xs font-body text-text-muted">
                <p>
                  <strong>Tone:</strong> <span className="text-peach">{tone}</span> &bull; 
                  <strong> Length:</strong> <span className="text-peach">{length}</span> &bull; 
                  <strong> Language:</strong> <span className="text-peach">{language}</span>
                </p>
              </div>
            </motion.div>
          )}
        </div>

        {/* Chat Window */}
        <ChatWindow messages={messages} />

        {/* Input Bar */}
        <InputBar 
          onSend={handleSendMessage} 
          onImageGenerate={() => setShowImageGenerator(true)}
          contentType={contentType} 
        />
      </div>

      {/* Image Generator Modal */}
      <AnimatePresence>
        {showImageGenerator && (
          <ImageGenerator
            onGenerate={handleImageGenerate}
            onClose={() => setShowImageGenerator(false)}
            isGenerating={isGeneratingImage}
          />
        )}
      </AnimatePresence>

      {/* Notification Demo Modal */}
      <AnimatePresence>
        {showNotificationDemo && (
          <NotificationDemo
            onClose={() => setShowNotificationDemo(false)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

export default ChatPage
