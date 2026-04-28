import { User, Bot, Image as ImageIcon, Download } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import ProviderIndicator from './ProviderIndicator'
import ExportButtons from './ExportButtons'
import { motion } from 'framer-motion'

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user'
  const isImage = message.messageType === 'image'
  const isImageRequest = message.messageType === 'image_request'

  const handleImageDownload = () => {
    if (message.imageUrl) {
      const link = document.createElement('a')
      link.href = `http://localhost:8080${message.imageUrl}`
      link.download = `generated-image-${Date.now()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex space-x-3 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
          isUser ? 'bg-peach' : 'bg-surface-raised border border-white/10'
        }`}>
          {isUser ? (
            <User className="w-6 h-6 text-black" />
          ) : isImage ? (
            <ImageIcon className="w-6 h-6 text-peach" />
          ) : (
            <Bot className="w-6 h-6 text-peach" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
          <div className={`inline-block px-5 py-3.5 rounded-2xl shadow-md ${
            isUser
              ? 'bg-peach text-black rounded-tr-none'
              : 'bg-surface-raised border border-white/10 text-white rounded-tl-none'
          }`}>
            {isUser ? (
              <p className="whitespace-pre-wrap font-body text-sm md:text-base leading-relaxed">{message.content}</p>
            ) : isImage && message.imageUrl ? (
              // Generated Image Display
              <div className="space-y-3">
                <div className="relative group">
                  <img 
                    src={`http://localhost:8080${message.imageUrl}`}
                    alt={message.imagePrompt || "Generated image"}
                    className="max-w-full h-auto rounded-lg shadow-lg"
                    style={{ maxHeight: '400px' }}
                  />
                  <button
                    onClick={handleImageDownload}
                    className="absolute top-2 right-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                    title="Download image"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                </div>
                {message.imagePrompt && (
                  <p className="text-sm text-text-secondary italic">
                    "{message.imagePrompt}"
                  </p>
                )}
              </div>
            ) : (
              <div className="prose prose-sm prose-invert max-w-none font-body text-sm md:text-base leading-relaxed">
                {message.content ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : message.streaming && !message.content ? (
                   // Initial Skeleton Loader before streaming begins
                   <div className="flex items-center space-x-2 py-1">
                     <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0 }} className="w-2 h-2 rounded-full bg-peach" />
                     <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.2 }} className="w-2 h-2 rounded-full bg-peach" />
                     <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.4 }} className="w-2 h-2 rounded-full bg-peach" />
                   </div>
                ) : null}
              </div>
            )}
            
            {message.streaming && message.content && (
              <span className="inline-block w-2 h-4 bg-peach animate-blink ml-1 align-middle"></span>
            )}
          </div>

          {/* Message Meta - AI Messages Only */}
          {!isUser && !message.streaming && (message.content || isImage) && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-3 space-y-3 text-left"
            >
              {/* Provider Info */}
              <div className="flex items-center space-x-2 text-xs font-body">
                {isImage && message.imageModel ? (
                  <span className="text-text-secondary bg-surface-raised px-2 py-1 rounded-md border border-white/5">
                    {message.imageModel}
                  </span>
                ) : message.provider && (
                  <ProviderIndicator 
                    provider={message.provider} 
                    model={message.modelUsed} 
                  />
                )}
                {isImage && message.imageParameters?.generation_time && (
                  <span className="text-text-secondary bg-surface-raised px-2 py-1 rounded-md border border-white/5">
                    {message.imageParameters.generation_time}s
                  </span>
                )}
                {isImage && message.imageParameters?.width && message.imageParameters?.height && (
                  <span className="text-text-secondary bg-surface-raised px-2 py-1 rounded-md border border-white/5">
                    {message.imageParameters.width}×{message.imageParameters.height}
                  </span>
                )}
                {message.wordCount && (
                  <span className="text-text-secondary bg-surface-raised px-2 py-1 rounded-md border border-white/5">
                    {message.wordCount} words
                  </span>
                )}
                {message.tokensUsed && (
                  <span className="text-text-secondary bg-surface-raised px-2 py-1 rounded-md border border-white/5">
                    {message.tokensUsed} tokens
                  </span>
                )}
              </div>

              {/* Export Buttons - Only for text content */}
              {!isImage && (
                <ExportButtons 
                  content={message.content} 
                  contentType={message.contentType || 'general'} 
                />
              )}
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

export default MessageBubble
