import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { api } from '../services/api'
import { shallow } from 'zustand/shallow'

const CITIES = {
  kualalumpur: { lat: 3.1390, lng: 101.6869, name: 'Kuala Lumpur' },
  jakarta: { lat: -6.2088, lng: 106.8456, name: 'Jakarta' },
  manila: { lat: 14.5995, lng: 120.9842, name: 'Manila' },
  bangkok: { lat: 13.7563, lng: 100.5018, name: 'Bangkok' },
  singapore: { lat: 1.3521, lng: 103.8198, name: 'Singapore' },
  hochiminh: { lat: 10.8231, lng: 106.6297, name: 'Ho Chi Minh City' },
  mumbai: { lat: 19.0760, lng: 72.8777, name: 'Mumbai' },
  tokyo: { lat: 35.6762, lng: 139.6503, name: 'Tokyo' }
}

// Only enable devtools in development
const withDevtools = import.meta.env.DEV ? devtools : (config) => config

export const useStore = create(
  withDevtools((set, get) => ({
    // Map state
    currentCity: 'kualalumpur',
    mapCenter: [3.1390, 101.6869],
    mapZoom: 12,
    baseLayer: 'satellite',
    
    // Data layers visibility
    layers: {
      heat: true,
      airQuality: true,
      flood: false,
      green: true,
      growth: false,
    },
    
    // Environmental metrics
    metrics: {
      heatValue: '--',
      heatTrend: '--',
      airValue: '--',
      airTrend: '--',
      waterValue: '--',
      waterTrend: '--',
      greenValue: '--',
      greenTrend: '--',
    },
    
    // Status panel data
    statusData: {
      heatIndex: 'Loading...',
      airQuality: 'Loading...',
      greenCoverage: 'Loading...',
    },
    
    // Area selection
    selectedArea: null,
    selectedAreaData: null,
    selectionMode: false,
    selectionBox: null,
    
    // Elevation data
    elevationProfile: null,
    contourLines: null,
    showContours: false,
    
    // AI Chat
    chatMessages: [
      {
        role: 'assistant',
        content: "Hello! I'm your AI Urban Planning Assistant. I can help you analyze environmental data, suggest planning strategies, and answer questions about urban resilience.",
        timestamp: new Date(),
      }
    ],
    sessionId: 'default',
    
    // Loading state
    loading: false,
    
    // Actions
    setLoading: (loading) => set({ loading }),
    
    setCurrentCity: (cityKey) => {
      const city = CITIES[cityKey]
      if (city) {
        set({
          currentCity: cityKey,
          mapCenter: [city.lat, city.lng],
          mapZoom: 12,
        })
        get().loadCityData(city.lat, city.lng)
      }
    },
    
    setMapCenter: (center) => set({ mapCenter: center }),
    setMapZoom: (zoom) => set({ mapZoom: zoom }),
    setBaseLayer: (layer) => set({ baseLayer: layer }),
    
    toggleLayer: (layerName) => set((state) => ({
      layers: {
        ...state.layers,
        [layerName]: !state.layers[layerName]
      }
    })),
    
    setMetrics: (metrics) => set({ metrics }),
    setStatusData: (statusData) => set({ statusData }),
    
    setSelectedArea: (area) => set({ selectedArea: area }),
    setSelectedAreaData: (data) => set({ selectedAreaData: data }),
    setSelectionMode: (mode) => set({ selectionMode: mode }),
    setSelectionBox: (box) => set({ selectionBox: box }),
    
    setElevationProfile: (profile) => set({ elevationProfile: profile }),
    toggleContours: () => set((state) => ({ showContours: !state.showContours })),
    
    addChatMessage: (message) => set((state) => ({
      chatMessages: [...state.chatMessages, { ...message, timestamp: new Date() }]
    })),
    
    clearChatHistory: () => set({
      chatMessages: [
        {
          role: 'assistant',
          content: "Hello! I'm your AI Urban Planning Assistant. How can I help you today?",
          timestamp: new Date(),
        }
      ]
    }),
    
    // Data loading functions
    initializeData: async () => {
      set({ loading: true })
      const state = get()
      const city = CITIES[state.currentCity]
      
      try {
        await state.loadCityData(city.lat, city.lng)
      } catch (error) {
        console.error('Error initializing data:', error)
        // Load mock data as fallback
        state.loadMockData()
      } finally {
        set({ loading: false })
      }
    },
    
    loadCityData: async (lat, lng) => {
      // Update metrics with random data (replace with real API calls)
      const heatValue = Math.floor(Math.random() * 10) + 25
      const airValue = Math.floor(Math.random() * 100) + 50
      const waterValue = Math.floor(Math.random() * 80) + 20
      const greenValue = Math.floor(Math.random() * 50) + 20
      
      const trends = ['improving', 'declining', 'stable']
      
      set({
        metrics: {
          heatValue: `${heatValue}°C`,
          heatTrend: trends[Math.floor(Math.random() * 3)],
          airValue: `${airValue} AQI`,
          airTrend: trends[Math.floor(Math.random() * 3)],
          waterValue: `${waterValue}%`,
          waterTrend: trends[Math.floor(Math.random() * 3)],
          greenValue: `${greenValue}%`,
          greenTrend: trends[Math.floor(Math.random() * 3)],
        },
        statusData: {
          heatIndex: `${heatValue}°C`,
          airQuality: `${airValue} AQI`,
          greenCoverage: `${greenValue}%`,
        }
      })
    },
    
    loadMockData: () => {
      const heatValue = Math.floor(Math.random() * 10) + 25
      const airValue = Math.floor(Math.random() * 100) + 50
      const waterValue = Math.floor(Math.random() * 80) + 20
      const greenValue = Math.floor(Math.random() * 50) + 20
      
      const trends = ['improving', 'declining', 'stable']
      
      set({
        metrics: {
          heatValue: `${heatValue}°C`,
          heatTrend: trends[Math.floor(Math.random() * 3)],
          airValue: `${airValue} AQI`,
          airTrend: trends[Math.floor(Math.random() * 3)],
          waterValue: `${waterValue}%`,
          waterTrend: trends[Math.floor(Math.random() * 3)],
          greenValue: `${greenValue}%`,
          greenTrend: trends[Math.floor(Math.random() * 3)],
        },
        statusData: {
          heatIndex: `${heatValue}°C`,
          airQuality: `${airValue} AQI`,
          greenCoverage: `${greenValue}%`,
        }
      })
    },
    
    // AI Chat actions
    sendChatMessage: async (message) => {
      const state = get()
      
      // Add user message
      state.addChatMessage({ role: 'user', content: message })
      
      // Add loading message
      const loadingId = Date.now()
      state.addChatMessage({ role: 'assistant', content: 'Analyzing location and thinking...', id: loadingId })
      
      try {
        let response
        
        // Check if user is asking about a specific location or has selected an area
        const isLocationQuery = message.toLowerCase().includes('location') || 
                               message.toLowerCase().includes('here') ||
                               message.toLowerCase().includes('this area') ||
                               message.toLowerCase().includes('current') ||
                               state.selectedArea ||
                               state.selectedAreaData
        
        if (isLocationQuery && state.mapCenter) {
          // Use location-aware chat with real NASA data
          console.log('Using location-aware chat with NASA data for:', state.mapCenter)
          response = await api.chatWithLocation(
            message, 
            state.mapCenter[0], // lat
            state.mapCenter[1], // lng
            state.sessionId
          )
        } else {
          // Use regular chat
          response = await api.chat({
            message,
            selectedAreaData: state.selectedAreaData,
            sessionId: state.sessionId,
          })
        }
        
        // Remove loading message and add response
        set((state) => ({
          chatMessages: [
            ...state.chatMessages.filter(msg => msg.id !== loadingId),
            { role: 'assistant', content: response.response, timestamp: new Date() }
          ]
        }))
      } catch (error) {
        console.error('Error sending chat message:', error)
        set((state) => ({
          chatMessages: [
            ...state.chatMessages.filter(msg => msg.id !== loadingId),
            { 
              role: 'assistant', 
              content: "Sorry, I'm having trouble connecting. Please try again.",
              timestamp: new Date()
            }
          ]
        }))
      }
    },
    
    analyzeSelectedArea: async () => {
      const state = get()
      
      if (!state.selectedAreaData || !state.selectedArea) {
        return
      }
      
      state.addChatMessage({
        role: 'user',
        content: `Analyzing selected area (${state.selectedArea?.area || 'N/A'} km²)...`
      })
      
      const loadingId = Date.now()
      state.addChatMessage({
        role: 'assistant',
        content: 'Performing comprehensive AI analysis... This may take up to 60 seconds as we fetch real environmental data and generate detailed insights.',
        id: loadingId
      })
      
      try {
        // Calculate center coordinates from bounds
        const bounds = state.selectedArea.bounds
        const centerLat = (bounds[0][0] + bounds[1][0]) / 2
        const centerLng = (bounds[0][1] + bounds[1][1]) / 2
        
        // Format data according to backend AreaData schema
        const areaData = {
          area: parseFloat(state.selectedArea.area),
          center: { lat: centerLat, lng: centerLng },
          bounds: {
            southwest: { lat: bounds[0][0], lng: bounds[0][1] },
            northeast: { lat: bounds[1][0], lng: bounds[1][1] }
          },
          heatIndex: state.selectedAreaData.heatIndex,
          airQuality: state.selectedAreaData.airQuality,
          greenCoverage: state.selectedAreaData.greenCoverage,
          waterStress: state.selectedAreaData.waterStress || 0,
          floodRisk: state.selectedAreaData.floodRisk,
          population: state.selectedAreaData.population,
          buildings: state.selectedAreaData.buildings || Math.floor(state.selectedAreaData.population / 10)
        }
        
        const response = await api.analyzeArea({ areaData })
        
        set((state) => ({
          chatMessages: [
            ...state.chatMessages.filter(msg => msg.id !== loadingId),
            {
              role: 'assistant',
              content: response.analysis,
              timestamp: new Date()
            }
          ]
        }))
      } catch (error) {
        console.error('Error analyzing area:', error)
        set((state) => ({
          chatMessages: [
            ...state.chatMessages.filter(msg => msg.id !== loadingId),
            {
              role: 'assistant',
              content: 'Sorry, analysis failed. Please try again.',
              timestamp: new Date()
            }
          ]
        }))
      }
    },
    
    // Get current city object
    getCurrentCity: () => {
      const state = get()
      return CITIES[state.currentCity]
    },
    
    getCities: () => CITIES,
  }))
)

