import { useNavigate } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import { useAuth } from '../../context/AuthContext'
import { Plus, Search, Trash2, User, LogOut, MessageSquare, X } from 'lucide-react'
import { format } from 'date-fns'
import { useState } from 'react'
import toast from 'react-hot-toast'

const Sidebar = ({ isOpen, onToggle }) => {
  const { sessions, loadSession, clearCurrentSession, deleteSession, deleteAllSessions } = useChat()
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')

  const handleNewChat = () => {
    clearCurrentSession()
    toast.success('New chat started')
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

  const filteredSessions = sessions.filter((session) =>
    session.title?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg hover:bg-gray-50"
      >
        <MessageSquare className="w-6 h-6 text-primary" />
      </button>
    )
  }

  return (
    <div className="w-80 bg-surface-dark text-white flex flex-col h-screen">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Chats</h2>
          <button onClick={onToggle} className="p-1 hover:bg-gray-700 rounded">
            <X className="w-5 h-5" />
          </button>
        </div>
        <button onClick={handleNewChat} className="w-full btn-primary flex items-center justify-center space-x-2">
          <Plus className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Search */}
      <div className="p-4 border-b border-gray-700">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filteredSessions.length === 0 ? (
          <p className="text-center text-gray-400 py-8">No chats yet</p>
        ) : (
          filteredSessions.map((session) => (
            <div
              key={session.id}
              onClick={() => loadSession(session.id)}
              className="p-3 bg-gray-700 rounded-lg hover:bg-gray-600 cursor-pointer group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{session.title || 'Untitled Chat'}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {format(new Date(session.updatedAt), 'MMM d, yyyy')}
                  </p>
                </div>
                <button
                  onClick={(e) => handleDeleteSession(e, session.id)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-500 rounded"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700 space-y-2">
        <button
          onClick={handleDeleteAll}
          className="w-full flex items-center space-x-2 px-4 py-2 text-red-400 hover:bg-gray-700 rounded-lg"
        >
          <Trash2 className="w-5 h-5" />
          <span>Delete All Chats</span>
        </button>
        <button
          onClick={() => navigate('/profile')}
          className="w-full flex items-center space-x-2 px-4 py-2 hover:bg-gray-700 rounded-lg"
        >
          <User className="w-5 h-5" />
          <span>{user?.username || 'Profile'}</span>
        </button>
        <button
          onClick={logout}
          className="w-full flex items-center space-x-2 px-4 py-2 hover:bg-gray-700 rounded-lg"
        >
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar
