import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

export default function UploadZone({ onUpload, uploading, result, error, reset }) {
  const onDrop = useCallback(
    (accepted) => {
      if (accepted.length > 0) {
        onUpload(accepted[0])
      }
    },
    [onUpload]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: uploading,
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium text-gray-900">Upload a Document</h2>
        <p className="text-sm text-gray-500 mt-1">
          Upload a PDF to make it searchable. You can then ask questions in the Chat tab.
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400 bg-white'
        } ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <div className="text-3xl text-gray-400">
            {isDragActive ? '📄' : '📁'}
          </div>
          {isDragActive ? (
            <p className="text-blue-600 font-medium">Drop your PDF here</p>
          ) : (
            <>
              <p className="text-gray-600 font-medium">
                Drag & drop a PDF, or click to browse
              </p>
              <p className="text-xs text-gray-400">Only PDF files up to 10MB</p>
            </>
          )}
        </div>
      </div>

      {uploading && (
        <div className="flex items-center gap-2 text-blue-600">
          <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm">Processing document...</span>
        </div>
      )}

      {result && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-medium text-green-800">Document processed</p>
              <p className="text-xs text-green-600 mt-1">
                {result.filename} &middot; {result.chunk_count} chunks indexed
              </p>
            </div>
            <button onClick={reset} className="text-green-600 hover:text-green-800 text-sm">
              Clear
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start justify-between">
            <p className="text-sm text-red-700">{error}</p>
            <button onClick={reset} className="text-red-600 hover:text-red-800 text-sm">
              Dismiss
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
