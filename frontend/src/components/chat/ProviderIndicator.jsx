import { Zap, FileText, Code, Star } from 'lucide-react'

const ProviderIndicator = ({ provider, model }) => {
  const providers = {
    'Groq': { icon: Zap, color: 'text-orange-400', bg: 'bg-surface-raised border border-orange-400/20', desc: 'Speed/Creative' },
    'Gemini': { icon: FileText, color: 'text-blue-400', bg: 'bg-surface-raised border border-blue-400/20', desc: 'Structured' },
    'NVIDIA NIM': { icon: Code, color: 'text-green-400', bg: 'bg-surface-raised border border-green-400/20', desc: 'Technical' },
    'Cerebras': { icon: Star, color: 'text-purple-400', bg: 'bg-surface-raised border border-purple-400/20', desc: 'Fallback' },
  }

  if (!provider) return null

  const config = providers[provider] || { icon: Star, color: 'text-text-secondary', bg: 'bg-surface-raised border border-border', desc: 'AI' }
  const Icon = config.icon

  return (
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full ${config.bg} ${config.color} text-xs font-medium font-body`}>
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
