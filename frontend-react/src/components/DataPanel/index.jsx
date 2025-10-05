import { memo, useCallback } from 'react'
import MetricsGrid from './MetricsGrid'
import AIAssistant from './AIAssistant'
import { TrendingUp, RefreshCw } from 'lucide-react'
import { useStore } from '../../store/useStore'

export default memo(function DataPanel() {
  // Selective subscription
  const initializeData = useStore((state) => state.initializeData)

  const handleRefresh = useCallback(() => {
    initializeData()
  }, [initializeData])

  return (
    <aside className="bg-white/10 rounded-2xl p-6 border border-white/20 overflow-y-auto scrollbar-thin">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-primary-400 font-semibold text-lg">
            <TrendingUp className="w-5 h-5" />
            Environmental Metrics
          </h3>
          <button
            onClick={handleRefresh}
            className="w-10 h-10 flex items-center justify-center bg-white/10 border border-white/20 rounded-lg hover:bg-white/20 transition-all hover:rotate-180"
          >
            <RefreshCw className="w-5 h-5 text-white" />
          </button>
        </div>

        {/* Metrics Grid */}
        <MetricsGrid />

        {/* AI Assistant */}
        <AIAssistant />
      </div>
    </aside>
  )
})

