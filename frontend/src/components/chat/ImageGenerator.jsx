import { useState, useEffect } from 'react'
import { Image as ImageIcon, Wand2, Settings, X, Loader2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const ImageGenerator = ({ onGenerate, onClose, isGenerating }) => {
  const [prompt, setPrompt] = useState('')
  const [negativePrompt, setNegativePrompt] = useState('')
  const [style, setStyle] = useState('realistic')
  const [preset, setPreset] = useState('square')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [customSettings, setCustomSettings] = useState({
    width: 512,
    height: 512,
    steps: 30,
    guidanceScale: 7.5
  })
  const [styles, setStyles] = useState([])
  const [presets, setPresets] = useState({})
  const [usage, setUsage] = useState({ dailyCount: 0, dailyLimit: 5, remaining: 5 })

  useEffect(() => {
    fetchStyles()
    fetchPresets()
    fetchUsage()
  }, [])

  const fetchStyles = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/images/styles', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setStyles(data.styles || [])
      }
    } catch (error) {
      console.error('Failed to fetch styles:', error)
    }
  }

  const fetchPresets = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/images/presets', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setPresets(data.presets || {})
      }
    } catch (error) {
      console.error('Failed to fetch presets:', error)
    }
  }

  const fetchUsage = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/images/usage', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setUsage(data)
      }
    } catch (error) {
      console.error('Failed to fetch usage:', error)
    }
  }

  const handlePresetChange = (presetName) => {
    setPreset(presetName)
    if (presets[presetName]) {
      setCustomSettings({
        width: presets[presetName].width,
        height: presets[presetName].height,
        steps: presets[presetName].steps,
        guidanceScale: presets[presetName].guidance_scale
      })
    }
  }

  const handleGenerate = () => {
    if (!prompt.trim()) return
    if (usage.remaining <= 0) {
      alert('You have reached your daily limit of 5 images. Please try again tomorrow.')
      return
    }

    const imageRequest = {
      prompt: prompt.trim(),
      negativePrompt: negativePrompt.trim() || undefined,
      style: style,
      width: customSettings.width,
      height: customSettings.height,
      steps: customSettings.steps,
      guidanceScale: customSettings.guidanceScale
    }

    onGenerate(imageRequest)
    setPrompt('')
    setNegativePrompt('')
    
    // Update usage count optimistically
    setUsage(prev => ({
      ...prev,
      dailyCount: prev.dailyCount + 1,
      remaining: Math.max(0, prev.remaining - 1)
    }))
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
    >
      <motion.div
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        className="bg-surface-raised border border-white/10 rounded-2xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto custom-scrollbar"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-peach-subtle rounded-full flex items-center justify-center">
              <ImageIcon className="w-5 h-5 text-peach" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-white">Generate Image</h2>
              <p className="text-sm text-text-secondary">
                {usage.remaining} of {usage.dailyLimit} images remaining today
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-surface-raised border border-white/10 flex items-center justify-center text-text-secondary hover:text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Usage Warning */}
        {usage.remaining <= 1 && (
          <div className="mb-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <p className="text-sm text-yellow-400">
              {usage.remaining === 0 
                ? "You've reached your daily limit. Try again tomorrow!"
                : "This is your last image for today!"
              }
            </p>
          </div>
        )}

        {/* Main Prompt */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Describe your image
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="A beautiful sunset over mountains, peaceful landscape..."
              className="w-full px-4 py-3 bg-surface-raised border border-white/10 rounded-xl text-white placeholder-text-secondary font-body focus:outline-none focus:border-peach/50 focus:shadow-[0_0_20px_rgba(249,168,168,0.15)] transition-all duration-300 resize-none custom-scrollbar"
              rows="3"
              maxLength="1000"
            />
            <div className="text-xs text-text-secondary mt-1">
              {prompt.length}/1000 characters
            </div>
          </div>

          {/* Style Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Style
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {styles.map((styleOption) => (
                <button
                  key={styleOption.id}
                  onClick={() => setStyle(styleOption.id)}
                  className={`p-3 rounded-lg border text-sm font-medium transition-all ${
                    style === styleOption.id
                      ? 'bg-peach text-black border-peach'
                      : 'bg-surface-raised border-white/10 text-white hover:border-peach/50'
                  }`}
                >
                  {styleOption.name}
                </button>
              ))}
            </div>
          </div>

          {/* Preset Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Size Preset
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {Object.entries(presets).map(([presetName, presetData]) => (
                <button
                  key={presetName}
                  onClick={() => handlePresetChange(presetName)}
                  className={`p-3 rounded-lg border text-sm transition-all ${
                    preset === presetName
                      ? 'bg-peach text-black border-peach'
                      : 'bg-surface-raised border-white/10 text-white hover:border-peach/50'
                  }`}
                >
                  <div className="font-medium capitalize">{presetName.replace('_', ' ')}</div>
                  <div className="text-xs opacity-70">
                    {presetData.width}×{presetData.height}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Advanced Settings Toggle */}
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center space-x-2 text-sm text-peach hover:text-peach-light transition-colors"
          >
            <Settings className="w-4 h-4" />
            <span>Advanced Settings</span>
          </button>

          {/* Advanced Settings */}
          <AnimatePresence>
            {showAdvanced && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="space-y-4 overflow-hidden"
              >
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Negative Prompt (what to avoid)
                  </label>
                  <textarea
                    value={negativePrompt}
                    onChange={(e) => setNegativePrompt(e.target.value)}
                    placeholder="blurry, low quality, distorted..."
                    className="w-full px-4 py-3 bg-surface-raised border border-white/10 rounded-xl text-white placeholder-text-secondary font-body focus:outline-none focus:border-peach/50 transition-all duration-300 resize-none"
                    rows="2"
                    maxLength="500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Steps: {customSettings.steps}
                    </label>
                    <input
                      type="range"
                      min="10"
                      max="50"
                      value={customSettings.steps}
                      onChange={(e) => setCustomSettings(prev => ({ ...prev, steps: parseInt(e.target.value) }))}
                      className="w-full accent-peach"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Guidance: {customSettings.guidanceScale}
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="20"
                      step="0.5"
                      value={customSettings.guidanceScale}
                      onChange={(e) => setCustomSettings(prev => ({ ...prev, guidanceScale: parseFloat(e.target.value) }))}
                      className="w-full accent-peach"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating || usage.remaining <= 0}
            className="w-full bg-peach hover:bg-peach-light disabled:bg-gray-600 disabled:cursor-not-allowed text-black font-semibold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center space-x-2"
          >
            {isGenerating ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Wand2 className="w-5 h-5" />
                <span>Generate Image</span>
              </>
            )}
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default ImageGenerator