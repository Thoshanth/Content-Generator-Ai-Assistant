import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { userService } from '../services/userService'
import toast from 'react-hot-toast'
import { User, Mail, Calendar, MessageSquare, ArrowLeft, Trash2, Eye, EyeOff, LogOut } from 'lucide-react'

const ProfilePage = () => {
  const { user, updateUser, logout } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    fullName: user?.fullName || '',
    avatarUrl: user?.avatarUrl || '',
  })
  const [passwordData, setPasswordData] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  })
  const [showPasswords, setShowPasswords] = useState({
    old: false,
    new: false,
    confirm: false,
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await userService.getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const handleUpdateProfile = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await userService.updateProfile(formData.fullName, formData.avatarUrl)
      updateUser(formData)
      toast.success('Profile updated successfully')
      setEditing(false)
    } catch (error) {
      toast.error('Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const handleChangePassword = async (e) => {
    e.preventDefault()

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    if (passwordData.newPassword.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }

    setLoading(true)

    try {
      await userService.changePassword(passwordData.oldPassword, passwordData.newPassword)
      toast.success('Password changed successfully')
      setPasswordData({ oldPassword: '', newPassword: '', confirmPassword: '' })
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to change password')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteAccount = async () => {
    if (window.confirm('Are you sure you want to delete your account? This cannot be undone.')) {
      try {
        await userService.deleteAccount()
        toast.success('Account deleted')
        logout()
      } catch (error) {
        toast.error('Failed to delete account')
      }
    }
  }

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }))
  }

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <div className="bg-bg border-b border-border">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/chat')}
            className="flex items-center space-x-2 text-text-secondary hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-body text-sm font-medium">Back to Chat</span>
          </button>
          <button
            onClick={logout}
            className="flex items-center space-x-2 text-text-secondary hover:text-peach transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span className="font-body text-sm font-medium">Logout</span>
          </button>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {/* Profile Card */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-heading font-bold text-white">Profile</h2>
            {!editing && (
              <button onClick={() => setEditing(true)} className="btn-secondary text-sm">
                Edit Profile
              </button>
            )}
          </div>

          {editing ? (
            <form onSubmit={handleUpdateProfile} className="space-y-5">
              <div>
                <label className="block text-sm font-body font-medium text-white mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-body font-medium text-white mb-2">
                  Avatar URL
                </label>
                <input
                  type="url"
                  value={formData.avatarUrl}
                  onChange={(e) => setFormData({ ...formData, avatarUrl: e.target.value })}
                  className="input-field"
                  placeholder="https://example.com/avatar.jpg"
                />
              </div>

              <div className="flex space-x-4 pt-2">
                <button type="submit" disabled={loading} className="btn-primary">
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditing(false)}
                  className="btn-ghost"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row items-center md:items-start space-y-4 md:space-y-0 md:space-x-6">
                <div className="w-24 h-24 bg-surface-raised rounded-full flex items-center justify-center border border-border shadow-sm">
                  {user?.avatarUrl ? (
                    <img src={user.avatarUrl} alt="Avatar" className="w-full h-full rounded-full object-cover" />
                  ) : (
                    <User className="w-12 h-12 text-peach" />
                  )}
                </div>
                <div className="text-center md:text-left mt-2">
                  <h3 className="text-2xl font-heading font-bold text-white">
                    {user?.fullName || 'No name set'}
                  </h3>
                  <p className="text-text-secondary font-body mt-1">@{user?.username}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-border">
                <div className="flex items-center space-x-4 bg-surface-raised p-4 rounded-xl">
                  <div className="p-2 bg-bg rounded-lg border border-border">
                    <Mail className="w-5 h-5 text-peach" />
                  </div>
                  <div>
                    <p className="text-sm font-body text-text-secondary">Email</p>
                    <p className="font-medium font-body text-white">{user?.email}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-surface-raised p-4 rounded-xl">
                  <div className="p-2 bg-bg rounded-lg border border-border">
                    <Calendar className="w-5 h-5 text-peach" />
                  </div>
                  <div>
                    <p className="text-sm font-body text-text-secondary">Member Since</p>
                    <p className="font-medium font-body text-white">
                      {user?.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Stats Card */}
        {stats && (
          <div className="card">
            <h2 className="text-xl font-heading font-bold text-white mb-6">Usage Statistics</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div className="text-center p-6 bg-surface-raised rounded-xl border border-border">
                <div className="inline-flex p-3 bg-bg rounded-full border border-border mb-3">
                  <MessageSquare className="w-6 h-6 text-peach" />
                </div>
                <p className="text-3xl font-heading font-bold text-white mb-1">{stats.totalSessions}</p>
                <p className="text-sm font-body text-text-secondary">Total Sessions</p>
              </div>
              <div className="text-center p-6 bg-surface-raised rounded-xl border border-border">
                <div className="inline-flex p-3 bg-bg rounded-full border border-border mb-3">
                  <MessageSquare className="w-6 h-6 text-peach" />
                </div>
                <p className="text-3xl font-heading font-bold text-white mb-1">{stats.userMessages}</p>
                <p className="text-sm font-body text-text-secondary">Messages Sent</p>
              </div>
              <div className="text-center p-6 bg-surface-raised rounded-xl border border-border">
                <div className="inline-flex p-3 bg-bg rounded-full border border-border mb-3">
                  <MessageSquare className="w-6 h-6 text-peach" />
                </div>
                <p className="text-3xl font-heading font-bold text-white mb-1">{stats.dailyMessageCount}/10</p>
                <p className="text-sm font-body text-text-secondary">Today's Usage</p>
              </div>
            </div>
          </div>
        )}

        {/* Change Password Card */}
        <div className="card">
          <h2 className="text-xl font-heading font-bold text-white mb-6">Change Password</h2>
          <form onSubmit={handleChangePassword} className="space-y-5 max-w-md">
            <div>
              <label className="block text-sm font-body font-medium text-white mb-2">
                Current Password
              </label>
              <div className="relative">
                <input
                  type={showPasswords.old ? 'text' : 'password'}
                  value={passwordData.oldPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, oldPassword: e.target.value })}
                  className="input-field pr-12"
                  required
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('old')}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-white transition-colors"
                >
                  {showPasswords.old ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-body font-medium text-white mb-2">
                New Password
              </label>
              <div className="relative">
                <input
                  type={showPasswords.new ? 'text' : 'password'}
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                  className="input-field pr-12"
                  required
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('new')}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-white transition-colors"
                >
                  {showPasswords.new ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-body font-medium text-white mb-2">
                Confirm New Password
              </label>
              <div className="relative">
                <input
                  type={showPasswords.confirm ? 'text' : 'password'}
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                  className="input-field pr-12"
                  required
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('confirm')}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-white transition-colors"
                >
                  {showPasswords.confirm ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="pt-2">
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Changing...' : 'Change Password'}
              </button>
            </div>
          </form>
        </div>

        {/* Danger Zone */}
        <div className="card border-error/30 bg-error/5">
          <h2 className="text-xl font-heading font-bold text-error mb-4">Danger Zone</h2>
          <p className="text-text-secondary font-body mb-6">
            Once you delete your account, there is no going back. Please be certain.
          </p>
          <button
            onClick={handleDeleteAccount}
            className="btn-danger inline-flex items-center space-x-2"
          >
            <Trash2 className="w-5 h-5" />
            <span>Delete Account</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
