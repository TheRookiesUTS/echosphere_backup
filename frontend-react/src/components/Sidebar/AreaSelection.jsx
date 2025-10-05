import { Crop, X, Crosshair } from 'lucide-react'
import { useStore } from '../../store/useStore'

export default function AreaSelection() {
  const { selectedArea, selectedAreaData, selectionMode, setSelectionMode, setSelectedArea, setSelectedAreaData, setMapCenter, setMapZoom } = useStore()

  const toggleSelection = () => {
    setSelectionMode(!selectionMode)
  }

  const clearSelection = () => {
    setSelectedArea(null)
    setSelectedAreaData(null)
  }

  const focusOnArea = () => {
    if (selectedArea && selectedArea.bounds) {
      // Calculate center of the selected area
      const bounds = selectedArea.bounds
      const centerLat = bounds.reduce((sum, point) => sum + point[0], 0) / bounds.length
      const centerLng = bounds.reduce((sum, point) => sum + point[1], 0) / bounds.length
      
      setMapCenter([centerLat, centerLng])
      setMapZoom(15) // Zoom in closer when focusing on area
    }
  }

    return (
    <div>
      <h3 className="flex items-center gap-2 text-primary-400 font-semibold mb-4">
        <Crop className="w-5 h-5" />
        Area Selection
      </h3>
      <div className="space-y-3">
        <div className="space-y-2">
          <button
            onClick={toggleSelection}
            className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-semibold text-white transition-all ${
              selectionMode
                ? 'bg-gradient-to-r from-success-600 to-success-500 shadow-lg shadow-success-500/30'
                : 'bg-gradient-to-r from-yellow-600 to-yellow-500 hover:shadow-lg hover:shadow-yellow-500/30'
            }`}
          >
            {selectionMode ? (
              <>
                <X className="w-5 h-5" />
                <span className="text-sm">Cancel Selection</span>
              </>
            ) : (
              <>
                <Crop className="w-5 h-5" />
                <span className="text-sm">Select Area</span>
              </>
            )}
          </button>

          {selectedArea && (
            <>
              <button
                onClick={clearSelection}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white/10 border border-white/20 rounded-lg font-semibold text-white text-sm transition-all hover:bg-white/20"
              >
                <X className="w-4 h-4" />
                Clear Selection
              </button>
              <button
                onClick={focusOnArea}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white/10 border border-white/20 rounded-lg font-semibold text-white text-sm transition-all hover:bg-white/20"
              >
                <Crosshair className="w-4 h-4" />
                Focus on Area
              </button>
            </>
          )}
        </div>

        {/* Selection Instructions */}
        {selectionMode && (
          <div className="bg-blue-600/20 border border-blue-400/30 rounded-lg p-3 mb-3">
            <div className="flex items-center gap-2 text-blue-200 text-sm">
              <Crop className="w-4 h-4" />
              <span>Click and drag to create a selection box</span>
            </div>
            <div className="mt-1 text-xs text-blue-300">
              Hold mouse button and drag to select an area
            </div>
          </div>
        )}

        <div className="bg-white/5 border border-white/10 rounded-lg p-4">
          {selectedAreaData ? (
            <div>
              <h4 className="text-primary-400 font-semibold text-sm mb-3">Selected Area Analysis</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Area:</span>
                  <span className="text-primary-400 font-semibold">{selectedArea?.area || 'N/A'} km²</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Population:</span>
                  <span className="text-primary-400 font-semibold">{selectedAreaData.population?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Heat Index:</span>
                  <span className="text-primary-400 font-semibold">{selectedAreaData.heatIndex}°C</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Air Quality:</span>
                  <span className="text-primary-400 font-semibold">{selectedAreaData.airQuality} AQI</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Green:</span>
                  <span className="text-primary-400 font-semibold">{selectedAreaData.greenCoverage}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Flood Risk:</span>
                  <span className="text-primary-400 font-semibold">{selectedAreaData.floodRisk}</span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-400 text-sm text-center">
              Click "Select Area" to drag and select a region
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

