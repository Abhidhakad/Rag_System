import axios from 'axios'

const client = axios.create({
  baseURL: 'https://rag-system-duei.onrender.com/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
})

export async function uploadDocument(file) {
  const form = new FormData()
  form.append('file', file)

  const { data } = await client.post('/documents/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function queryDocuments(question) {
  const { data } = await client.post('/chat/query', { question })
  return data
}

export async function healthCheck() {
  const { data } = await client.get('/health')
  return data
}
