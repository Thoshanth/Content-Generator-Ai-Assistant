import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useChat } from '../context/ChatContext'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../components/chat/Sidebar'
import ChatWindow from '../components/chat/ChatWindow'
import InputBar from '../components/chat/InputBar'
import ContentTypeSelector from '../components/chat/ContentTypeSelector'
import ToneSelector from '../components/chat/ToneSelector'
import LengthSelector from '../components/chat/LengthSelector'
import LanguageSelector from '../components/chat/LanguageSelector'
import toast from 'react-hot-toast'
import { Settings } from 'lucide-react'

const ChatPage = () => {
  const [contentType, setContentType] = useState('general')
  const [tone, setTone] = useState('professional')
  const [length, setLength] = useState('auto')
  const [language, setLanguage] = useState('English')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const { user, isAuthenticated } = useAuth()
  const { loadSessions, sendMessage, currentSession, messages } = useChat()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated) {
      loadSessions()
    }
  }, [isAuthenticated])

  const handleSendMessage = async (prompt) => {
    if (!isAuthenticated) {
      toast.error('Please login to send messages')
      navigate('/login', { state: { from: '/chat' } })
      return
    }

    if (!prompt.trim()) {
      toast.error('Please enter a message')
      return
    }

    // Check daily limit
    if (user?.dailyMessageCount >= 10) {
      toast.error('Daily message limit reached (10/day)')
      return
    }

    try {
      // Send with all v5.0 parameters
      await sendMessage(prompt, contentType, false, {
        tone,
        length,
        language
      })
    } catch (error) {
      console.error('Send message error:', error)
      toast.error(error.response?.data?.error || error.message || 'Failed to send message')
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
            <div>
              <h1 className="text-xl md:text-2xl font-heading font-bold text-white">
                {currentSession ? currentSession.title || 'Chat Session' : 'New Chat'}
              </h1>
              <p className="text-xs md:text-sm font-body text-text-secondary">
                {isAuthenticated ? `${user?.dailyMessageCount || 0}/10 messages used today` : 'Login to save your conversations'}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="btn-icon flex items-center space-x-2 text-sm"
              >
                <Settings className="w-4 h-4" />
                <span className="hidden md:inline">{showAdvanced ? 'Hide' : 'Options'}</span>
              </button>
            </div>
          </div>

          {/* Content Type Selector - Always Visible */}
          <div className="flex items-center space-x-4">
            <ContentTypeSelector value={contentType} onChange={setContentType} />
          </div>

          {/* Advanced Options - Collapsible */}
          {showAdvanced && (
            <div className="mt-4 pt-4 border-t border-border">
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
            </div>
          )}
        </div>

        {/* Chat Window */}
        <ChatWindow messages={messages} />

        {/* Input Bar */}
        <InputBar onSend={handleSendMessage} contentType={contentType} />
      </div>
    </div>
  )
}

export default ChatPage
