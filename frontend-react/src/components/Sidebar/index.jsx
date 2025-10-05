import { memo } from 'react'
import DataLayers from './DataLayers'
import PlanningScenarios from './PlanningScenarios'
import SearchLocation from './SearchLocation'
import MapLayers from './MapLayers'
import AreaSelection from './AreaSelection'
import ElevationPanel from './ElevationPanel'

export default memo(function Sidebar() {
  return (
    <aside className="bg-white/10 rounded-2xl p-6 border border-white/20 overflow-y-auto scrollbar-thin">
      <div className="space-y-6">
        <DataLayers />
        <PlanningScenarios />
        <SearchLocation />
        <MapLayers />
        <AreaSelection />
        <ElevationPanel />
      </div>
    </aside>
  )
})

