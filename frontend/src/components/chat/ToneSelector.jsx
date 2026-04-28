import { useState, useRef, useEffect } from 'react'
import { Smile, Briefcase, GraduationCap, Zap, Heart, Sparkles, Users, ChevronDown } from 'lucide-react'

const ToneSelector = ({ value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  const tones = [
    { value: 'professional', label: 'Professional', icon: Briefcase, desc: 'Formal, business-appropriate' },
    { value: 'casual', label: 'Casual', icon: Smile, desc: 'Friendly, conversational' },
    { value: 'formal', label: 'Formal', icon: GraduationCap, desc: 'Academic, sophisticated' },
    { value: 'persuasive', label: 'Persuasive', icon: Zap, desc: 'Convincing, compelling' },
    { value: 'friendly', label: 'Friendly', icon: Heart, desc: 'Warm, personable' },
    { value: 'witty', label: 'Witty', icon: Sparkles, desc: 'Humorous, clever' },
    { value: 'empathetic', label: 'Empathetic', icon: Users, desc: 'Understanding, compassionate' },
  ]

  const selectedTone = tones.find(t => t.value === value) || tones[0]

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
      <span className="text-sm text-text-secondary">Tone:</span>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between w-40 px-4 py-2 bg-surface-raised border border-border rounded-xl text-white font-body focus:outline-none focus:ring-2 focus:ring-peach transition-colors"
          title={selectedTone.desc}
        >
          <div className="flex items-center space-x-2 truncate">
            <selectedTone.icon className="w-4 h-4 text-peach flex-shrink-0" />
            <span className="truncate">{selectedTone.label}</span>
          </div>
          <ChevronDown className="w-4 h-4 text-text-secondary flex-shrink-0 ml-2" />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-2 w-48 bg-surface-raised border border-border rounded-xl shadow-xl z-50 overflow-hidden py-1 max-h-60 overflow-y-auto custom-scrollbar">
            {tones.map((tone) => (
              <button
                key={tone.value}
                onClick={() => {
                  onChange(tone.value)
                  setIsOpen(false)
                }}
                title={tone.desc}
                className={`w-full text-left px-4 py-2.5 flex items-center space-x-2 font-body transition-colors ${
                  value === tone.value
                    ? 'bg-peach/20 text-peach'
                    : 'text-white hover:bg-peach/10 hover:text-peach'
                }`}
              >
                <tone.icon className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{tone.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ToneSelector
