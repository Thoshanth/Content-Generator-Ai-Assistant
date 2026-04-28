import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, Sparkles, ChevronRight } from 'lucide-react'

const FollowUpQuestions = ({ questions, onQuestionClick, isLoading }) => {
  // Show loading skeleton while questions are being generated
  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="px-6 pb-4"
      >
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center gap-2 mb-3">
            <div className="flex items-center justify-center w-6 h-6 bg-peach/20 rounded-full">
              <Sparkles className="w-3.5 h-3.5 text-peach" />
            </div>
            <span className="text-sm font-medium text-text-secondary font-body">
              Generating personalized questions...
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {[...Array(6)].map((_, index) => (
              <div
                key={index}
                className="bg-surface-raised border border-white/10 rounded-xl p-3.5 animate-pulse"
              >
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 bg-peach/10 rounded-full flex-shrink-0 mt-0.5" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 bg-white/10 rounded w-3/4" />
                    <div className="h-4 bg-white/10 rounded w-1/2" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    )
  }

  if (!questions || questions.length === 0) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="px-6 pb-4"
    >
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="flex items-center gap-2 mb-3"
        >
          <div className="flex items-center justify-center w-6 h-6 bg-peach/20 rounded-full">
            <Sparkles className="w-3.5 h-3.5 text-peach" />
          </div>
          <span className="text-sm font-medium text-text-secondary font-body">
            Suggested questions to help me understand better
          </span>
        </motion.div>

        {/* Questions Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <AnimatePresence>
            {questions.map((question, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, scale: 0.95, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ 
                  delay: index * 0.05,
                  duration: 0.3,
                  ease: "easeOut"
                }}
                whileHover={{ 
                  scale: 1.02,
                  boxShadow: "0 0 20px rgba(249, 168, 168, 0.2)"
                }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onQuestionClick(question)}
                disabled={isLoading}
                className="group relative bg-surface-raised border border-white/10 rounded-xl p-3.5 text-left transition-all duration-300 hover:border-peach/50 hover:bg-surface-raised/80 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
              >
                {/* Gradient overlay on hover */}
                <div className="absolute inset-0 bg-gradient-to-r from-peach/0 via-peach/5 to-peach/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                {/* Content */}
                <div className="relative flex items-start gap-3">
                  <div className="flex-shrink-0 mt-0.5">
                    <div className="flex items-center justify-center w-5 h-5 bg-peach/10 rounded-full group-hover:bg-peach/20 transition-colors">
                      <MessageCircle className="w-3 h-3 text-peach" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-body text-white leading-relaxed group-hover:text-peach transition-colors">
                      {question}
                    </p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-text-muted group-hover:text-peach transition-all group-hover:translate-x-1 flex-shrink-0 mt-0.5" />
                </div>

                {/* Bottom shine effect */}
                <motion.div
                  className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-peach/50 to-transparent opacity-0 group-hover:opacity-100"
                  initial={{ scaleX: 0 }}
                  whileHover={{ scaleX: 1 }}
                  transition={{ duration: 0.3 }}
                />
              </motion.button>
            ))}
          </AnimatePresence>
        </div>

        {/* Helper text */}
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-xs text-text-muted text-center mt-3 font-body"
        >
          Click a question to answer it, or type your own message below
        </motion.p>
      </div>
    </motion.div>
  )
}

export default FollowUpQuestions
