import { Loader2, Satellite } from 'lucide-react'
import { useEffect, useState } from 'react'

export default function LoadingOverlay({ isOpen }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    if (isOpen) {
      setMounted(true)
    }
  }, [isOpen])

  if (!mounted && !isOpen) return null

  return (
    <div
      className={`fixed inset-0 bg-black/80 backdrop-blur-sm z-[9999] flex items-center justify-center transition-opacity duration-300 ${
        isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
      }`}
    >
      <div className="text-center text-white">
        <Satellite className="w-12 h-12 text-primary-400 mx-auto mb-4 animate-spin-slow" />
        <p className="text-lg font-medium">Loading NASA Earth Observation Data...</p>
      </div>
    </div>
  )
}

