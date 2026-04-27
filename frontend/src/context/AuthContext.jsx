import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'
import { userService } from '../services/userService'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      if (authService.isAuthenticated()) {
        // Initialize automatic token refresh
        authService.initializeAuth()
        
        const profile = await userService.getProfile()
        setUser(profile)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      authService.logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const response = await authService.login(email, password)
    const profile = await userService.getProfile()
    setUser(profile)
    return response
  }

  const register = async (data) => {
    const response = await authService.register(data)
    return response
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  const updateUser = (updatedData) => {
    setUser((prev) => ({ ...prev, ...updatedData }))
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
