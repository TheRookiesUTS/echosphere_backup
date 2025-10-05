import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import Header from './Header'
import Sidebar from './Sidebar'
import MapContainer from './Map/MapContainer'
import DataPanel from './DataPanel'
import LoadingOverlay from './LoadingOverlay'
import { useStore } from '../store/useStore'
import { useEffect } from 'react'

export default function Dashboard() {
  const loading = useStore((state) => state.loading)
  const initializeData = useStore((state) => state.initializeData)

  useEffect(() => {
    initializeData()
    // Only run once on mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700">
      {/* Custom Header with Back Button */}
      <header className="bg-black/30 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link
                to="/"
                className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-2 hover:bg-white/20 transition-all duration-300"
              >
                <ArrowLeft className="w-5 h-5 text-white" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white">EchoSphere</h1>
                <p className="text-primary-300 text-sm">Urban Resilience Digital Twin</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="bg-gradient-to-r from-success-600 to-success-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                🛰️ NASA Powered
              </span>
            </div>
          </div>
        </div>
      </header>
      
      <main className="grid grid-cols-1 lg:grid-cols-[320px_1fr_350px] gap-4 p-4 h-[calc(100vh-80px)]">
        <Sidebar />
        <MapContainer />
        <DataPanel />
      </main>

      <LoadingOverlay isOpen={loading} />

      {/* NASA Attribution Footer */}
      <footer className="bg-black/30 backdrop-blur-md border-t border-white/10 py-4 text-center text-sm text-gray-400">
        <div className="container mx-auto px-4">
          <p className="flex items-center justify-center gap-2">
            <span className="text-danger-600">🛰️</span>
            Data provided by NASA Earth Observation APIs | Urban Resilience Digital Twin for NASA Space Apps Challenge
          </p>
        </div>
      </footer>
    </div>
  )
}

