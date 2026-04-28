import { Smile, Briefcase, GraduationCap, Zap, Heart, Sparkles, Users } from 'lucide-react'

const ToneSelector = ({ value, onChange }) => {
  const tones = [
    { value: 'professional', label: 'Professional', icon: Briefcase, desc: 'Formal, business-appropriate' },
    { value: 'casual', label: 'Casual', icon: Smile, desc: 'Friendly, conversational' },
    { value: 'formal', label: 'Formal', icon: GraduationCap, desc: 'Academic, sophisticated' },
    { value: 'persuasive', label: 'Persuasive', icon: Zap, desc: 'Convincing, compelling' },
    { value: 'friendly', label: 'Friendly', icon: Heart, desc: 'Warm, personable' },
    { value: 'witty', label: 'Witty', icon: Sparkles, desc: 'Humorous, clever' },
    { value: 'empathetic', label: 'Empathetic', icon: Users, desc: 'Understanding, compassionate' },
  ]

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-text-secondary">Tone:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
        title={tones.find(t => t.value === value)?.desc}
      >
        {tones.map((tone) => (
          <option key={tone.value} value={tone.value} title={tone.desc}>
            {tone.label}
          </option>
        ))}
      </select>
    </div>
  )
}

export default ToneSelector
