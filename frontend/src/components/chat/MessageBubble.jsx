import { User, Bot } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import ProviderIndicator from './ProviderIndicator'
import ExportButtons from './ExportButtons'

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user'

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

          {/* Message Meta - AI Messages Only */}
          {!isUser && !message.streaming && (
            <div className="mt-2 space-y-2">
              {/* Provider Info */}
              <div className="flex items-center space-x-2 text-xs">
                {message.provider && (
                  <ProviderIndicator 
                    provider={message.provider} 
                    model={message.modelUsed} 
                  />
                )}
                {message.wordCount && (
                  <span className="text-text-secondary">
                    {message.wordCount} words
                  </span>
                )}
                {message.tokensUsed && (
                  <span className="text-text-secondary">
                    • {message.tokensUsed} tokens
                  </span>
                )}
              </div>

              {/* Export Buttons */}
              <ExportButtons 
                content={message.content} 
                contentType={message.contentType || 'general'} 
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
