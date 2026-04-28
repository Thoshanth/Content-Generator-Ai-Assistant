import { Zap, FileText, Code, Star } from 'lucide-react'

const ProviderIndicator = ({ provider, model }) => {
  const providers = {
    'Groq': { icon: Zap, color: 'text-orange-600', bg: 'bg-orange-50', desc: 'Speed/Creative' },
    'Gemini': { icon: FileText, color: 'text-blue-600', bg: 'bg-blue-50', desc: 'Structured' },
    'NVIDIA NIM': { icon: Code, color: 'text-green-600', bg: 'bg-green-50', desc: 'Technical' },
    'Cerebras': { icon: Star, color: 'text-purple-600', bg: 'bg-purple-50', desc: 'Fallback' },
  }

  if (!provider) return null

  const config = providers[provider] || { icon: Star, color: 'text-gray-600', bg: 'bg-gray-50', desc: 'AI' }
  const Icon = config.icon

  return (
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full ${config.bg} ${config.color} text-xs font-medium`}>
      <Icon className="w-3 h-3" />
      <span>{provider}</span>
      {model && (
        <span className="text-xs opacity-75">
          • {model.split('/').pop().substring(0, 20)}
        </span>
      )}
    </div>
  )
}

export default ProviderIndicator
