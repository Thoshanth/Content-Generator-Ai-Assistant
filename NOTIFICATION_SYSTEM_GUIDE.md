# Notification System Guide

## Overview

The notification system provides a comprehensive way to display user feedback in the top-left corner of the application. It replaces or complements the existing react-hot-toast system with more customizable and feature-rich notifications.

## Features

- **Top-left positioning** - Notifications appear in the top-left corner as requested
- **Multiple notification types** - Success, Error, Warning, Info with distinct styling
- **Auto-dismiss** - Configurable duration with visual progress bar
- **Persistent notifications** - For critical messages that require user action
- **Smooth animations** - Enter/exit animations with proper transitions
- **Manual dismissal** - Click X button to close any notification
- **Bulk actions** - Clear all notifications at once
- **Responsive design** - Works on all screen sizes
- **Accessibility** - Proper ARIA labels and keyboard navigation

## Installation & Setup

The notification system is already integrated into the app. Here's what was added:

### 1. Context Provider (`NotificationContext.jsx`)
```jsx
import { NotificationProvider } from './context/NotificationContext'

// Wrap your app
<NotificationProvider>
  <App />
</NotificationProvider>
```

### 2. Notification Container (`NotificationContainer.jsx`)
```jsx
import NotificationContainer from './components/ui/NotificationContainer'

// Add to your main layout
<NotificationContainer />
```

### 3. Custom Hook (`useNotifications.js`)
```jsx
import { useNotifications } from './hooks/useNotifications'
```

## Usage

### Basic Usage

```jsx
import { useNotifications } from '../hooks/useNotifications'

const MyComponent = () => {
  const { notifySuccess, notifyError, notifyWarning, notifyInfo } = useNotifications()

  const handleSuccess = () => {
    notifySuccess('Operation completed!', 'Success')
  }

  const handleError = () => {
    notifyError('Something went wrong', 'Error')
  }

  return (
    <div>
      <button onClick={handleSuccess}>Show Success</button>
      <button onClick={handleError}>Show Error</button>
    </div>
  )
}
```

### Advanced Usage

```jsx
const { addNotification, removeNotification } = useNotifications()

// Custom notification with all options
const notificationId = addNotification({
  type: 'warning',
  title: 'Custom Warning',
  message: 'This is a custom notification',
  duration: 10000, // 10 seconds
  persistent: false // Auto-dismiss after duration
})

// Remove specific notification
removeNotification(notificationId)
```

### Application-Specific Methods

The hook provides pre-configured methods for common scenarios:

```jsx
const {
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
} = useNotifications()

// Usage examples
notifyApiError(error) // Handles API error formatting
notifyAuthError() // Pre-configured auth error message
notifyFileUploadSuccess('document.pdf') // File-specific success
notifyConnectionLost() // Persistent connection warning
```

## Notification Types

### 1. Success Notifications
- **Color**: Green theme
- **Icon**: Check circle
- **Duration**: 5 seconds (default)
- **Use for**: Successful operations, confirmations

### 2. Error Notifications
- **Color**: Red theme
- **Icon**: X circle
- **Duration**: 8 seconds (longer for errors)
- **Use for**: Failed operations, critical errors

### 3. Warning Notifications
- **Color**: Yellow theme
- **Icon**: Alert triangle
- **Duration**: 5 seconds (default)
- **Use for**: Cautions, non-critical issues

### 4. Info Notifications
- **Color**: Blue theme
- **Icon**: Info circle
- **Duration**: 5 seconds (default)
- **Use for**: General information, tips

## Configuration Options

### Notification Object Structure
```jsx
{
  id: 'auto-generated', // Unique identifier
  type: 'success|error|warning|info', // Notification type
  title: 'string', // Main heading (optional)
  message: 'string', // Body text (optional)
  duration: 5000, // Auto-dismiss time in ms
  persistent: false // If true, won't auto-dismiss
}
```

### Duration Guidelines
- **Success**: 5 seconds (default)
- **Error**: 8-10 seconds (longer for user to read)
- **Warning**: 5-6 seconds
- **Info**: 5 seconds
- **Persistent**: 0 or very high value

## Integration Examples

### 1. API Error Handling
```jsx
try {
  const response = await api.call()
  notifySuccess('Data saved successfully')
} catch (error) {
  notifyApiError(error)
}
```

### 2. Form Validation
```jsx
const handleSubmit = (data) => {
  if (!data.email) {
    notifyValidationError('Email is required')
    return
  }
  
  if (!isValidEmail(data.email)) {
    notifyValidationError('Please enter a valid email address')
    return
  }
  
  // Process form...
}
```

### 3. File Upload
```jsx
const handleFileUpload = async (file) => {
  try {
    await uploadFile(file)
    notifyFileUploadSuccess(file.name)
  } catch (error) {
    notifyFileUploadError(file.name, error.message)
  }
}
```

### 4. Connection Status
```jsx
useEffect(() => {
  const handleOnline = () => notifyConnectionRestored()
  const handleOffline = () => notifyConnectionLost()
  
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
  
  return () => {
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
  }
}, [])
```

## Styling & Customization

### CSS Classes Used
- `.fixed.top-4.left-4` - Container positioning
- `.bg-green-50.border-green-400` - Success styling
- `.bg-red-50.border-red-400` - Error styling
- `.bg-yellow-50.border-yellow-400` - Warning styling
- `.bg-blue-50.border-blue-400` - Info styling

### Animation Classes
- `.animate-shrink` - Progress bar animation
- Tailwind transitions for enter/exit animations

### Customizing Appearance
To modify notification appearance, update the `getNotificationStyles()` function in `NotificationItem.jsx`:

```jsx
const typeStyles = {
  success: "bg-green-50 border-green-400 text-green-800",
  error: "bg-red-50 border-red-400 text-red-800",
  warning: "bg-yellow-50 border-yellow-400 text-yellow-800",
  info: "bg-blue-50 border-blue-400 text-blue-800"
}
```

## Demo Component

A demo component (`NotificationDemo.jsx`) is available to test all notification types. Access it through the "Notifications" button in the ChatPage header.

## Best Practices

### 1. Message Content
- **Title**: Keep short and descriptive (2-4 words)
- **Message**: Provide clear, actionable information
- **Tone**: Match the notification type (success = positive, error = helpful)

### 2. Timing
- Use appropriate durations for content length
- Make errors persistent for critical issues
- Don't overwhelm users with too many notifications

### 3. User Experience
- Group related notifications when possible
- Provide clear next steps in error messages
- Use consistent language across the application

### 4. Performance
- Clean up notifications to prevent memory leaks
- Limit the number of simultaneous notifications
- Use the bulk clear function when appropriate

## Migration from react-hot-toast

To migrate existing toast notifications:

```jsx
// Old way
import toast from 'react-hot-toast'
toast.success('Success message')
toast.error('Error message')

// New way
import { useNotifications } from '../hooks/useNotifications'
const { notifySuccess, notifyError } = useNotifications()
notifySuccess('Success message', 'Success')
notifyError('Error message', 'Error')
```

## Troubleshooting

### Notifications not appearing
1. Ensure `NotificationProvider` wraps your app
2. Check that `NotificationContainer` is rendered
3. Verify the hook is used within the provider

### Styling issues
1. Ensure Tailwind CSS is properly configured
2. Check that custom animations are defined in CSS
3. Verify z-index values don't conflict

### Performance issues
1. Use `clearAllNotifications()` to clean up
2. Avoid creating too many persistent notifications
3. Monitor notification count in development

## Future Enhancements

Potential improvements for the notification system:

1. **Sound notifications** - Audio feedback for different types
2. **Notification history** - View past notifications
3. **User preferences** - Customize duration and position
4. **Rich content** - Support for buttons and links in notifications
5. **Notification groups** - Collapse similar notifications
6. **Push notifications** - Browser notification API integration

## Support

For issues or questions about the notification system:
1. Check this documentation
2. Review the demo component for examples
3. Examine existing usage in ChatPage.jsx
4. Test with the NotificationDemo component