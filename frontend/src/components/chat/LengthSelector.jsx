import { Minus, Equal, Plus, Sparkles } from 'lucide-react'

const LengthSelector = ({ value, onChange }) => {
  const lengths = [
    { value: 'short', label: 'Short', icon: Minus, desc: '100-300 words' },
    { value: 'medium', label: 'Medium', icon: Equal, desc: '300-800 words' },
    { value: 'long', label: 'Long', icon: Plus, desc: '800+ words' },
    { value: 'auto', label: 'Auto', icon: Sparkles, desc: 'AI decides' },
  ]

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-text-secondary">Length:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
        title={lengths.find(l => l.value === value)?.desc}
      >
        {lengths.map((length) => (
          <option key={length.value} value={length.value} title={length.desc}>
            {length.label}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LengthSelector
