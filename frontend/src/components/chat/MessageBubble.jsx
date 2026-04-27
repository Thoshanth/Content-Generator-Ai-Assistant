import { User, Bot, Copy, Check } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { useState } from 'react'
import toast from 'react-hot-toast'

const MessageBubble = ({ message }) => {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    toast.success('Copied to clipboard')
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex space-x-3 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary' : 'bg-gray-200'
        }`}>
          {isUser ? (
            <User className="w-6 h-6 text-white" />
          ) : (
            <Bot className="w-6 h-6 text-gray-600" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
          <div className={`inline-block px-4 py-3 rounded-lg ${
            isUser
              ? 'bg-primary text-white'
              : 'bg-white border border-border text-text-primary'
          }`}>
            {isUser ? (
              <p className="whitespace-pre-wrap">{message.content}</p>
            ) : (
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            )}
            
            {message.streaming && (
              <span className="inline-block w-2 h-4 bg-current animate-pulse ml-1"></span>
            )}
          </div>

          {/* Message Meta */}
          {!isUser && !message.streaming && (
            <div className="flex items-center space-x-2 mt-2 text-xs text-text-secondary">
              {message.modelUsed && (
                <span className="px-2 py-1 bg-gray-100 rounded">
                  {message.modelUsed.split('/')[1]?.split(':')[0] || 'AI'}
                </span>
              )}
              {message.tokensUsed && (
                <span>{message.tokensUsed} tokens</span>
              )}
              <button
                onClick={handleCopy}
                className="p-1 hover:bg-gray-100 rounded"
                title="Copy to clipboard"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-green-500" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
