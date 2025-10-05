import { useStore } from '../../store/useStore'
import { useEffect, useState } from 'react'

export default function StatusPanel() {
  const { statusData, selectedAreaData, layers } = useStore()
  const [currentData, setCurrentData] = useState(statusData)

  useEffect(() => {
    // If an area is selected, show area-specific data
    if (selectedAreaData) {
      setCurrentData({
        heatIndex: `${selectedAreaData.heatIndex}°C`,
        airQuality: `${selectedAreaData.airQuality} AQI`,
        greenCoverage: `${selectedAreaData.greenCoverage}%`
      })
    } else {
      // Otherwise show general status data
      setCurrentData(statusData)
    }
  }, [statusData, selectedAreaData])

  const getAirQualityColor = (value) => {
    const aqi = parseInt(value)
    if (aqi > 150) return 'text-red-400'
    if (aqi > 100) return 'text-yellow-400'
    return 'text-green-400'
  }

  const getHeatIndexColor = (value) => {
    const temp = parseInt(value)
    if (temp > 35) return 'text-red-400'
    if (temp > 30) return 'text-orange-400'
    return 'text-blue-400'
  }

  const getGreenCoverageColor = (value) => {
    const coverage = parseInt(value)
    if (coverage > 60) return 'text-green-400'
    if (coverage > 30) return 'text-yellow-400'
    return 'text-red-400'
  }

  return (
    <div className="absolute top-6 left-6 z-[1000] bg-black/80 backdrop-blur-md rounded-xl p-4 border border-white/20 shadow-lg">
      <div className="space-y-2 text-sm">
        <div className="flex items-center justify-between gap-8">
          <span className="text-gray-400">Heat Index:</span>
          <span className={`font-semibold ${getHeatIndexColor(currentData.heatIndex)}`}>
            {currentData.heatIndex}
          </span>
        </div>
        <div className="flex items-center justify-between gap-8">
          <span className="text-gray-400">Air Quality:</span>
          <span className={`font-semibold ${getAirQualityColor(currentData.airQuality)}`}>
            {currentData.airQuality}
          </span>
        </div>
        <div className="flex items-center justify-between gap-8">
          <span className="text-gray-400">Green Coverage:</span>
          <span className={`font-semibold ${getGreenCoverageColor(currentData.greenCoverage)}`}>
            {currentData.greenCoverage}
          </span>
        </div>
        
        {/* Show active layers indicator */}
        <div className="mt-3 pt-2 border-t border-white/20">
          <div className="text-xs text-gray-400 mb-1">Active Layers:</div>
          <div className="flex flex-wrap gap-1">
            {Object.entries(layers).map(([key, active]) => (
              active && (
                <span
                  key={key}
                  className="px-2 py-1 bg-primary-600/50 rounded text-xs text-primary-200"
                >
                  {key === 'airQuality' ? 'Air Quality' : 
                   key === 'heat' ? 'Heat Map' :
                   key === 'flood' ? 'Flood Risk' :
                   key === 'green' ? 'Green Space' :
                   key === 'growth' ? 'Urban Growth' : key}
                </span>
              )
            ))}
          </div>
        </div>

        {/* Show selection status */}
        {selectedAreaData && (
          <div className="mt-3 pt-2 border-t border-white/20">
            <div className="text-xs text-green-400 font-semibold">
              ✓ Area Selected ({selectedAreaData.population?.toLocaleString()} people)
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

