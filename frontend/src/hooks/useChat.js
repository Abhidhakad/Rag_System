import { useState, useCallback, useRef } from 'react'
import { queryDocuments } from '../services/api'

export function useChat() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const pendingRef = useRef(false)

  const send = useCallback(async (question) => {
    if (pendingRef.current) return

    const userMsg = { role: 'user', content: question }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    setError(null)
    pendingRef.current = true

    try {
      const res = await queryDocuments(question)
      if (res.success) {
        const assistantMsg = {
          role: 'assistant',
          content: res.data.answer,
          citations: res.data.citations,
        }
        setMessages((prev) => [...prev, assistantMsg])
      } else {
        setError(res.message || 'No answer returned')
      }
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || err.message || 'Query failed'
      setError(msg)
    } finally {
      setLoading(false)
      pendingRef.current = false
    }
  }, [])

  const clear = useCallback(() => {
    setMessages([])
    setError(null)
  }, [])

  return { messages, send, loading, error, clear }
}
