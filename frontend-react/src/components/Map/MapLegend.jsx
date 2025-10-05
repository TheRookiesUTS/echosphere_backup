import { useStore } from '../../store/useStore'

export default function MapLegend() {
  const { layers, showContours } = useStore()

  return (
    <div className="absolute bottom-6 right-6 z-[1000] bg-black/80 backdrop-blur-md rounded-xl p-4 border border-white/20 max-w-xs shadow-lg">
      <h3 className="text-white font-semibold text-sm mb-3">Map Legend</h3>
      
      <div className="space-y-2 text-xs">
        {/* Heat Map Legend */}
        {layers.heat && (
          <div className="space-y-1">
            <div className="text-primary-400 font-medium">Heat Island Map</div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gradient-to-r from-blue-400 via-cyan-400 via-lime-400 via-yellow-400 to-red-400 rounded"></div>
              <span className="text-gray-300">Temperature intensity</span>
            </div>
          </div>
        )}

        {/* Air Quality Legend */}
        {layers.airQuality && (
          <div className="space-y-1">
            <div className="text-primary-400 font-medium">Air Quality</div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
              <span className="text-gray-300">Good (AQI &lt; 100)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <span className="text-gray-300">Moderate (AQI 100-150)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-400 rounded-full"></div>
              <span className="text-gray-300">Unhealthy (AQI &gt; 150)</span>
            </div>
          </div>
        )}

        {/* Flood Risk Legend */}
        {layers.flood && (
          <div className="space-y-1">
            <div className="text-primary-400 font-medium">Flood Risk</div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-blue-400"></div>
              <span className="text-gray-300">Low Risk</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-yellow-400"></div>
              <span className="text-gray-300">Medium Risk</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-400"></div>
              <span className="text-gray-300">High Risk</span>
            </div>
          </div>
        )}

        {/* Green Space Legend */}
        {layers.green && (
          <div className="space-y-1">
            <div className="text-primary-400 font-medium">Green Space</div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-400 rounded-full opacity-60"></div>
              <span className="text-gray-300">Vegetation coverage</span>
            </div>
          </div>
        )}

        {/* Contour Lines Legend */}
        {showContours && (
          <div className="space-y-1 pt-2 border-t border-white/20">
            <div className="text-primary-400 font-medium">Contour Lines</div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-green-600"></div>
              <span className="text-gray-300">Low elevation (100-300m)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-yellow-600"></div>
              <span className="text-gray-300">Medium elevation (300-500m)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-brown-600"></div>
              <span className="text-gray-300">High elevation (500m+)</span>
            </div>
          </div>
        )}

        {/* Area Selection Legend */}
        <div className="space-y-1 pt-2 border-t border-white/20">
          <div className="text-primary-400 font-medium">Selection</div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-400 rounded" style={{ borderStyle: 'dashed', opacity: 0.8 }}></div>
            <span className="text-gray-300">Temporary selection (while dragging)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-400 rounded" style={{ borderStyle: 'dashed', opacity: 0.6 }}></div>
            <span className="text-gray-300">Permanent selected area</span>
          </div>
        </div>
      </div>
    </div>
  )
}
