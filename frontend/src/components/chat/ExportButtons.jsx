import { useState } from 'react'
import { Copy, FileText, FileCode, Download, Check } from 'lucide-react'
import { exportContent, exportPdf } from '../../services/api'
import toast from 'react-hot-toast'

const ExportButtons = ({ content, contentType }) => {
  const [copied, setCopied] = useState(false)
  const [exporting, setExporting] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast.error('Failed to copy')
    }
  }

  const handleExportHTML = async () => {
    try {
      setExporting(true)
      const result = await exportContent(content, 'html', contentType)
      
      // Create and download HTML file
      const blob = new Blob([result.content], { type: 'text/html' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `content_${Date.now()}.html`
      a.click()
      URL.revokeObjectURL(url)
      
      toast.success('Exported as HTML!')
    } catch (error) {
      toast.error('Failed to export HTML')
    } finally {
      setExporting(false)
    }
  }

  const handleExportPDF = async () => {
    try {
      setExporting(true)
      const pdfBlob = await exportPdf(content, contentType, 'document')
      
      // Download PDF
      const url = URL.createObjectURL(pdfBlob)
      const a = document.createElement('a')
      a.href = url
      a.download = `content_${Date.now()}.pdf`
      a.click()
      URL.revokeObjectURL(url)
      
      toast.success('Exported as PDF!')
    } catch (error) {
      console.error('PDF export error:', error)
      toast.error('Failed to export PDF')
    } finally {
      setExporting(false)
    }
  }

  if (!content) return null

  return (
    <div className="flex items-center space-x-2 mt-2 font-body">
      <button
        onClick={handleCopy}
        className="inline-flex items-center space-x-1 px-3 py-1 text-xs bg-surface-raised border border-white/10 hover:border-peach/50 text-white hover:text-peach rounded-lg transition-colors"
        title="Copy to clipboard"
      >
        {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
        <span>{copied ? 'Copied!' : 'Copy'}</span>
      </button>

      <button
        onClick={handleExportHTML}
        disabled={exporting}
        className="inline-flex items-center space-x-1 px-3 py-1 text-xs bg-surface-raised border border-white/10 hover:border-peach/50 text-white hover:text-peach rounded-lg transition-colors disabled:opacity-50"
        title="Export as HTML"
      >
        <FileCode className="w-3 h-3" />
        <span>HTML</span>
      </button>

      <button
        onClick={handleExportPDF}
        disabled={exporting}
        className="inline-flex items-center space-x-1 px-3 py-1 text-xs bg-surface-raised border border-white/10 hover:border-peach/50 text-white hover:text-peach rounded-lg transition-colors disabled:opacity-50"
        title="Export as PDF"
      >
        <Download className="w-3 h-3" />
        <span>PDF</span>
      </button>

      {exporting && (
        <span className="text-xs text-text-secondary animate-pulse">Exporting...</span>
      )}
    </div>
  )
}

export default ExportButtons
