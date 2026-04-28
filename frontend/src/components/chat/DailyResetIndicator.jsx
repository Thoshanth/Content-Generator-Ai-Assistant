import { useState, useEffect } from 'react'
import { Clock } from 'lucide-react'
import { motion } from 'framer-motion'

const DailyResetIndicator = ({ dailyMessageCount = 0, maxMessages = 10 }) => {
  const [timeUntilReset, setTimeUntilReset] = useState('')

  useEffect(() => {
    const calculateTimeUntilMidnight = () => {
      const now = new Date()
      const midnight = new Date()
      midnight.setHours(24, 0, 0, 0)
      
      const diff = midnight - now
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((diff % (1000 * 60)) / 1000)
      
      return `${hours}h ${minutes}m ${seconds}s`
    }

    const updateTimer = () => {
      setTimeUntilReset(calculateTimeUntilMidnight())
    }

    updateTimer()
    const interval = setInterval(updateTimer, 1000)

    return () => clearInterval(interval)
  }, [])

  const percentage = (dailyMessageCount / maxMessages) * 100
  const isNearLimit = dailyMessageCount >= maxMessages * 0.8

  return (
    <motion.div 
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-surface-raised border border-border rounded-xl p-3 space-y-2"
    >
      {/* Progress Bar */}
      <div className="flex items-center justify-between text-xs font-body">
        <span className="text-text-secondary">Daily Usage</span>
        <span className={`font-bold ${isNearLimit ? 'text-error' : 'text-peach'}`}>
          {dailyMessageCount}/{maxMessages}
        </span>
      </div>
      
      <div className="w-full bg-surface h-2 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className={`h-full rounded-full ${
            isNearLimit 
              ? 'bg-gradient-to-r from-error to-error/70' 
              : 'bg-gradient-to-r from-peach to-peach/70'
          }`}
        />
      </div>

      {/* Reset Timer */}
      <div className="flex items-center justify-between text-[10px] font-body text-text-muted">
        <div className="flex items-center space-x-1">
          <Clock className="w-3 h-3" />
          <span>Resets in</span>
        </div>
        <motion.span 
          animate={{ opacity: [1, 0.5, 1] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="font-mono text-peach"
        >
          {timeUntilReset}
        </motion.span>
      </div>
    </motion.div>
  )
}

export default DailyResetIndicator
