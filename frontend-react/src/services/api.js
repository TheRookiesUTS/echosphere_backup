import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
axiosInstance.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const api = {
  // AI Chat endpoints
  chat: async (data) => {
    return await axiosInstance.post('/api/chat', data)
  },

  chatWithLocation: async (message, lat, lng, sessionId = 'default') => {
    return await axiosInstance.post('/api/chat-with-location', null, {
      params: { message, lat, lng, session_id: sessionId },
      timeout: 60000 // 60 seconds for AI analysis with NASA data
    })
  },

  analyzeArea: async (data) => {
    return await axiosInstance.post('/api/analyze-area', data, {
      timeout: 60000 // 60 seconds for AI analysis
    })
  },

  // NASA endpoints
  getEarthImagery: async (lat, lng, dim = 0.1) => {
    return await axiosInstance.get('/api/nasa/imagery', {
      params: { lat, lng, dim }
    })
  },

  getEONETEvents: async (status = 'open', limit = 50) => {
    return await axiosInstance.get('/api/nasa/eonet/events', {
      params: { status, limit }
    })
  },

  getPowerClimateData: async (lat, lng) => {
    return await axiosInstance.get('/api/nasa/power/climate', {
      params: { lat, lng }
    })
  },

  // Health check
  healthCheck: async () => {
    return await axiosInstance.get('/api/health')
  },
}

export default axiosInstance

