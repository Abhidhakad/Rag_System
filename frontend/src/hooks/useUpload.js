import { useState, useCallback } from 'react'
import { uploadDocument } from '../services/api'

export function useUpload() {
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const upload = useCallback(async (file) => {
    setUploading(true)
    setError(null)
    setResult(null)

    try {
      const res = await uploadDocument(file)
      if (res.success) {
        setResult(res.data)
      } else {
        setError(res.message || 'Upload failed')
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Upload failed'
      setError(msg)
    } finally {
      setUploading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  return { upload, uploading, result, error, reset }
}
