import { useState } from 'react'
import { Send, Sparkles, Image as ImageIcon } from 'lucide-react'
import { motion } from 'framer-motion'

const InputBar = ({ onSend, onImageGenerate, contentType }) => {
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
          <motion.textarea
            whileFocus={{ scale: 1.01 }}
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
          <div className="flex flex-col space-y-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="button"
              onClick={onImageGenerate}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-xl transition-all duration-300 flex items-center justify-center space-x-2 shadow-[0_0_15px_rgba(147,51,234,0.2)] hover:shadow-[0_0_25px_rgba(147,51,234,0.4)]"
              title="Generate Image"
            >
              <ImageIcon className="w-5 h-5" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={!input.trim()}
              className="btn-primary px-6 py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 shadow-[0_0_15px_rgba(249,168,168,0.2)] hover:shadow-[0_0_25px_rgba(249,168,168,0.4)] transition-all duration-300 relative overflow-hidden group"
            >
              <motion.div
                animate={{ rotate: input.trim() ? [0, 360] : 0 }}
                transition={{ duration: 2, repeat: input.trim() ? Infinity : 0, ease: "linear" }}
                className="absolute inset-0 bg-gradient-to-r from-peach/0 via-peach/20 to-peach/0 group-hover:opacity-100 opacity-0 transition-opacity"
              />
              <Send className="w-5 h-5 relative z-10" />
            </motion.button>
          </div>
        </div>
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xs font-body text-text-secondary mt-3 text-center flex items-center justify-center gap-2"
        >
          <Sparkles className="w-3 h-3 text-peach" />
          Press <span className="px-1 py-0.5 bg-surface-raised rounded text-white border border-border">Enter</span> to send, <span className="px-1 py-0.5 bg-surface-raised rounded text-white border border-border">Shift + Enter</span> for new line
          <span className="mx-2">•</span>
          <ImageIcon className="w-3 h-3 text-purple-400" />
          Click image button to generate AI images
        </motion.p>
      </form>
    </div>
  )
}

export default InputBar
