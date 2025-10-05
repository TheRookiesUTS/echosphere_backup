import { Mountain, Satellite, Map as MapIcon, Route } from 'lucide-react'
import { useStore } from '../../store/useStore'

const baseLayers = [
  { key: 'satellite', icon: Satellite, label: 'Satellite View' },
  { key: 'topographic', icon: Mountain, label: 'Topographic' },
  { key: 'terrain', icon: Mountain, label: 'Terrain' },
  { key: 'streets', icon: Route, label: 'Street Map' },
]

export default function MapLayers() {
  const { baseLayer, setBaseLayer } = useStore()

  return (
    <div>
      <h3 className="flex items-center gap-2 text-primary-400 font-semibold mb-4">
        <Mountain className="w-5 h-5" />
        Map Layers
      </h3>
      <div className="space-y-2">
        {baseLayers.map((layer) => (
          <label
            key={layer.key}
            className="flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all hover:bg-white/10 border border-transparent hover:border-white/20"
          >
            <input
              type="radio"
              name="baseLayer"
              checked={baseLayer === layer.key}
              onChange={() => setBaseLayer(layer.key)}
              className="w-5 h-5 text-primary-400 focus:ring-2 focus:ring-primary-400 cursor-pointer"
            />
            <layer.icon className="w-5 h-5 text-primary-400" />
            <span className="text-white text-sm">{layer.label}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

