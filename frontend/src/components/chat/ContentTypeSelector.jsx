import { useState, useRef, useEffect } from 'react'
import { FileText, Mail, Share2, Megaphone, MessageCircle, Code, FileCode, Video, Package, BookOpen, Twitter, Briefcase, ChevronDown } from 'lucide-react'

const ContentTypeSelector = ({ value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  const contentTypes = [
    { value: 'general', label: 'General', icon: MessageCircle },
    { value: 'blog_post', label: 'Blog Post', icon: FileText },
    { value: 'email', label: 'Email', icon: Mail },
    { value: 'social_media', label: 'Social Media', icon: Share2 },
    { value: 'ad_copy', label: 'Ad Copy', icon: Megaphone },
    { value: 'tweet_thread', label: 'Tweet Thread', icon: Twitter },
    { value: 'resume', label: 'Resume', icon: Briefcase },
    { value: 'cover_letter', label: 'Cover Letter', icon: FileText },
    { value: 'youtube_script', label: 'YouTube Script', icon: Video },
    { value: 'product_desc', label: 'Product Description', icon: Package },
    { value: 'essay', label: 'Essay', icon: BookOpen },
    { value: 'code_explainer', label: 'Code Explainer', icon: Code },
  ]

  const selectedType = contentTypes.find(t => t.value === value) || contentTypes[0]

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
      <span className="text-sm text-text-secondary">Content Type:</span>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between w-48 px-4 py-2 bg-surface-raised border border-border rounded-xl text-white font-body focus:outline-none focus:ring-2 focus:ring-peach transition-colors"
        >
          <div className="flex items-center space-x-2 truncate">
            <selectedType.icon className="w-4 h-4 text-peach flex-shrink-0" />
            <span className="truncate">{selectedType.label}</span>
          </div>
          <ChevronDown className="w-4 h-4 text-text-secondary flex-shrink-0 ml-2" />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-2 w-48 bg-surface-raised border border-border rounded-xl shadow-xl z-50 overflow-hidden py-1 max-h-60 overflow-y-auto custom-scrollbar">
            {contentTypes.map((type) => (
              <button
                key={type.value}
                onClick={() => {
                  onChange(type.value)
                  setIsOpen(false)
                }}
                className={`w-full text-left px-4 py-2.5 flex items-center space-x-2 font-body transition-colors ${
                  value === type.value
                    ? 'bg-peach/20 text-peach'
                    : 'text-white hover:bg-peach/10 hover:text-peach'
                }`}
              >
                <type.icon className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{type.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ContentTypeSelector
