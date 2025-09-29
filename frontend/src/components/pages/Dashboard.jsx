import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="min-h-screen flex flex-col bg-gray-50">
            {/* Navbar */}
            <nav className="bg-green-600 text-white px-6 py-4 flex justify-between items-center shadow-md">
                <h1 className="text-2xl font-bold">🌱 AgriWise Dashboard</h1>
                <button
                    onClick={handleLogout}
                    className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition"
                >
                    Logout
                </button>
            </nav>

            {/* Welcome message */}
            <header className="p-6 text-center">
                <h2 className="text-3xl font-semibold text-gray-800">
                    Welcome back to AgriWise!
                </h2>
                <p className="text-gray-600 mt-2">
                    Manage farmland insights, explore crops, and search for opportunities 🚜
                </p>
            </header>

            {/* Main content: 2-column layout */}
            <main className="flex flex-grow px-6 py-4 gap-6">
                {/* Left Section: Features */}
                <aside className="w-1/3 bg-white shadow-md rounded-lg p-6">
                    <h3 className="text-xl font-semibold mb-4 text-green-700">Features</h3>
                    <ul className="space-y-3 text-gray-700">
                        <li className="p-2 rounded hover:bg-green-50 cursor-pointer">🌾 Crop Recommendations</li>
                        <li className="p-2 rounded hover:bg-green-50 cursor-pointer">📊 ROI Prediction</li>
                        <li className="p-2 rounded hover:bg-green-50 cursor-pointer">📝 Document Checklist</li>
                        <li className="p-2 rounded hover:bg-green-50 cursor-pointer">💹 Market Trends</li>
                    </ul>
                </aside>

                {/* Right Section: Map Search */}
                <section className="flex-1 bg-white shadow-md rounded-lg p-6">
                    <h3 className="text-xl font-semibold mb-4 text-green-700">
                        🔍 Search Farmland
                    </h3>
                    <div className="mb-4">
                        <input
                            type="text"
                            placeholder="Enter location, soil type, or crop..."
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500"
                        />
                    </div>
                    <div className="h-80 bg-gray-200 flex items-center justify-center rounded-lg">
                        {/* Placeholder for Map */}
                        <span className="text-gray-500">🗺️ Map will be displayed here</span>
                    </div>
                </section>
            </main>
        </div>
    );
}

export default Dashboard;
