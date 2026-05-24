import { useEffect, useRef } from 'react'

function CitationCard({ citation }) {
  return (
    <details className="mt-2 text-xs border border-gray-200 rounded bg-gray-50">
      <summary className="px-3 py-1.5 cursor-pointer text-gray-500 hover:text-gray-700 font-medium">
        Source (chunk {citation.chunk_index + 1}, relevance: {citation.score.toFixed(2)})
      </summary>
      <p className="px-3 py-2 text-gray-600 border-t border-gray-200">
        {citation.content.slice(0, 300)}
        {citation.content.length > 300 ? '...' : ''}
      </p>
    </details>
  )
}

export default function ChatMessages({ messages, loading, error }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  if (messages.length === 0 && !loading) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400">
        <div className="text-center space-y-2">
          <div className="text-4xl">💬</div>
          <p className="text-sm">Upload a document, then ask a question</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto space-y-4 pr-2">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] rounded-lg px-4 py-3 ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-200 text-gray-800'
            }`}
          >
            <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            {msg.citations && msg.citations.length > 0 && (
              <div className="mt-3 space-y-1">
                {msg.citations.map((c, j) => (
                  <CitationCard key={j} citation={c} />
                ))}
              </div>
            )}
          </div>
        </div>
      ))}

      {loading && (
        <div className="flex justify-start">
          <div className="bg-white border border-gray-200 rounded-lg px-4 py-3">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.1s]" />
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]" />
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
