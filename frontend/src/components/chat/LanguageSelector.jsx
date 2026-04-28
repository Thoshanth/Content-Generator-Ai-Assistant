import { Globe } from 'lucide-react'

const LanguageSelector = ({ value, onChange }) => {
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

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-text-secondary">Language:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
      >
        {languages.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.flag} {lang.label}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LanguageSelector
