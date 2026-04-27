import { useState } from 'react'
import { Send } from 'lucide-react'

const InputBar = ({ onSend, contentType }) => {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSend(input)
      setInput('')
    }
  }

  const placeholders = {
    blog_post: 'Write a blog post about...',
    email: 'Write an email about...',
    social_media: 'Create a social media post about...',
    ad_copy: 'Write ad copy for...',
    general: 'Ask me anything...',
  }

  return (
    <div className="bg-white border-t border-border p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="flex space-x-4">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholders[contentType] || placeholders.general}
            className="flex-1 px-4 py-3 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            rows="3"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
          />
          <button
            type="submit"
            disabled={!input.trim()}
            className="btn-primary self-end px-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="text-xs text-text-secondary mt-2 text-center">
          Press Enter to send, Shift+Enter for new line
        </p>
      </form>
    </div>
  )
}

export default InputBar
