import api from './api'

export const userService = {
  async getProfile() {
    const response = await api.get('/user/profile')
    return response.data
  },

  async updateProfile(fullName, avatarUrl) {
    const response = await api.put('/user/profile', { fullName, avatarUrl })
    return response.data
  },

  async changePassword(oldPassword, newPassword) {
    const response = await api.put('/user/password', { oldPassword, newPassword })
    return response.data
  },

  async getStats() {
    const response = await api.get('/user/stats')
    return response.data
  },

  async deleteAccount() {
    const response = await api.delete('/user/account')
    return response.data
  },
}
