import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FileText, Mail, Share2, Megaphone, Zap, BrainCircuit, Globe, Layers, ChevronRight, ArrowRight } from 'lucide-react'
import { motion, useScroll, useTransform, useMotionValue, useSpring } from 'framer-motion'

const LandingPage = () => {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const { scrollYProgress } = useScroll()
  const yPos = useTransform(scrollYProgress, [0, 1], [0, -200])
  
  // Mouse Follower state
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)
  const springX = useSpring(mouseX, { stiffness: 100, damping: 30 })
  const springY = useSpring(mouseY, { stiffness: 100, damping: 30 })

  const handleMouseMove = (e) => {
    mouseX.set(e.clientX)
    mouseY.set(e.clientY)
  }
  
  // Typing Effect State
  const [text, setText] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)
  const [loopNum, setLoopNum] = useState(0)
  const [typingSpeed, setTypingSpeed] = useState(150)
  
  const words = ['Blog Posts', 'Viral Threads', 'Ad Copy', 'Cold Emails']

  useEffect(() => {
    const handleType = () => {
      const i = loopNum % words.length
      const fullText = words[i]

      setText(isDeleting 
        ? fullText.substring(0, text.length - 1) 
        : fullText.substring(0, text.length + 1)
      )

      setTypingSpeed(isDeleting ? 30 : 100)

      if (!isDeleting && text === fullText) {
        setTimeout(() => setIsDeleting(true), 2000)
      } else if (isDeleting && text === '') {
        setIsDeleting(false)
        setLoopNum(loopNum + 1)
      }
    }

    const timer = setTimeout(handleType, typingSpeed)
    return () => clearTimeout(timer)
  }, [text, isDeleting, loopNum, typingSpeed, words])

  const handleGetStarted = () => {
    navigate('/chat')
  }

  const contentTypes = [
    { icon: FileText, name: 'SEO-Optimized Blog Posts', desc: 'Craft long-form content that ranks on search engines and engages your core audience with deep, insightful analysis.' },
    { icon: Mail, name: 'High-Converting Emails', desc: 'Generate professional, persuasive email campaigns designed to maximize open rates and drive immediate action.' },
    { icon: Share2, name: 'Viral Social Media', desc: 'Create platform-specific, punchy social media content tailored for Twitter, LinkedIn, and Instagram audiences.' },
    { icon: Megaphone, name: 'Compelling Ad Copy', desc: 'Write conversion-focused advertising copy for Facebook and Google Ads that significantly lowers your CPA.' },
  ]

  const benefits = [
    { icon: Zap, title: 'Lightning Fast Generation', desc: 'Experience zero latency. Our highly optimized infrastructure delivers complex content in milliseconds, not minutes.' },
    { icon: BrainCircuit, title: 'Advanced AI Models', desc: 'Powered by the latest breakthrough foundational models, ensuring human-like reasoning and impeccable grammar.' },
    { icon: Globe, title: 'Multilingual Capabilities', desc: 'Break global barriers. Generate localized content fluently across dozens of languages without losing cultural nuance.' },
    { icon: Layers, title: 'Infinite Formats', desc: 'From technical code explanations to creative essays, our platform seamlessly adapts to any content structure you need.' },
  ]

  // Animation Variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.2, delayChildren: 0.1 }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30, scale: 0.95 },
    visible: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { type: "spring", stiffness: 100, damping: 15 } 
    }
  }

  return (
    <div className="min-h-screen bg-bg selection:bg-peach/30" onMouseMove={handleMouseMove}>
      
      {/* Dynamic Cursor Glow (Desktop Only) */}
      <motion.div 
        className="fixed top-0 left-0 w-96 h-96 bg-peach/20 rounded-full blur-[100px] pointer-events-none z-0 hidden lg:block"
        style={{
          x: springX,
          y: springY,
          translateX: '-50%',
          translateY: '-50%'
        }}
      />

      {/* Premium Navbar */}
      <nav className="bg-bg/60 backdrop-blur-xl border-b border-white/5 sticky top-0 z-50 transition-all duration-300">
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className="flex justify-between items-center h-20">
            <Link to="/" className="flex items-center space-x-4 group">
              <motion.img 
                whileHover={{ rotate: 180 }}
                transition={{ duration: 0.6, ease: "easeInOut" }}
                src="/logo.png" 
                alt="Logo" 
                className="h-10 w-10 object-contain drop-shadow-[0_0_8px_rgba(249,168,168,0.5)]" 
              />
              <span className="text-xl font-heading font-bold text-white tracking-wide group-hover:text-peach transition-colors duration-300">
                Synthetix<span className="text-white group-hover:text-peach">.AI</span>
              </span>
            </Link>
            <div className="flex items-center space-x-6">
              {isAuthenticated ? (
                <>
                  <Link to="/profile" className="text-sm font-body font-medium text-text-secondary hover:text-white transition-colors">
                    Dashboard
                  </Link>
                  <motion.button 
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGetStarted} 
                    className="btn-primary py-2.5 px-6 rounded-full shadow-[0_0_15px_rgba(249,168,168,0.3)] relative overflow-hidden group"
                  >
                    <span className="relative z-10">Launch App</span>
                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
                  </motion.button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-sm font-body font-medium text-text-secondary hover:text-white transition-colors">
                    Sign In
                  </Link>
                  <motion.button 
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGetStarted} 
                    className="btn-primary py-2.5 px-6 rounded-full shadow-[0_0_15px_rgba(249,168,168,0.3)] flex items-center space-x-2 group relative overflow-hidden"
                  >
                    <span className="relative z-10">Get Started</span>
                    <ArrowRight className="w-4 h-4 relative z-10 group-hover:translate-x-1 transition-transform" />
                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
                  </motion.button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section with Advanced Motion */}
      <div className="relative overflow-hidden min-h-[90vh] flex items-center">
        {/* Background Grid */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik02MCAwaC0xdjYwaDFWMHptMCA1OXYxaC02MHYtMWg2MHoiIGZpbGw9IiNmOWE4YTgiIGZpbGwtb3BhY2l0eT0iMC4wNSIvPjwvZz48L3N2Zz4=')] [mask-image:radial-gradient(ellipse_at_center,black,transparent_80%)] pointer-events-none" />
        
        <motion.div 
          animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-peach/10 blur-[150px] rounded-[40%] pointer-events-none" 
        />
        
        <div className="relative max-w-7xl mx-auto px-6 lg:px-12 pt-10 pb-20 text-center z-10">
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 20 }}
            className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-surface-raised border border-peach/20 mb-8 backdrop-blur-md shadow-[0_0_20px_rgba(249,168,168,0.1)] hover:border-peach/50 transition-colors cursor-default"
          >
            <span className="w-2 h-2 rounded-full bg-peach animate-pulse shadow-[0_0_10px_rgba(249,168,168,1)]" />
            <span className="text-xs font-body font-bold text-peach uppercase tracking-widest">Synthetix Core v5.0 Live</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.1 }}
            className="text-6xl md:text-[6rem] font-heading font-bold text-white mb-8 leading-[1.05] tracking-tight h-[180px] md:h-[220px]"
          >
            Generate<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-peach via-[#ffcccc] to-white border-r-4 border-peach pr-2 animate-blink inline-block pb-4">
              {text}
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-xl md:text-2xl text-text-secondary mb-12 max-w-3xl mx-auto font-body leading-relaxed"
          >
            Unleash the power of enterprise-grade AI to generate pristine assets in mere milliseconds. No friction, just results.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <motion.button 
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(249,168,168,0.6)" }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGetStarted} 
              className="btn-primary text-lg px-10 py-5 rounded-full shadow-[0_0_30px_rgba(249,168,168,0.3)] flex items-center space-x-3 group w-full sm:w-auto justify-center relative overflow-hidden"
            >
              <span className="relative z-10 font-bold tracking-wide">Start Generating</span>
              <ArrowRight className="w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" />
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 ease-in-out"></div>
            </motion.button>
          </motion.div>
        </div>
      </div>

      {/* Core Use Cases Section */}
      <div id="features" className="bg-surface py-32 border-y border-white/5 relative overflow-hidden z-10">
        <motion.div style={{ y: yPos }} className="absolute inset-0 bg-bg opacity-50 z-[-1]" />
        
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={containerVariants}
            className="text-center mb-24"
          >
            <motion.h2 variants={itemVariants} className="text-4xl md:text-6xl font-heading font-bold text-white mb-6">One Platform.<br/>Infinite Possibilities.</motion.h2>
            <motion.p variants={itemVariants} className="text-xl font-body text-text-secondary max-w-2xl mx-auto">Stop jumping between tools. Our AI adapts its architecture to perfectly match the tone, length, and format of whatever you're building.</motion.p>
          </motion.div>

          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            variants={containerVariants}
            className="grid grid-cols-1 md:grid-cols-2 gap-8"
          >
            {contentTypes.map((type) => (
              <motion.div 
                key={type.name}
                variants={itemVariants}
                whileHover={{ y: -10, scale: 1.02 }}
                className="group p-10 bg-bg border border-white/5 rounded-3xl hover:border-peach/40 transition-all duration-300 shadow-xl hover:shadow-[0_20px_40px_rgba(249,168,168,0.1)] relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-64 h-64 bg-peach/10 blur-[80px] rounded-full group-hover:bg-peach/20 group-hover:scale-150 transition-all duration-700 pointer-events-none" />
                <div className="relative z-10">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-surface-raised border border-peach/20 rounded-2xl mb-8 group-hover:rotate-6 transition-transform duration-300 shadow-lg">
                    <type.icon className="w-8 h-8 text-peach" />
                  </div>
                  <h3 className="text-2xl font-heading font-bold text-white mb-4 group-hover:text-peach transition-colors">{type.name}</h3>
                  <p className="text-base font-body text-text-secondary leading-relaxed">{type.desc}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Technology Value Proposition */}
      <div className="py-32 relative overflow-hidden bg-bg">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[600px] bg-gradient-to-b from-transparent via-peach/5 to-transparent pointer-events-none" />
        <div className="max-w-7xl mx-auto px-6 lg:px-12 relative z-10">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={containerVariants}
            className="text-center mb-20"
          >
            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-heading font-bold text-white mb-6">Built for Excellence</motion.h2>
            <motion.p variants={itemVariants} className="text-lg font-body text-text-secondary max-w-2xl mx-auto">We've engineered every aspect of our infrastructure to provide a seamless, state-of-the-art content generation experience.</motion.p>
          </motion.div>

          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            variants={containerVariants}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {benefits.map((benefit) => (
              <motion.div 
                key={benefit.title} 
                variants={itemVariants}
                whileHover={{ y: -5 }}
                className="p-8 bg-surface-raised rounded-3xl border border-white/5 hover:border-peach/30 transition-colors duration-300 relative group overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-b from-peach/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative z-10">
                  <benefit.icon className="w-10 h-10 text-peach mb-6 group-hover:scale-110 transition-transform duration-300" />
                  <h3 className="text-xl font-heading font-bold text-white mb-3">{benefit.title}</h3>
                  <p className="text-sm font-body text-text-secondary leading-relaxed">
                    {benefit.desc}
                  </p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-32 bg-surface border-y border-white/5 relative overflow-hidden">
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
          className="absolute -top-[50%] -right-[20%] w-[1000px] h-[1000px] bg-[radial-gradient(circle,rgba(249,168,168,0.05)_0%,transparent_60%)] pointer-events-none"
        />
        
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
          className="max-w-4xl mx-auto px-6 lg:px-12 text-center relative z-10"
        >
          <motion.h2 variants={itemVariants} className="text-5xl md:text-7xl font-heading font-bold text-white mb-8 tracking-tight">Ready to transform<br/>your workflow?</motion.h2>
          <motion.p variants={itemVariants} className="text-xl text-text-secondary mb-12 font-body">Join thousands of professionals already scaling their output with our AI.</motion.p>
          <motion.div variants={itemVariants}>
            <motion.button 
              whileHover={{ scale: 1.05, boxShadow: "0 0 50px rgba(249,168,168,0.5)" }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGetStarted} 
              className="btn-primary text-xl px-14 py-6 rounded-full shadow-[0_0_30px_rgba(249,168,168,0.3)] relative overflow-hidden group"
            >
              <span className="relative z-10 font-bold">Open Application</span>
              <div className="absolute inset-0 bg-white/20 translate-y-[100%] group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
            </motion.button>
          </motion.div>
        </motion.div>
      </div>

      {/* Minimal Footer */}
      <footer className="bg-bg pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-16">
            <div className="col-span-1 md:col-span-1">
              <div className="flex items-center space-x-3 mb-6">
                <img src="/logo.png" alt="Logo" className="h-8 w-8 object-contain opacity-80" />
                <span className="text-lg font-heading font-bold text-white">Synthetix<span className="text-peach">.AI</span></span>
              </div>
              <p className="text-sm text-text-secondary font-body leading-relaxed max-w-xs">
                The premier AI content generation platform for forward-thinking teams and creators.
              </p>
            </div>
            
            <div className="col-span-1">
              <h4 className="text-white font-heading font-bold mb-6 tracking-wide">Platform</h4>
              <ul className="space-y-4 font-body text-sm text-text-secondary">
                <li><Link to="/chat" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">AI Studio</Link></li>
                <li><Link to="/profile" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">Dashboard</Link></li>
                <li><a href="#features" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">Features</a></li>
              </ul>
            </div>
            
            <div className="col-span-1">
              <h4 className="text-white font-heading font-bold mb-6 tracking-wide">Account</h4>
              <ul className="space-y-4 font-body text-sm text-text-secondary">
                {isAuthenticated ? (
                  <>
                    <li><Link to="/profile" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">Settings</Link></li>
                  </>
                ) : (
                  <>
                    <li><Link to="/login" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">Sign In</Link></li>
                    <li><Link to="/register" className="hover:text-peach transition-colors inline-block hover:translate-x-1 duration-200">Create Account</Link></li>
                  </>
                )}
              </ul>
            </div>
          </div>
          
          <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row justify-between items-center text-xs font-body text-text-muted">
            <p>&copy; {new Date().getFullYear()} Synthetix AI. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <span className="hover:text-text-secondary cursor-pointer transition-colors">Privacy Policy</span>
              <span className="hover:text-text-secondary cursor-pointer transition-colors">Terms of Service</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

