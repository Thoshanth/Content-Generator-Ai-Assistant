import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import { Bot, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

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
      <div className="flex-1 flex items-center justify-center p-8 overflow-y-auto custom-scrollbar">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-md"
        >
          <motion.div 
            animate={{ 
              y: [0, -10, 0],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ 
              repeat: Infinity, 
              duration: 4,
              ease: "easeInOut"
            }}
            className="inline-flex items-center justify-center w-20 h-20 bg-peach-subtle rounded-full mb-6 relative"
          >
            <Bot className="w-10 h-10 text-peach" />
            <motion.div
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [0.5, 0.8, 0.5]
              }}
              transition={{ 
                repeat: Infinity, 
                duration: 2
              }}
              className="absolute inset-0 rounded-full bg-peach/20"
            />
          </motion.div>
          <motion.h2 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-2xl font-heading font-bold text-white mb-4"
          >
            Welcome to Creo
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-text-secondary font-body flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4 text-peach" />
            Choose a content type and start generating amazing content with AI
          </motion.p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
      {messages.map((message, index) => (
        <motion.div
          key={message.id || index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
        >
          <MessageBubble message={message} />
        </motion.div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatWindow
