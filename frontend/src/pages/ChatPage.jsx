import { useState, useEffect } from 'react'
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
  const { user } = useAuth()
  const { loadSessions, sendMessage, currentSession, messages } = useChat()

  useEffect(() => {
    loadSessions()
  }, [])

  const handleSendMessage = async (prompt) => {
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
      toast.success('Message sent!')
    } catch (error) {
      console.error('Send message error:', error)
      toast.error(error.response?.data?.error || error.message || 'Failed to send message')
    }
  }

  return (
    <div className="flex h-screen bg-surface">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-border px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-2xl font-bold text-text-primary">AI Content Generator</h1>
              <p className="text-sm text-text-secondary">
                {user?.dailyMessageCount || 0}/10 messages used today
              </p>
            </div>
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="inline-flex items-center space-x-2 px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <Settings className="w-4 h-4" />
              <span>{showAdvanced ? 'Hide' : 'Show'} Options</span>
            </button>
          </div>

          {/* Content Type Selector - Always Visible */}
          <div className="flex items-center space-x-4">
            <ContentTypeSelector value={contentType} onChange={setContentType} />
          </div>

          {/* Advanced Options - Collapsible */}
          {showAdvanced && (
            <div className="mt-3 pt-3 border-t border-border">
              <div className="flex flex-wrap items-center gap-4">
                <ToneSelector value={tone} onChange={setTone} />
                <LengthSelector value={length} onChange={setLength} />
                <LanguageSelector value={language} onChange={setLanguage} />
              </div>
              <div className="mt-2 text-xs text-text-secondary">
                <p>
                  <strong>Tone:</strong> {tone} • 
                  <strong> Length:</strong> {length} • 
                  <strong> Language:</strong> {language}
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
