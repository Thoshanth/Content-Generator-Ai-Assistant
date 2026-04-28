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
    <div className="bg-bg border-t border-border p-4 flex-shrink-0">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="flex space-x-4">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholders[contentType] || placeholders.general}
            className="flex-1 px-4 py-3 bg-surface-raised border border-white/10 rounded-xl text-white placeholder-text-secondary font-body focus:outline-none focus:border-peach/50 focus:shadow-[0_0_20px_rgba(249,168,168,0.15)] transition-all duration-300 resize-none custom-scrollbar"
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
            className="btn-primary self-end px-6 py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-[0_0_15px_rgba(249,168,168,0.2)] hover:shadow-[0_0_25px_rgba(249,168,168,0.4)] transition-all duration-300"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="text-xs font-body text-text-secondary mt-3 text-center">
          Press <span className="px-1 py-0.5 bg-surface-raised rounded text-white border border-border">Enter</span> to send, <span className="px-1 py-0.5 bg-surface-raised rounded text-white border border-border">Shift + Enter</span> for new line
        </p>
      </form>
    </div>
  )
}

export default InputBar
