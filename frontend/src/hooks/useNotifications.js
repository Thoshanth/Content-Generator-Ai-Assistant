import { useNotification } from '../context/NotificationContext'

export const useNotifications = () => {
  const {
    notifications,
    addNotification,
    removeNotification,
    clearAllNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo
  } = useNotification()

  // Enhanced notification methods with common use cases
  const notifySuccess = (message, title = 'Success') => {
    return showSuccess(title, message)
  }

  const notifyError = (message, title = 'Error') => {
    return showError(title, message, { duration: 8000 })
  }

  const notifyWarning = (message, title = 'Warning') => {
    return showWarning(title, message)
  }

  const notifyInfo = (message, title = 'Info') => {
    return showInfo(title, message)
  }

  // Specific notification types for common scenarios
  const notifyApiError = (error, customMessage = null) => {
    const message = customMessage || error?.response?.data?.message || error?.message || 'An unexpected error occurred'
    return showError('API Error', message, { duration: 10000 })
  }

  const notifyNetworkError = () => {
    return showError('Network Error', 'Please check your internet connection and try again', { 
      duration: 8000,
      persistent: false 
    })
  }

  const notifyAuthError = () => {
    return showError('Authentication Error', 'Please log in again to continue', { 
      duration: 10000,
      persistent: true 
    })
  }

  const notifyValidationError = (message) => {
    return showWarning('Validation Error', message, { duration: 6000 })
  }

  const notifyFileUploadSuccess = (filename) => {
    return showSuccess('Upload Complete', `${filename} has been uploaded successfully`)
  }

  const notifyFileUploadError = (filename, error) => {
    return showError('Upload Failed', `Failed to upload ${filename}: ${error}`, { duration: 8000 })
  }

  const notifyMessageSent = () => {
    return showSuccess('Message Sent', 'Your message has been sent successfully')
  }

  const notifyImageGenerated = () => {
    return showSuccess('Image Generated', 'Your image has been created successfully')
  }

  const notifyImageGenerationError = (error) => {
    return showError('Image Generation Failed', error || 'Failed to generate image', { duration: 8000 })
  }

  const notifyConnectionLost = () => {
    return showWarning('Connection Lost', 'Attempting to reconnect...', { 
      persistent: true,
      duration: 0 
    })
  }

  const notifyConnectionRestored = () => {
    return showSuccess('Connection Restored', 'You are back online')
  }

  const notifyFeatureComingSoon = (feature) => {
    return showInfo('Coming Soon', `${feature} will be available in a future update`)
  }

  const notifyMaintenance = () => {
    return showWarning('Maintenance Mode', 'Some features may be temporarily unavailable', { 
      persistent: true 
    })
  }

  return {
    // Basic notification methods
    notifications,
    addNotification,
    removeNotification,
    clearAllNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    
    // Enhanced methods
    notifySuccess,
    notifyError,
    notifyWarning,
    notifyInfo,
    
    // Specific use case methods
    notifyApiError,
    notifyNetworkError,
    notifyAuthError,
    notifyValidationError,
    notifyFileUploadSuccess,
    notifyFileUploadError,
    notifyMessageSent,
    notifyImageGenerated,
    notifyImageGenerationError,
    notifyConnectionLost,
    notifyConnectionRestored,
    notifyFeatureComingSoon,
    notifyMaintenance
  }
}

export default useNotifications