import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Register from './components/pages/Register';
import Login from './components/pages/Login';
import Home from './components/pages/Home';
import ResetPassword from './components/pages/ResetPassword';
import DashboardLayout from './components/layout/DashboardLayout.jsx';
import Dashboard from './components/pages/Dashboard';
import Profile from './components/pages/Profile';
import LandRecommendations from './components/pages/LandRecommendations';
import CropRecommendations from './components/pages/CropRecommendations';

// Protected Route Component
function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />

        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="profile" element={<Profile />} />
          <Route path="recommendations" element={<LandRecommendations />} />
          <Route path="crop-advisor" element={<CropRecommendations />} />

          {/* Placeholder routes for other features */}
          <Route path="map" element={<ComingSoon title="Interactive Map" />} />
          <Route path="properties" element={<ComingSoon title="My Properties" />} />
          <Route path="calculator" element={<ComingSoon title="ROI Calculator" />} />
          <Route path="analytics" element={<ComingSoon title="Analytics" />} />
          <Route path="settings" element={<ComingSoon title="Settings" />} />
        </Route>

        {/* 404 Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

// Coming Soon Component
function ComingSoon({ title }) {
  return (
    <div className="flex flex-col items-center justify-center h-96">
      <div className="text-center">
        <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-3">{title}</h2>
        <p className="text-gray-600 mb-6">This feature is under development and will be available soon!</p>
        <div className="inline-flex items-center space-x-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-medium">
          <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Coming Soon</span>
        </div>
      </div>
    </div>
  );
}

// 404 Not Found Component
function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-gray-300 mb-4">404</h1>
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Page Not Found</h2>
        <p className="text-gray-600 mb-8">The page you're looking for doesn't exist.</p>
        <a
          href="/"
          className="inline-block px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-semibold hover:from-green-600 hover:to-emerald-700 transition-all shadow-lg"
        >
          Go Home
        </a>
      </div>
    </div>
  );
}

export default App;