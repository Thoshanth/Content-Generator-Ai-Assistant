import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import { Bot } from 'lucide-react'

const ChatWindow = ({ messages }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-light rounded-full mb-6">
            <Bot className="w-10 h-10 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            Start a Conversation
          </h2>
          <p className="text-text-secondary">
            Choose a content type and start generating amazing content with AI
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {messages.map((message, index) => (
        <MessageBubble key={message.id || index} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatWindow
