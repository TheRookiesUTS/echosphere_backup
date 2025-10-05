import { Beaker, Leaf, Home, Shield } from 'lucide-react'
import { useStore } from '../../store/useStore'
import { toast } from '../../utils/toast'

const scenarios = [
  {
    id: 'trees',
    icon: Leaf,
    label: 'Add Green Corridor',
    heatReduction: -2,
    greenIncrease: 15,
  },
  {
    id: 'roofs',
    icon: Home,
    label: 'Install Cool Roofs',
    heatReduction: -3,
    airImprovement: -20,
  },
  {
    id: 'flood',
    icon: Shield,
    label: 'Flood Mitigation',
    waterReduction: -25,
  },
]

export default function PlanningScenarios() {
  const { setLoading, metrics, setMetrics } = useStore()

  const runScenario = (scenario) => {
    setLoading(true)

    setTimeout(() => {
      const newMetrics = { ...metrics }

      if (scenario.heatReduction) {
        const currentHeat = parseInt(metrics.heatValue) || 30
        newMetrics.heatValue = `${currentHeat + scenario.heatReduction}°C`
        newMetrics.heatTrend = 'improving'
      }

      if (scenario.greenIncrease) {
        const currentGreen = parseInt(metrics.greenValue) || 30
        newMetrics.greenValue = `${currentGreen + scenario.greenIncrease}%`
        newMetrics.greenTrend = 'increasing'
      }

      if (scenario.airImprovement) {
        const currentAir = parseInt(metrics.airValue) || 100
        newMetrics.airValue = `${currentAir + scenario.airImprovement} AQI`
        newMetrics.airTrend = 'improving'
      }

      if (scenario.waterReduction) {
        const currentWater = parseInt(metrics.waterValue) || 60
        newMetrics.waterValue = `${currentWater + scenario.waterReduction}%`
        newMetrics.waterTrend = 'improving'
      }

      setMetrics(newMetrics)
      setLoading(false)

      toast.success(`${scenario.label} simulation completed!`, `Scenario analysis shows positive environmental impacts`)
    }, 2000)
  }

  return (
    <div>
      <h3 className="flex items-center gap-2 text-primary-400 font-semibold mb-4">
        <Beaker className="w-5 h-5" />
        Planning Scenarios
      </h3>
      <div className="space-y-2">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            onClick={() => runScenario(scenario)}
            className="w-full flex items-center gap-3 p-3 bg-gradient-to-r from-success-600 to-success-500 rounded-lg font-semibold text-white transition-all hover:shadow-lg hover:shadow-success-500/30 hover:-translate-y-0.5 active:translate-y-0"
          >
            <scenario.icon className="w-5 h-5" />
            <span className="text-sm">{scenario.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

