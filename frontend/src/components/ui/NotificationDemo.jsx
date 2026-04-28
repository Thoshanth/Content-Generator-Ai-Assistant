import React from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import { motion } from 'framer-motion'
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Info, 
  Wifi, 
  WifiOff, 
  Upload, 
  Image as ImageIcon,
  MessageSquare,
  Settings
} from 'lucide-react'

const NotificationDemo = ({ onClose }) => {
  const {
    notifySuccess,
    notifyError,
    notifyWarning,
    notifyInfo,
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
    notifyMaintenance,
    clearAllNotifications
  } = useNotifications()

  const demoNotifications = [
    {
      category: 'Basic Types',
      items: [
        {
          name: 'Success',
          icon: CheckCircle,
          color: 'text-green-500',
          action: () => notifySuccess('Operation completed successfully!', 'Success')
        },
        {
          name: 'Error',
          icon: XCircle,
          color: 'text-red-500',
          action: () => notifyError('Something went wrong', 'Error')
        },
        {
          name: 'Warning',
          icon: AlertTriangle,
          color: 'text-yellow-500',
          action: () => notifyWarning('Please check your input', 'Warning')
        },
        {
          name: 'Info',
          icon: Info,
          color: 'text-blue-500',
          action: () => notifyInfo('Here is some useful information', 'Information')
        }
      ]
    },
    {
      category: 'Application Specific',
      items: [
        {
          name: 'Message Sent',
          icon: MessageSquare,
          color: 'text-green-500',
          action: () => notifyMessageSent()
        },
        {
          name: 'Image Generated',
          icon: ImageIcon,
          color: 'text-purple-500',
          action: () => notifyImageGenerated()
        },
        {
          name: 'Upload Success',
          icon: Upload,
          color: 'text-green-500',
          action: () => notifyFileUploadSuccess('document.pdf')
        },
        {
          name: 'Feature Coming Soon',
          icon: Settings,
          color: 'text-blue-500',
          action: () => notifyFeatureComingSoon('Advanced Analytics')
        }
      ]
    },
    {
      category: 'Error Scenarios',
      items: [
        {
          name: 'API Error',
          icon: XCircle,
          color: 'text-red-500',
          action: () => notifyApiError({ message: 'Server returned 500 error' })
        },
        {
          name: 'Network Error',
          icon: WifiOff,
          color: 'text-red-500',
          action: () => notifyNetworkError()
        },
        {
          name: 'Auth Error',
          icon: XCircle,
          color: 'text-red-500',
          action: () => notifyAuthError()
        },
        {
          name: 'Validation Error',
          icon: AlertTriangle,
          color: 'text-yellow-500',
          action: () => notifyValidationError('Email format is invalid')
        }
      ]
    },
    {
      category: 'Connection Status',
      items: [
        {
          name: 'Connection Lost',
          icon: WifiOff,
          color: 'text-yellow-500',
          action: () => notifyConnectionLost()
        },
        {
          name: 'Connection Restored',
          icon: Wifi,
          color: 'text-green-500',
          action: () => notifyConnectionRestored()
        },
        {
          name: 'Maintenance Mode',
          icon: Settings,
          color: 'text-yellow-500',
          action: () => notifyMaintenance()
        }
      ]
    }
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-surface rounded-2xl border border-border p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto custom-scrollbar"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-heading font-bold text-white">
            Notification System Demo
          </h2>
          <div className="flex items-center space-x-3">
            <button
              onClick={clearAllNotifications}
              className="btn-secondary text-sm"
            >
              Clear All
            </button>
            <button
              onClick={onClose}
              className="btn-ghost text-sm"
            >
              Close
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {demoNotifications.map((category) => (
            <div key={category.category} className="space-y-4">
              <h3 className="text-lg font-semibold text-peach border-b border-border pb-2">
                {category.category}
              </h3>
              <div className="grid grid-cols-1 gap-2">
                {category.items.map((item) => {
                  const IconComponent = item.icon
                  return (
                    <button
                      key={item.name}
                      onClick={item.action}
                      className="flex items-center space-x-3 p-3 bg-surface-raised hover:bg-border rounded-xl transition-all duration-200 text-left"
                    >
                      <IconComponent className={`w-5 h-5 ${item.color}`} />
                      <span className="text-text-primary font-medium">
                        {item.name}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-surface-raised rounded-xl">
          <h4 className="font-semibold text-white mb-2">Usage Instructions:</h4>
          <ul className="text-sm text-text-secondary space-y-1">
            <li>• Notifications appear in the top-left corner</li>
            <li>• Click any button above to trigger a notification</li>
            <li>• Notifications auto-dismiss after their duration (except persistent ones)</li>
            <li>• Click the X button on any notification to dismiss it manually</li>
            <li>• Use "Clear All" to remove all notifications at once</li>
          </ul>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default NotificationDemo