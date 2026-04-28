import { useNavigate } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import { useAuth } from '../../context/AuthContext'
import { Plus, Search, Trash2, User, LogOut, MessageSquare, X, LogIn, Home, RotateCcw } from 'lucide-react'
import { format } from 'date-fns'
import { useState } from 'react'
import toast from 'react-hot-toast'

const Sidebar = ({ isOpen, onToggle }) => {
  const { sessions, loadSessions, loadSession, clearCurrentSession, deleteSession, deleteAllSessions, currentSession, loading: chatLoading } = useChat()
  const { user, logout, isAuthenticated, loading: authLoading } = useAuth()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')

  const handleNewChat = () => {
    clearCurrentSession()
    toast.success('New chat started')
  }

  const handleRefresh = async () => {
    if (isAuthenticated) {
      try {
        await loadSessions()
        toast.success('History updated')
      } catch (error) {
        toast.error('Failed to refresh')
      }
    }
  }

  const handleDeleteAll = async () => {
    if (window.confirm('Delete all chat history? This cannot be undone.')) {
      try {
        await deleteAllSessions()
        toast.success('All chats deleted')
      } catch (error) {
        toast.error('Failed to delete chats')
      }
    }
  }

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation()
    if (window.confirm('Delete this chat?')) {
      try {
        await deleteSession(sessionId)
        toast.success('Chat deleted')
      } catch (error) {
        toast.error('Failed to delete chat')
      }
    }
  }

  const safeSessions = Array.isArray(sessions) ? sessions : []
  const filteredSessions = safeSessions.filter((session) =>
    session?.title?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed top-4 left-4 z-50 p-2 bg-surface-raised border border-border rounded-xl shadow-lg hover:bg-border transition-colors"
      >
        <MessageSquare className="w-6 h-6 text-peach" />
      </button>
    )
  }

  return (
    <div className="w-[280px] bg-surface border-r border-border text-white flex flex-col h-screen flex-shrink-0 transition-all duration-300">
      {/* Header */}
      <div className="p-5 border-b border-border">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center space-x-2">
            <h2 className="text-xl font-heading font-bold text-white">Chats</h2>
            {isAuthenticated && (
              <button 
                onClick={handleRefresh}
                className={`p-1 text-text-muted hover:text-peach transition-all ${chatLoading ? 'animate-spin text-peach' : ''}`}
                title="Refresh history"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
          <button onClick={onToggle} className="btn-icon p-1.5">
            <X className="w-5 h-5" />
          </button>
        </div>
        <button onClick={handleNewChat} className="w-full btn-primary py-3 flex items-center justify-center space-x-2 shadow-lg shadow-peach/10">
          <Plus className="w-5 h-5" />
          <span className="font-bold">New Chat</span>
        </button>
      </div>

      {/* Search */}
      <div className="px-5 py-4">
        <div className="relative group">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-muted group-focus-within:text-peach transition-colors" />
          <input
            type="text"
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            disabled={!isAuthenticated}
            className="w-full pl-10 pr-4 py-2.5 bg-surface-raised border border-border rounded-xl text-white placeholder-text-muted font-body text-sm focus:outline-none focus:ring-1 focus:ring-peach/50 disabled:opacity-50 transition-all"
          />
        </div>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-2 custom-scrollbar">
        {!isAuthenticated ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-4 px-6 py-10">
            <div className="w-16 h-16 bg-surface-raised rounded-3xl flex items-center justify-center border border-border shadow-inner">
              <MessageSquare className="w-8 h-8 text-text-muted" />
            </div>
            <div>
              <p className="font-heading font-bold text-white text-base">Secure Your History</p>
              <p className="font-body text-text-secondary text-xs mt-2 leading-relaxed">Sign in to save your AI generations and access them anywhere.</p>
            </div>
            <button onClick={() => navigate('/login')} className="btn-primary text-sm w-full py-3 rounded-2xl">
              Sign In to Synthetix
            </button>
          </div>
        ) : (
          <>
            <div className="px-3 pt-2 pb-1 flex items-center justify-between">
              <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-text-muted">Recent Activity</h3>
              {chatLoading && <span className="text-[10px] text-peach animate-pulse">Loading...</span>}
            </div>
            
            {filteredSessions.length === 0 ? (
              <div className="text-center py-20 flex flex-col items-center">
                <div className="w-12 h-12 bg-surface-raised rounded-full flex items-center justify-center mb-4 opacity-20">
                  <MessageSquare className="w-6 h-6 text-text-muted" />
                </div>
                <p className="font-body text-text-muted text-xs px-10 leading-relaxed">
                  {searchQuery ? 'No conversations match your search.' : 'Your chat history is empty. Start a new conversation above!'}
                </p>
              </div>
            ) : (
              filteredSessions.map((session) => (
                <div
                  key={session.id}
                  onClick={() => loadSession(session.id)}
                  className={`p-3.5 rounded-2xl cursor-pointer group transition-all duration-300 border ${
                    currentSession?.id === session.id 
                      ? 'bg-surface-raised border-peach/40 shadow-[0_8px_20px_rgba(249,168,168,0.08)]' 
                      : 'bg-transparent border-transparent hover:bg-surface-raised/50 hover:border-border/50'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <p className={`font-body font-semibold text-sm truncate ${
                        currentSession?.id === session.id ? 'text-peach' : 'text-text-primary group-hover:text-peach'
                      } transition-colors`}>
                        {session.title || 'Untitled Generation'}
                      </p>
                      <div className="flex items-center mt-1.5 space-x-2">
                        <span className={`w-1.5 h-1.5 rounded-full ${currentSession?.id === session.id ? 'bg-peach' : 'bg-text-muted/30'}`} />
                        <p className="text-[10px] font-body text-text-muted uppercase tracking-wider">
                          {(() => {
                            try {
                              const date = session.updatedAt?.seconds 
                                ? new Date(session.updatedAt.seconds * 1000) 
                                : new Date(session.updatedAt);
                              return isNaN(date.getTime()) ? 'Recently' : format(date, 'MMM d, h:mm a');
                            } catch {
                              return 'Recently';
                            }
                          })()}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={(e) => handleDeleteSession(e, session.id)}
                      className="p-2 text-text-muted hover:text-error hover:bg-error/10 rounded-xl transition-all opacity-0 group-hover:opacity-100"
                      title="Delete chat"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-border bg-bg/50 backdrop-blur-sm space-y-2">
        {isAuthenticated && (
          <button
            onClick={handleDeleteAll}
            className="w-full flex items-center space-x-3 px-3 py-2.5 text-xs font-body text-text-muted hover:text-error hover:bg-error/5 rounded-xl transition-all group"
          >
            <Trash2 className="w-4 h-4 opacity-50 group-hover:opacity-100" />
            <span>Clear History</span>
          </button>
        )}
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => navigate('/')}
            className="flex items-center justify-center space-x-2 p-2.5 text-xs font-body text-text-secondary hover:text-white hover:bg-surface-raised rounded-xl transition-all border border-transparent hover:border-border"
          >
            <Home className="w-4 h-4" />
            <span>Home</span>
          </button>
          <button
            onClick={() => navigate(isAuthenticated ? '/profile' : '/login')}
            className="flex items-center justify-center space-x-2 p-2.5 text-xs font-body text-text-secondary hover:text-white hover:bg-surface-raised rounded-xl transition-all border border-transparent hover:border-border"
          >
            <User className="w-4 h-4" />
            <span className="truncate">{user?.username || 'Profile'}</span>
          </button>
        </div>
        {isAuthenticated ? (
          <button
            onClick={logout}
            className="w-full flex items-center justify-center space-x-2 p-3 text-xs font-bold font-body text-text-muted hover:text-white hover:bg-error/20 rounded-xl transition-all border border-border/50 hover:border-error/30"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="w-full flex items-center justify-center space-x-2 p-3 text-sm font-bold font-body text-peach bg-peach/10 hover:bg-peach/20 rounded-xl transition-all border border-peach/20"
          >
            <LogIn className="w-4 h-4" />
            <span>Login</span>
          </button>
        )}
      </div>
    </div>
  )
}

export default Sidebar
