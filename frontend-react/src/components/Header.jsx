import { Satellite } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-black/30 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <Satellite className="w-8 h-8 text-primary-400" />
            <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-primary-400 to-success-400 bg-clip-text text-transparent">
              Urban Resilience Digital Twin
            </h1>
          </div>
          <div className="flex items-center">
            <span className="bg-gradient-to-r from-danger-600 to-danger-500 px-4 py-2 rounded-full text-sm font-semibold uppercase tracking-wide">
              NASA Space Apps Challenge
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}

