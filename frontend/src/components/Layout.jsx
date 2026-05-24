import { useState } from 'react'
import UploadZone from './UploadZone'
import ChatMessages from './ChatMessages'
import ChatInput from './ChatInput'
import { useUpload } from '../hooks/useUpload'
import { useChat } from '../hooks/useChat'

export default function Layout() {
  const [activeTab, setActiveTab] = useState('chat')
  const upload = useUpload()
  const chat = useChat()

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-900">RAG Document Q&A</h1>
          <nav className="flex gap-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Chat
            </button>
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'upload'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Upload
            </button>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full p-6">
        {activeTab === 'upload' && (
          <UploadZone
            onUpload={upload.upload}
            uploading={upload.uploading}
            result={upload.result}
            error={upload.error}
            reset={upload.reset}
          />
        )}

        {activeTab === 'chat' && (
          <div className="flex flex-col h-[calc(100vh-140px)]">
            <ChatMessages
              messages={chat.messages}
              loading={chat.loading}
              error={chat.error}
            />
            <ChatInput
              onSend={chat.send}
              loading={chat.loading}
              onClear={chat.clear}
              hasMessages={chat.messages.length > 0}
            />
          </div>
        )}
      </main>
    </div>
  )
}
