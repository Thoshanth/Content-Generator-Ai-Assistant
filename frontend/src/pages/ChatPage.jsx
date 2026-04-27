import { useState, useEffect } from 'react'
import { useChat } from '../context/ChatContext'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../components/chat/Sidebar'
import ChatWindow from '../components/chat/ChatWindow'
import InputBar from '../components/chat/InputBar'
import ContentTypeSelector from '../components/chat/ContentTypeSelector'
import toast from 'react-hot-toast'

const ChatPage = () => {
  const [contentType, setContentType] = useState('general')
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
      await sendMessage(prompt, contentType, false) // Use non-streaming for now
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-text-primary">AI Content Generator</h1>
              <p className="text-sm text-text-secondary">
                {user?.dailyMessageCount || 0}/10 messages used today
              </p>
            </div>
            <ContentTypeSelector value={contentType} onChange={setContentType} />
          </div>
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
