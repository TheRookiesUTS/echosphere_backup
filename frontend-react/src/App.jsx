import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MainMenu from './components/MainMenu'
import Dashboard from './components/Dashboard'
import ReportingPortal from './components/ReportingPortal'

function App() {
  return (
    <Router>
      <Routes>
        {/* Main Menu - Default Route */}
        <Route path="/" element={<MainMenu />} />
        
        {/* Urban Planner Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* Reporting Portal */}
        <Route path="/reporting" element={<ReportingPortal />} />
        
        {/* Fallback to main menu */}
        <Route path="*" element={<MainMenu />} />
      </Routes>
    </Router>
  )
}

export default App