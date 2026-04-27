import { FileText, Mail, Share2, Megaphone, MessageCircle } from 'lucide-react'

const ContentTypeSelector = ({ value, onChange }) => {
  const contentTypes = [
    { value: 'general', label: 'General', icon: MessageCircle },
    { value: 'blog_post', label: 'Blog Post', icon: FileText },
    { value: 'email', label: 'Email', icon: Mail },
    { value: 'social_media', label: 'Social Media', icon: Share2 },
    { value: 'ad_copy', label: 'Ad Copy', icon: Megaphone },
  ]

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-text-secondary">Content Type:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
      >
        {contentTypes.map((type) => (
          <option key={type.value} value={type.value}>
            {type.label}
          </option>
        ))}
      </select>
    </div>
  )
}

export default ContentTypeSelector
