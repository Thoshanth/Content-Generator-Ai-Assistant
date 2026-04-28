import { FileText, Mail, Share2, Megaphone, MessageCircle, Code, FileCode, Video, Package, BookOpen, Twitter, Briefcase } from 'lucide-react'

const ContentTypeSelector = ({ value, onChange }) => {
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
