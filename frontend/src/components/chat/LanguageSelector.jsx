import { useState, useRef, useEffect } from 'react'
import { Globe, ChevronDown } from 'lucide-react'

const LanguageSelector = ({ value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  const languages = [
    { value: 'English', label: 'English', flag: '🇺🇸' },
    { value: 'Hindi', label: 'Hindi', flag: '🇮🇳' },
    { value: 'Telugu', label: 'Telugu', flag: '🇮🇳' },
    { value: 'Spanish', label: 'Spanish', flag: '🇪🇸' },
    { value: 'French', label: 'French', flag: '🇫🇷' },
    { value: 'German', label: 'German', flag: '🇩🇪' },
    { value: 'Portuguese', label: 'Portuguese', flag: '🇵🇹' },
    { value: 'Arabic', label: 'Arabic', flag: '🇸🇦' },
    { value: 'Japanese', label: 'Japanese', flag: '🇯🇵' },
    { value: 'Chinese (Simplified)', label: 'Chinese', flag: '🇨🇳' },
    { value: 'Korean', label: 'Korean', flag: '🇰🇷' },
  ]

  const selectedLang = languages.find(l => l.value === value) || languages[0]

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
      <span className="text-sm text-text-secondary">Language:</span>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between w-40 px-4 py-2 bg-surface-raised border border-border rounded-xl text-white font-body focus:outline-none focus:ring-2 focus:ring-peach transition-colors"
        >
          <div className="flex items-center space-x-2 truncate">
            <span className="flex-shrink-0 text-peach">{selectedLang.flag}</span>
            <span className="truncate">{selectedLang.label}</span>
          </div>
          <ChevronDown className="w-4 h-4 text-text-secondary flex-shrink-0 ml-2" />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-2 w-48 bg-surface-raised border border-border rounded-xl shadow-xl z-50 overflow-hidden py-1 max-h-60 overflow-y-auto custom-scrollbar">
            {languages.map((lang) => (
              <button
                key={lang.value}
                onClick={() => {
                  onChange(lang.value)
                  setIsOpen(false)
                }}
                className={`w-full text-left px-4 py-2.5 flex items-center space-x-2 font-body transition-colors ${
                  value === lang.value
                    ? 'bg-peach/20 text-peach'
                    : 'text-white hover:bg-peach/10 hover:text-peach'
                }`}
              >
                <span className="flex-shrink-0">{lang.flag}</span>
                <span className="truncate">{lang.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default LanguageSelector
