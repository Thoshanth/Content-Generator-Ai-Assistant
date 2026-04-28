import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'
import { Eye, EyeOff } from 'lucide-react'
import { motion } from 'framer-motion'

const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await login(email, password)
      toast.success('Login successful!')
      const from = location.state?.from || '/chat'
      navigate(from, { replace: true })
    } catch (error) {
      toast.error(error.response?.data?.error || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex bg-bg relative overflow-hidden">
      {/* Left Column: Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 lg:p-12 z-10 relative">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="max-w-[440px] w-full"
        >
          <div className="mb-10">
            <Link to="/" className="inline-flex items-center space-x-3 mb-10 group">
              <img src="/logo.png" alt="Logo" className="h-10 w-10 object-contain drop-shadow-[0_0_8px_rgba(249,168,168,0.5)] transition-transform group-hover:scale-105" />
              <span className="text-xl font-heading font-bold text-white tracking-wide">
                Creo<span className="text-peach">.AI</span>
              </span>
            </Link>
            <h1 className="text-4xl font-heading font-bold text-white mb-3 tracking-tight">Welcome back</h1>
            <p className="text-base font-body text-text-secondary">Sign in to your workspace and continue creating.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-body font-medium text-white mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field bg-surface/50 backdrop-blur-sm border-white/10 hover:border-peach/50 focus:bg-surface-raised transition-all"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-body font-medium text-white mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field bg-surface/50 backdrop-blur-sm border-white/10 hover:border-peach/50 focus:bg-surface-raised transition-all pr-12"
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember_me"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="h-4 w-4 rounded border-white/20 bg-surface text-peach focus:ring-peach focus:ring-offset-bg cursor-pointer transition-colors"
                />
                <label htmlFor="remember_me" className="ml-2 block text-sm font-body text-text-secondary cursor-pointer hover:text-white transition-colors">
                  Remember me
                </label>
              </div>
              <a href="#" className="text-sm font-body font-medium text-text-secondary hover:text-peach transition-colors">
                Forgot password?
              </a>
            </div>

            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3.5 mt-4 shadow-[0_0_20px_rgba(249,168,168,0.15)] hover:shadow-[0_0_30px_rgba(249,168,168,0.3)]"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
            </motion.button>
          </form>

          <div className="mt-10 pt-8 border-t border-white/5 text-center">
            <p className="text-sm font-body text-text-secondary">
              Don't have an account?{' '}
              <Link to="/register" className="text-white hover:text-peach transition-colors font-medium ml-1">
                Create workspace &rarr;
              </Link>
            </p>
          </div>
        </motion.div>
      </div>

      {/* Right Column: Logo Display */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-surface-raised border-l border-white/5 items-center justify-center">
        {/* Subtle background glow */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(249,168,168,0.03)_0%,transparent_70%)] pointer-events-none"></div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="relative z-10 flex flex-col items-center justify-center text-center p-12"
        >
          {/* Glowing Logo Container */}
          <div className="relative w-48 h-48 md:w-64 md:h-64 mb-10 flex items-center justify-center group">
            {/* Animated aura */}
            <div className="absolute inset-0 bg-peach/20 blur-[80px] rounded-full group-hover:bg-peach/30 transition-colors duration-700"></div>
            <img 
              src="/logo.png" 
              alt="Creo AI Logo" 
              className="w-full h-full object-contain relative z-10 drop-shadow-[0_0_25px_rgba(249,168,168,0.5)] transition-transform duration-700 hover:scale-105"
            />
          </div>
          
          <h2 className="text-4xl md:text-5xl font-heading font-bold text-white mb-4 tracking-tight">
            Creo<span className="text-peach">.AI</span>
          </h2>
          <p className="text-lg font-body text-text-secondary max-w-sm leading-relaxed">
            The premier AI content generation platform for forward-thinking teams and creators.
          </p>
        </motion.div>
      </div>
    </div>
  )
}

export default LoginPage
