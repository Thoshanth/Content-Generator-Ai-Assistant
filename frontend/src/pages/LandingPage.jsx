import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Sparkles, FileText, Mail, Share2, Megaphone } from 'lucide-react'

const LandingPage = () => {
  const { isAuthenticated } = useAuth()

  const contentTypes = [
    { icon: FileText, name: 'Blog Posts', desc: 'SEO-optimized articles' },
    { icon: Mail, name: 'Emails', desc: 'Professional communication' },
    { icon: Share2, name: 'Social Media', desc: 'Engaging posts' },
    { icon: Megaphone, name: 'Ad Copy', desc: 'Conversion-focused' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-light via-white to-primary-light">
      {/* Navbar */}
      <nav className="bg-white border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-8 h-8 text-primary" />
              <span className="text-xl font-bold text-text-primary">AI Content Generator</span>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <Link to="/chat" className="btn-primary">
                    Go to Chat
                  </Link>
                  <Link to="/profile" className="text-text-secondary hover:text-text-primary">
                    Profile
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-text-secondary hover:text-text-primary">
                    Login
                  </Link>
                  <Link to="/register" className="btn-primary">
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-text-primary mb-6">
            AI-Powered Content
            <br />
            <span className="text-primary">Generation Made Easy</span>
          </h1>
          <p className="text-xl text-text-secondary mb-8 max-w-2xl mx-auto">
            Create blog posts, emails, social media content, and ad copy in seconds with our
            advanced AI technology. Free to use with no credit card required.
          </p>
          <div className="flex justify-center space-x-4">
            <Link to={isAuthenticated ? '/chat' : '/register'} className="btn-primary text-lg px-8 py-3">
              Start Creating Free
            </Link>
            <a href="#features" className="btn-secondary text-lg px-8 py-3">
              Learn More
            </a>
          </div>
        </div>

        {/* Content Types */}
        <div id="features" className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {contentTypes.map((type) => (
            <div key={type.name} className="card text-center hover:shadow-lg transition-shadow">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-light rounded-full mb-4">
                <type.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-text-primary mb-2">{type.name}</h3>
              <p className="text-text-secondary">{type.desc}</p>
            </div>
          ))}
        </div>

        {/* Features */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-text-primary mb-12">
            Why Choose Our Platform?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card">
              <h3 className="text-xl font-semibold text-text-primary mb-3">⚡ Lightning Fast</h3>
              <p className="text-text-secondary">
                Generate high-quality content in seconds with our optimized AI models
              </p>
            </div>
            <div className="card">
              <h3 className="text-xl font-semibold text-text-primary mb-3">🎯 Multiple Formats</h3>
              <p className="text-text-secondary">
                Create blog posts, emails, social media content, and advertising copy
              </p>
            </div>
            <div className="card">
              <h3 className="text-xl font-semibold text-text-primary mb-3">💾 Save History</h3>
              <p className="text-text-secondary">
                All your conversations are saved and can be accessed anytime
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-20 text-center">
          <div className="card max-w-2xl mx-auto bg-gradient-to-r from-primary to-primary-accent text-white">
            <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
            <p className="text-lg mb-6 opacity-90">
              Join thousands of users creating amazing content with AI
            </p>
            <Link
              to={isAuthenticated ? '/chat' : '/register'}
              className="inline-block bg-white text-primary font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors"
            >
              Start Creating Now
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-border mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-text-secondary">
            <p>&copy; 2024 AI Content Generator. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
