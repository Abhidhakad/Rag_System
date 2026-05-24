import { useState } from 'react'

export default function ChatInput({ onSend, loading, onClear, hasMessages }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const q = input.trim()
    if (!q || loading) return
    setInput('')
    onSend(q)
  }

  return (
    <div className="border-t border-gray-200 pt-4 mt-4">
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={loading}
          className="flex-1 rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-blue-600 text-white rounded-lg px-5 py-2.5 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
        {hasMessages && (
          <button
            type="button"
            onClick={onClear}
            className="text-gray-400 hover:text-gray-600 text-sm px-2"
            title="Clear chat"
          >
            Clear
          </button>
        )}
      </form>
    </div>
  )
}
