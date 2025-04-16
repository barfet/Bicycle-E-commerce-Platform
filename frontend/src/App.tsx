import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'

// Placeholder Pages (to be created next)
import HomePage from './pages/HomePage'
import AdminLoginPage from './pages/AdminLoginPage'
import AdminDashboardPage from './pages/AdminDashboardPage' // Placeholder for protected area
import ProductConfiguratorPage from './pages/ProductConfiguratorPage'

function App() {
  return (
    <Router>
      <div>
        {/* Basic Navigation Example */}
        <nav style={{ marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid #ccc' }}>
          <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
          <Link to="/configure/bicycle" style={{ marginRight: '1rem' }}>Configure Bicycle</Link>
          <Link to="/admin">Admin</Link>
        </nav>

        {/* App Routes */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/configure/:productTypeId" element={<ProductConfiguratorPage />} />
          <Route path="/admin" element={<AdminLoginPage />} />
          <Route path="/admin/dashboard" element={<AdminDashboardPage />} /> {/* This would be protected later */}
          {/* Add other routes here */}
        </Routes>
      </div>
    </Router>
  )
}

export default App
