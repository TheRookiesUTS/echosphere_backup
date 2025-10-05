import { Link } from 'react-router-dom'
import { MapPin, FileText, Users, Globe, Shield } from 'lucide-react'

export default function MainMenu() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 flex items-center justify-center p-4">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="w-full h-full bg-repeat" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>
      
      <div className="relative z-10 max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-gradient-to-r from-success-500 to-primary-400 p-4 rounded-2xl shadow-2xl">
              <Globe className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-6xl font-bold text-white mb-4 bg-gradient-to-r from-white to-primary-200 bg-clip-text text-transparent">
            EchoSphere
          </h1>
          <p className="text-xl text-primary-200 max-w-2xl mx-auto leading-relaxed">
            Urban Resilience Digital Twin - NASA Space Apps Challenge 2025
          </p>
          <p className="text-sm text-primary-300 mt-2">
            Pathways to Healthy Cities & Human Settlement
          </p>
        </div>

        {/* Main Action Cards */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Urban Planner Dashboard */}
          <Link 
            to="/dashboard" 
            className="group block bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-8 hover:bg-white/15 transition-all duration-300 hover:scale-105 hover:shadow-2xl"
          >
            <div className="flex items-start gap-6">
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-4 rounded-2xl shadow-lg group-hover:shadow-xl transition-all duration-300">
                <MapPin className="w-8 h-8 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white mb-3 group-hover:text-blue-200 transition-colors">
                  Urban Planner Dashboard
                </h2>
                <p className="text-primary-200 mb-4 leading-relaxed">
                  Access comprehensive environmental analysis, interactive mapping, and AI-powered urban planning tools for city leaders and urban planners.
                </p>
                <div className="flex items-center text-blue-300 font-semibold">
                  <span>Launch Dashboard</span>
                  <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </Link>

          {/* Reporting Portal */}
          <Link 
            to="/reporting" 
            className="group block bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-8 hover:bg-white/15 transition-all duration-300 hover:scale-105 hover:shadow-2xl"
          >
            <div className="flex items-start gap-6">
              <div className="bg-gradient-to-r from-green-500 to-green-600 p-4 rounded-2xl shadow-lg group-hover:shadow-xl transition-all duration-300">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white mb-3 group-hover:text-green-200 transition-colors">
                  Reporting Portal
                </h2>
                <p className="text-primary-200 mb-4 leading-relaxed">
                  Submit environmental reports, track urban resilience metrics, and contribute to community-driven climate adaptation initiatives.
                </p>
                <div className="flex items-center text-green-300 font-semibold">
                  <span>Submit Report</span>
                  <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </Link>
        </div>

        {/* Feature Highlights */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 text-center">
            <div className="bg-gradient-to-r from-yellow-500 to-orange-500 p-3 rounded-xl w-fit mx-auto mb-4">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Climate Resilience</h3>
            <p className="text-primary-300 text-sm">Real-time environmental monitoring and risk assessment</p>
          </div>
          
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 text-center">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-3 rounded-xl w-fit mx-auto mb-4">
              <Users className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Community Driven</h3>
            <p className="text-primary-300 text-sm">Citizen reporting and collaborative planning tools</p>
          </div>
          
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 text-center">
            <div className="bg-gradient-to-r from-cyan-500 to-blue-500 p-3 rounded-xl w-fit mx-auto mb-4">
              <Globe className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">NASA Data</h3>
            <p className="text-primary-300 text-sm">Powered by NASA Earth observation satellites</p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-primary-300 text-sm">
            🛰️ Data provided by NASA Earth Observation APIs | Urban Resilience Digital Twin
          </p>
        </div>
      </div>
    </div>
  )
}
