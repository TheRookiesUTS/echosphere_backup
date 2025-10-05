import { Layers, Thermometer, Wind, Droplets, Trees, Building } from 'lucide-react'
import { useStore } from '../../store/useStore'

const layerConfig = [
  { key: 'heat', icon: Thermometer, label: 'Heat Island Map', color: 'text-orange-400' },
  { key: 'airQuality', icon: Wind, label: 'Air Quality', color: 'text-cyan-400' },
  { key: 'flood', icon: Droplets, label: 'Flood Risk', color: 'text-blue-400' },
  { key: 'green', icon: Trees, label: 'Green Space Index', color: 'text-green-400' },
  { key: 'growth', icon: Building, label: 'Urban Growth', color: 'text-purple-400' },
]

export default function DataLayers() {
  const { layers, toggleLayer } = useStore()

  return (
    <div>
      <h3 className="flex items-center gap-2 text-primary-400 font-semibold mb-4">
        <Layers className="w-5 h-5" />
        Data Layers
      </h3>
      <div className="space-y-2">
        {layerConfig.map((layer) => (
          <label
            key={layer.key}
            className="flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all hover:bg-white/10 border border-transparent hover:border-white/20"
          >
            <input
              type="checkbox"
              checked={layers[layer.key]}
              onChange={() => toggleLayer(layer.key)}
              className="w-5 h-5 rounded border-2 border-primary-400 bg-transparent checked:bg-primary-400 focus:ring-2 focus:ring-primary-400 focus:ring-offset-0 cursor-pointer"
            />
            <layer.icon className={`w-5 h-5 ${layer.color}`} />
            <span className="text-white text-sm">{layer.label}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

