import { memo } from 'react'
import { Thermometer, Wind, Droplet, Leaf } from 'lucide-react'
import { useStore } from '../../store/useStore'

const metricsConfig = [
  {
    key: 'heat',
    label: 'Heat Stress',
    icon: Thermometer,
    gradient: 'from-danger-600 to-danger-500',
    valueKey: 'heatValue',
    trendKey: 'heatTrend',
  },
  {
    key: 'air',
    label: 'Air Quality',
    icon: Wind,
    gradient: 'from-cyan-600 to-cyan-500',
    valueKey: 'airValue',
    trendKey: 'airTrend',
  },
  {
    key: 'water',
    label: 'Water Stress',
    icon: Droplet,
    gradient: 'from-blue-600 to-blue-500',
    valueKey: 'waterValue',
    trendKey: 'waterTrend',
  },
  {
    key: 'green',
    label: 'Green Coverage',
    icon: Leaf,
    gradient: 'from-success-600 to-success-500',
    valueKey: 'greenValue',
    trendKey: 'greenTrend',
  },
]

export default memo(function MetricsGrid() {
  // Selective subscription - only subscribe to metrics
  const metrics = useStore((state) => state.metrics)

  return (
    <div className="grid grid-cols-2 gap-4">
      {metricsConfig.map((metric) => (
        <div
          key={metric.key}
          className="bg-white/5 border border-white/10 rounded-xl p-4 transition-all hover:bg-white/10 hover:-translate-y-1 cursor-pointer"
        >
          <div
            className={`w-10 h-10 rounded-lg bg-gradient-to-br ${metric.gradient} flex items-center justify-center mb-3`}
          >
            <metric.icon className="w-5 h-5 text-white" />
          </div>
          <h4 className="text-sm text-gray-400 mb-2">{metric.label}</h4>
          <div className="text-2xl font-bold text-white mb-1">
            {metrics[metric.valueKey] || '--'}
          </div>
          <div className="text-xs text-primary-400 font-medium">
            {metrics[metric.trendKey] || '--'}
          </div>
        </div>
      ))}
    </div>
  )
})

