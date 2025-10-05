import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Reporting API functions
export const reportingApi = {
  // Submit a new report
  async submitReport(reportData) {
    try {
      const response = await api.post('/api/reports/submit', reportData)
      return response.data
    } catch (error) {
      console.error('Error submitting report:', error)
      throw new Error(error.response?.data?.detail || 'Failed to submit report')
    }
  },

  // Upload images for reports
  async uploadImages(files) {
    try {
      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })
      
      const response = await api.post('/api/reports/upload-images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response.data
    } catch (error) {
      console.error('Error uploading images:', error)
      throw new Error(error.response?.data?.detail || 'Failed to upload images')
    }
  },

  // Get report status
  async getReportStatus(reportId) {
    try {
      const response = await api.get(`/api/reports/status/${reportId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching report status:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch report status')
    }
  },

  // Get report statistics
  async getReportStatistics() {
    try {
      const response = await api.get('/api/reports/statistics')
      return response.data
    } catch (error) {
      console.error('Error fetching statistics:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch statistics')
    }
  },

  // Get recent reports
  async getRecentReports(limit = 10) {
    try {
      const response = await api.get(`/api/reports/recent?limit=${limit}`)
      return response.data
    } catch (error) {
      console.error('Error fetching recent reports:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch recent reports')
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/api/health')
      return response.data
    } catch (error) {
      console.error('Error checking API health:', error)
      throw new Error('API is not available')
    }
  }
}

// AI Chat API functions
export const chatApi = {
  async sendMessage(message, chatHistory = [], selectedAreaData = null, sessionId = 'default') {
    try {
      const response = await api.post('/api/chat', {
        message,
        chatHistory,
        selectedAreaData,
        sessionId
      })
      return response.data
    } catch (error) {
      console.error('Error sending chat message:', error)
      throw new Error(error.response?.data?.detail || 'Failed to send message')
    }
  },

  async analyzeArea(areaData) {
    try {
      const response = await api.post('/api/analyze-area', {
        areaData
      })
      return response.data
    } catch (error) {
      console.error('Error analyzing area:', error)
      throw new Error(error.response?.data?.detail || 'Failed to analyze area')
    }
  }
}

// NASA API functions
export const nasaApi = {
  async getEarthImagery(lat, lng, dim = 0.1) {
    try {
      const response = await api.get(`/api/nasa/imagery?lat=${lat}&lng=${lng}&dim=${dim}`)
      return response.data
    } catch (error) {
      console.error('Error fetching NASA imagery:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch NASA imagery')
    }
  },

  async getEONETEvents(status = 'open', limit = 50) {
    try {
      const response = await api.get(`/api/nasa/eonet/events?status=${status}&limit=${limit}`)
      return response.data
    } catch (error) {
      console.error('Error fetching EONET events:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch EONET events')
    }
  },

  async getClimateData(lat, lng) {
    try {
      const response = await api.get(`/api/nasa/power/climate?lat=${lat}&lng=${lng}`)
      return response.data
    } catch (error) {
      console.error('Error fetching climate data:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch climate data')
    }
  }
}

export default {
  reportingApi,
  chatApi,
  nasaApi
}

