import api from './api'

export const authService = {
  async register(data) {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async login(email, password) {
    const response = await api.post('/auth/login', { email, password })
    if (response.data.accessToken && response.data.refreshToken) {
      localStorage.setItem('accessToken', response.data.accessToken)
      localStorage.setItem('refreshToken', response.data.refreshToken)
      
      // Set up automatic token refresh
      this.scheduleTokenRefresh()
    }
    return response.data
  },

  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await api.post('/auth/refresh', { refreshToken })
      
      if (response.data.accessToken) {
        localStorage.setItem('accessToken', response.data.accessToken)
        localStorage.setItem('refreshToken', response.data.refreshToken)
        
        // Schedule next refresh
        this.scheduleTokenRefresh()
        
        return response.data.accessToken
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      this.logout()
      throw error
    }
  },

  scheduleTokenRefresh() {
    // Clear any existing timeout
    if (this.refreshTimeout) {
      clearTimeout(this.refreshTimeout)
    }
    
    // Schedule refresh 1 minute before expiration (14 minutes)
    this.refreshTimeout = setTimeout(() => {
      this.refreshToken().catch(() => {
        // If refresh fails, logout user
        this.logout()
      })
    }, 14 * 60 * 1000) // 14 minutes
  },

  logout() {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    
    // Clear refresh timeout
    if (this.refreshTimeout) {
      clearTimeout(this.refreshTimeout)
    }
    
    window.location.href = '/login'
  },

  async validateToken() {
    try {
      const response = await api.get('/auth/validate')
      return response.data.valid
    } catch (error) {
      // If validation fails due to expired token, try to refresh
      if (error.response?.status === 401) {
        try {
          await this.refreshToken()
          // Retry validation with new token
          const retryResponse = await api.get('/auth/validate')
          return retryResponse.data.valid
        } catch (refreshError) {
          return false
        }
      }
      return false
    }
  },

  getAccessToken() {
    return localStorage.getItem('accessToken')
  },

  getRefreshToken() {
    return localStorage.getItem('refreshToken')
  },

  // Backward compatibility
  getToken() {
    return this.getAccessToken()
  },

  isAuthenticated() {
    return !!this.getAccessToken()
  },

  // Initialize token refresh on app start
  initializeAuth() {
    if (this.isAuthenticated()) {
      this.scheduleTokenRefresh()
    }
  }
}
