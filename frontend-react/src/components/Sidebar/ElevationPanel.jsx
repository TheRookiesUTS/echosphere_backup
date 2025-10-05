import { TrendingUp, Layers } from 'lucide-react'
import { useStore } from '../../store/useStore'

export default function ElevationPanel() {
  const { elevationProfile, showContours, toggleContours, setElevationProfile, mapCenter } = useStore()

  const generateElevationProfile = () => {
    // Generate mock elevation data around current map center
    const elevations = []
    const numPoints = 20
    
    for (let i = 0; i < numPoints; i++) {
      const distance = (i / (numPoints - 1)) * 0.1 // 0.1 degree span
      const elevation = Math.random() * 2000 + 100 // Random elevation 100-2100m
      elevations.push({
        distance: distance,
        elevation: elevation,
        lat: mapCenter[0] + (Math.random() - 0.5) * 0.02,
        lng: mapCenter[1] + (Math.random() - 0.5) * 0.02
      })
    }
    
    setElevationProfile(elevations)
  }

  return (
    <div>
      <h3 className="flex items-center gap-2 text-primary-400 font-semibold mb-4">
        <TrendingUp className="w-5 h-5" />
        Elevation Profile
      </h3>
      <div className="space-y-3">
        <div className="space-y-2">
          <button 
            onClick={generateElevationProfile}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-purple-500 rounded-lg font-semibold text-white text-sm transition-all hover:shadow-lg hover:shadow-purple-500/30"
          >
            <TrendingUp className="w-4 h-4" />
            Show Elevation
          </button>
          <button
            onClick={toggleContours}
            className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-semibold text-white text-sm transition-all ${
              showContours
                ? 'bg-gradient-to-r from-purple-600 to-purple-500 shadow-lg shadow-purple-500/30'
                : 'bg-white/10 border border-white/20 hover:bg-white/20'
            }`}
          >
            <Layers className="w-4 h-4" />
            Contour Lines
          </button>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-lg p-4 text-sm text-gray-400">
          {elevationProfile ? (
            <div>
              <h4 className="text-primary-400 font-semibold mb-3">Elevation Analysis</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span>Min Elevation:</span>
                  <span className="text-primary-400 font-semibold">
                    {Math.min(...elevationProfile.map(e => e.elevation)).toFixed(0)}m
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Max Elevation:</span>
                  <span className="text-primary-400 font-semibold">
                    {Math.max(...elevationProfile.map(e => e.elevation)).toFixed(0)}m
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Avg Elevation:</span>
                  <span className="text-primary-400 font-semibold">
                    {(elevationProfile.reduce((sum, e) => sum + e.elevation, 0) / elevationProfile.length).toFixed(0)}m
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Elevation Range:</span>
                  <span className="text-primary-400 font-semibold">
                    {(Math.max(...elevationProfile.map(e => e.elevation)) - Math.min(...elevationProfile.map(e => e.elevation))).toFixed(0)}m
                  </span>
                </div>
              </div>
              
              {/* Simple elevation chart */}
              <div className="mt-3">
                <div className="text-xs text-gray-400 mb-1">Elevation Profile:</div>
                <div className="h-16 bg-gray-800/50 rounded p-1">
                  <div className="h-full flex items-end gap-0.5">
                    {elevationProfile.slice(0, 10).map((point, index) => (
                      <div
                        key={index}
                        className="bg-gradient-to-t from-purple-600 to-purple-400 rounded-sm flex-1"
                        style={{
                          height: `${(point.elevation / Math.max(...elevationProfile.map(e => e.elevation))) * 100}%`
                        }}
                        title={`${point.elevation.toFixed(0)}m`}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-center">Click "Show Elevation" to analyze terrain</p>
          )}
        </div>
      </div>
    </div>
  )
}

