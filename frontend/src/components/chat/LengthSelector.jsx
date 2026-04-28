import { useState, useRef, useEffect } from 'react'
import { Minus, Equal, Plus, Sparkles, ChevronDown } from 'lucide-react'

const LengthSelector = ({ value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  const lengths = [
    { value: 'short', label: 'Short', icon: Minus, desc: '100-300 words' },
    { value: 'medium', label: 'Medium', icon: Equal, desc: '300-800 words' },
    { value: 'long', label: 'Long', icon: Plus, desc: '800+ words' },
    { value: 'auto', label: 'Auto', icon: Sparkles, desc: 'AI decides' },
  ]

  const selectedLength = lengths.find(l => l.value === value) || lengths[3]

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-text-secondary">Length:</span>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between w-36 px-4 py-2 bg-surface-raised border border-border rounded-xl text-white font-body focus:outline-none focus:ring-2 focus:ring-peach transition-colors"
          title={selectedLength.desc}
        >
          <div className="flex items-center space-x-2 truncate">
            <selectedLength.icon className="w-4 h-4 text-peach flex-shrink-0" />
            <span className="truncate">{selectedLength.label}</span>
          </div>
          <ChevronDown className="w-4 h-4 text-text-secondary flex-shrink-0 ml-2" />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-2 w-48 bg-surface-raised border border-border rounded-xl shadow-xl z-50 overflow-hidden py-1 max-h-60 overflow-y-auto custom-scrollbar">
            {lengths.map((length) => (
              <button
                key={length.value}
                onClick={() => {
                  onChange(length.value)
                  setIsOpen(false)
                }}
                title={length.desc}
                className={`w-full text-left px-4 py-2.5 flex items-center space-x-2 font-body transition-colors ${
                  value === length.value
                    ? 'bg-peach/20 text-peach'
                    : 'text-white hover:bg-peach/10 hover:text-peach'
                }`}
              >
                <length.icon className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{length.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default LengthSelector
