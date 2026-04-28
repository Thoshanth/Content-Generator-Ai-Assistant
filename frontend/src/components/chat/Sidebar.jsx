import { useNavigate } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import { useAuth } from '../../context/AuthContext'
import { Plus, Search, Trash2, User, LogOut, MessageSquare, X, LogIn, Home, RotateCcw, Clock, Calendar } from 'lucide-react'
import { format, isToday, isYesterday, isThisWeek, isThisMonth } from 'date-fns'
import { useState, useMemo, useEffect } from 'react'
import toast from 'react-hot-toast'
import ConfirmModal from '../ui/ConfirmModal'

const Sidebar = ({ isOpen, onToggle }) => {
  const { sessions, loadSessions, loadSession, clearCurrentSession, deleteSession, deleteAllSessions, currentSession, loading: chatLoading } = useChat()
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [confirmModal, setConfirmModal] = useState({ isOpen: false, type: '', sessionId: null, title: '', message: '' })

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
    setConfirmModal({
      isOpen: true,
      type: 'deleteAll',
      sessionId: null,
      title: 'Delete All Chat History',
      message: 'This will permanently delete all your chat sessions and cannot be undone. Are you sure you want to continue?'
    })
  }

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation()
    setConfirmModal({
      isOpen: true,
      type: 'deleteSession',
      sessionId: sessionId,
      title: 'Delete Chat Session',
      message: 'This will permanently delete this chat session and all its messages. This action cannot be undone.'
    })
  }

  const confirmAction = async () => {
    try {
      if (confirmModal.type === 'deleteAll') {
        await deleteAllSessions()
        toast.success('All chats deleted')
      } else if (confirmModal.type === 'deleteSession') {
        await deleteSession(confirmModal.sessionId)
        toast.success('Chat deleted')
      }
    } catch (error) {
      toast.error('Failed to delete')
    }
  }

  const safeSessions = Array.isArray(sessions) ? sessions : []
  
  // Debug logging
  useEffect(() => {
    console.log('Sidebar: Sessions updated:', safeSessions.length, safeSessions)
    console.log('Sidebar: isAuthenticated:', isAuthenticated)
    console.log('Sidebar: chatLoading:', chatLoading)
  }, [sessions, isAuthenticated, chatLoading])
  
  const filteredSessions = safeSessions.filter((session) =>
    session?.title?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  // Group sessions by date
  const groupedSessions = useMemo(() => {
    const groups = {
      today: [],
      yesterday: [],
      thisWeek: [],
      thisMonth: [],
      older: []
    }

    filteredSessions.forEach((session) => {
      try {
        const date = session.updatedAt?.seconds 
          ? new Date(session.updatedAt.seconds * 1000) 
          : new Date(session.updatedAt)
        
        if (isNaN(date.getTime())) {
          groups.older.push(session)
          return
        }

        if (isToday(date)) {
          groups.today.push(session)
        } else if (isYesterday(date)) {
          groups.yesterday.push(session)
        } else if (isThisWeek(date)) {
          groups.thisWeek.push(session)
        } else if (isThisMonth(date)) {
          groups.thisMonth.push(session)
        } else {
          groups.older.push(session)
        }
      } catch {
        groups.older.push(session)
      }
    })

    return groups
  }, [filteredSessions])

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed top-4 left-4 z-50 p-3 bg-surface-raised border border-border rounded-xl shadow-lg hover:bg-border transition-colors duration-200"
      >
        <MessageSquare className="w-5 h-5 text-peach" />
      </button>
    )
  }

  const SessionGroup = ({ title, sessions, icon: Icon }) => {
    if (sessions.length === 0) return null

    return (
      <div className="mb-6">
        <div className="px-3 pb-2 flex items-center space-x-2">
          <Icon className="w-3.5 h-3.5 text-text-muted" />
          <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-text-muted">{title}</h3>
          <span className="text-[10px] text-text-muted/50">({sessions.length})</span>
        </div>
        <div className="space-y-2">
          {sessions.map((session) => (
            <div
              key={session.id}
              onClick={() => loadSession(session.id)}
              className={`p-3 rounded-xl cursor-pointer group transition-all duration-200 border ${
                currentSession?.id === session.id 
                  ? 'bg-surface-raised border-peach/40 shadow-sm' 
                  : 'bg-transparent border-transparent hover:bg-surface-raised/50 hover:border-border/50'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className={`font-medium text-sm truncate ${
                    currentSession?.id === session.id ? 'text-peach' : 'text-text-primary group-hover:text-peach'
                  } transition-colors`}>
                    {session.title || 'Untitled Generation'}
                  </p>
                  <div className="flex items-center mt-1 space-x-2">
                    <span className={`w-1.5 h-1.5 rounded-full ${
                      currentSession?.id === session.id ? 'bg-peach' : 'bg-text-muted/30'
                    }`} />
                    <p className="text-[10px] text-text-muted uppercase tracking-wider">
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
                  className="p-2 text-text-muted hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                  title="Delete chat"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="w-[280px] bg-surface border-r border-border text-white flex flex-col h-screen flex-shrink-0">
        {/* Header */}
        <div className="p-5 border-b border-border">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5 text-peach" />
              <h2 className="text-xl font-bold text-white">Creo</h2>
              {isAuthenticated && (
                <button 
                  onClick={handleRefresh}
                  className={`p-1 text-text-muted hover:text-peach transition-colors ${chatLoading ? 'animate-spin text-peach' : ''}`}
                  title="Refresh history"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            <button 
              onClick={onToggle} 
              className="p-1.5 text-text-muted hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <button 
            onClick={handleNewChat} 
            className="w-full bg-peach hover:bg-peach/90 text-white py-3 px-4 rounded-xl font-medium transition-colors flex items-center justify-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </button>
        </div>

      {/* Search */}
      <div className="px-5 py-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            disabled={!isAuthenticated}
            className="w-full pl-10 pr-4 py-2.5 bg-surface-raised border border-border rounded-xl text-white placeholder-text-muted text-sm focus:outline-none focus:ring-2 focus:ring-peach/50 focus:border-peach/50 disabled:opacity-50 transition-all"
          />
        </div>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto px-3 pb-3 custom-scrollbar">
        {!isAuthenticated ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-4 px-6 py-10">
            <div className="w-16 h-16 bg-surface-raised rounded-2xl flex items-center justify-center border border-border">
              <MessageSquare className="w-8 h-8 text-text-muted" />
            </div>
            <div>
              <p className="font-bold text-white text-base">Secure Your History</p>
              <p className="text-text-secondary text-xs mt-2 leading-relaxed">Sign in to save your AI generations and access them anywhere.</p>
            </div>
            <button 
              onClick={() => navigate('/login')} 
              className="bg-peach hover:bg-peach/90 text-white text-sm w-full py-3 rounded-xl font-medium transition-colors"
            >
              Sign In to Creo
            </button>
          </div>
        ) : (
          <>
            {filteredSessions.length === 0 ? (
              <div className="text-center py-20 flex flex-col items-center">
                <div className="w-12 h-12 bg-surface-raised rounded-full flex items-center justify-center mb-4 opacity-20">
                  <MessageSquare className="w-6 h-6 text-text-muted" />
                </div>
                <p className="text-text-muted text-xs px-10 leading-relaxed">
                  {searchQuery ? 'No conversations match your search.' : 'Your chat history is empty. Start a new conversation above!'}
                </p>
              </div>
            ) : (
              <>
                <SessionGroup title="Today" sessions={groupedSessions.today} icon={Clock} />
                <SessionGroup title="Yesterday" sessions={groupedSessions.yesterday} icon={Calendar} />
                <SessionGroup title="This Week" sessions={groupedSessions.thisWeek} icon={Calendar} />
                <SessionGroup title="This Month" sessions={groupedSessions.thisMonth} icon={Calendar} />
                <SessionGroup title="Older" sessions={groupedSessions.older} icon={Calendar} />
              </>
            )}
          </>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-border bg-bg/50 backdrop-blur-sm space-y-2">
        {isAuthenticated && (
          <button
            onClick={handleDeleteAll}
            className="w-full flex items-center space-x-3 px-3 py-2.5 text-xs text-text-muted hover:text-red-500 hover:bg-red-500/5 rounded-xl transition-all group"
          >
            <Trash2 className="w-4 h-4 opacity-50 group-hover:opacity-100" />
            <span>Clear History</span>
          </button>
        )}
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => navigate('/')}
            className="flex items-center justify-center space-x-2 p-2.5 text-xs text-text-secondary hover:text-white hover:bg-surface-raised rounded-xl transition-all border border-transparent hover:border-border"
          >
            <Home className="w-4 h-4" />
            <span>Home</span>
          </button>
          <button
            onClick={() => navigate(isAuthenticated ? '/profile' : '/login')}
            className="flex items-center justify-center space-x-2 p-2.5 text-xs text-text-secondary hover:text-white hover:bg-surface-raised rounded-xl transition-all border border-transparent hover:border-border"
          >
            <User className="w-4 h-4" />
            <span className="truncate">{user?.username || 'Profile'}</span>
          </button>
        </div>
        {isAuthenticated ? (
          <button
            onClick={logout}
            className="w-full flex items-center justify-center space-x-2 p-3 text-xs font-medium text-text-muted hover:text-white hover:bg-red-500/10 rounded-xl transition-all border border-border/50 hover:border-red-500/30"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="w-full flex items-center justify-center space-x-2 p-3 text-sm font-medium text-peach bg-peach/10 hover:bg-peach/20 rounded-xl transition-all border border-peach/20"
          >
            <LogIn className="w-4 h-4" />
            <span>Login</span>
          </button>
        )}
      </div>
    </div>

    {/* Confirmation Modal */}
    <ConfirmModal
      isOpen={confirmModal.isOpen}
      onClose={() => setConfirmModal({ ...confirmModal, isOpen: false })}
      onConfirm={confirmAction}
      title={confirmModal.title}
      message={confirmModal.message}
      confirmText="Delete"
      cancelText="Cancel"
      type="danger"
    />
    </>
  )
}

export default Sidebar
