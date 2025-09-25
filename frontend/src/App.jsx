import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from './components/pages/Register';
import Login from './components/pages/Login';

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 to-green-300 flex items-center justify-center px-4">
      <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full p-12 text-center">
        <h1 className="text-5xl font-extrabold text-green-800 mb-6">
          Welcome to AgriWise
        </h1>
        <p className="text-gray-700 text-lg mb-10">
          AgriWise is your smart farmland finder and advisor. Get AI-based crop recommendations,
          predict ROI, and make informed investment decisions for farmland and agriculture.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-6">
          <Link
            to="/login"
            className="px-10 py-4 border border-gray-400 text-gray-700 rounded-lg font-semibold transition"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="px-10 py-4 border border-gray-400 text-gray-700 rounded-lg font-semibold transition"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;
