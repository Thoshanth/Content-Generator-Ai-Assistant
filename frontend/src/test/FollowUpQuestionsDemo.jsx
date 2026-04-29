import { useState } from 'react'
import FollowUpQuestions from './FollowUpQuestions'
import { motion } from 'framer-motion'

/**
 * Demo component to showcase follow-up questions
 * This can be used for testing or as a standalone demo page
 */
const FollowUpQuestionsDemo = () => {
  const [selectedQuestion, setSelectedQuestion] = useState(null)

  const demoQuestions = {
    resume: [
      "What is your full name?",
      "What is your email address and phone number?",
      "What is your current education level and institution?",
      "What are your top 3-5 technical skills or areas of expertise?",
      "Describe your most recent work experience or internship",
      "What are 2-3 significant projects you've worked on?"
    ],
    cover_letter: [
      "What is the company name and position you're applying for?",
      "What specific skills or experiences make you a good fit for this role?",
      "Why are you interested in this company?",
      "What is a key achievement that demonstrates your qualifications?",
      "When are you available to start?"
    ],
    blog_post: [
      "What is the main topic or title of your blog post?",
      "Who is your target audience?",
      "What are the key points you want to cover?",
      "What tone would you like (professional, casual, technical, etc.)?",
      "Do you have any specific examples or data to include?"
    ]
  }

  const [currentType, setCurrentType] = useState('resume')

  const handleQuestionClick = (question) => {
    setSelectedQuestion(question)
    console.log('Question clicked:', question)
  }

  return (
    <div className="min-h-screen bg-bg p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-heading font-bold text-white mb-4">
            Follow-Up Questions Demo
          </h1>
          <p className="text-text-secondary font-body text-lg">
            Claude AI-style interactive question interface
          </p>
        </motion.div>

        {/* Content Type Selector */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex justify-center gap-4 mb-6">
            {Object.keys(demoQuestions).map((type) => (
              <button
                key={type}
                onClick={() => {
                  setCurrentType(type)
                  setSelectedQuestion(null)
                }}
                className={`px-6 py-3 rounded-xl font-body font-medium transition-all duration-300 ${
                  currentType === type
                    ? 'bg-peach text-black shadow-lg'
                    : 'bg-surface-raised text-white border border-white/10 hover:border-peach/50'
                }`}
              >
                {type.replace('_', ' ').toUpperCase()}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Mock Chat Window */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-surface-raised border border-white/10 rounded-2xl p-8 mb-6 min-h-[200px] flex items-center justify-center"
        >
          {selectedQuestion ? (
            <div className="text-center">
              <p className="text-white font-body text-lg mb-2">
                You selected:
              </p>
              <p className="text-peach font-body text-xl font-medium">
                "{selectedQuestion}"
              </p>
            </div>
          ) : (
            <p className="text-text-secondary font-body text-lg">
              Click a question below to see it in action
            </p>
          )}
        </motion.div>

        {/* Follow-Up Questions Component */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <FollowUpQuestions
            questions={demoQuestions[currentType]}
            onQuestionClick={handleQuestionClick}
            isLoading={false}
          />
        </motion.div>

        {/* Features List */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="bg-surface-raised border border-white/10 rounded-xl p-6">
            <div className="w-12 h-12 bg-peach/20 rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">🎯</span>
            </div>
            <h3 className="text-white font-heading font-bold text-lg mb-2">
              Context-Aware
            </h3>
            <p className="text-text-secondary font-body text-sm">
              Questions adapt based on content type and user input
            </p>
          </div>

          <div className="bg-surface-raised border border-white/10 rounded-xl p-6">
            <div className="w-12 h-12 bg-peach/20 rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">✨</span>
            </div>
            <h3 className="text-white font-heading font-bold text-lg mb-2">
              Smooth Animations
            </h3>
            <p className="text-text-secondary font-body text-sm">
              Elegant transitions and hover effects for better UX
            </p>
          </div>

          <div className="bg-surface-raised border border-white/10 rounded-xl p-6">
            <div className="w-12 h-12 bg-peach/20 rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">🚀</span>
            </div>
            <h3 className="text-white font-heading font-bold text-lg mb-2">
              One-Click Send
            </h3>
            <p className="text-text-secondary font-body text-sm">
              Click any question to instantly send it as a message
            </p>
          </div>
        </motion.div>

        {/* Code Example */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-12 bg-surface-raised border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-white font-heading font-bold text-lg mb-4">
            Usage Example
          </h3>
          <pre className="text-text-secondary font-mono text-sm overflow-x-auto">
{`<FollowUpQuestions 
  questions={followUpQuestions}
  onQuestionClick={handleFollowUpClick}
  isLoading={loadingFollowUp}
/>`}
          </pre>
        </motion.div>
      </div>
    </div>
  )
}

export default FollowUpQuestionsDemo
