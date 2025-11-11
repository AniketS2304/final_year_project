import { useState, useEffect } from "react";
import axios from "axios";

function CropRecommendations() {
    const [formData, setFormData] = useState({
        N: "",
        P: "",
        K: "",
        temperature: "",
        humidity: "",
        ph: "",
        rainfall: "",
        location: ""
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [availableCrops, setAvailableCrops] = useState([]);
    const [history, setHistory] = useState([]);
    const [stats, setStats] = useState(null);
    const [activeTab, setActiveTab] = useState("recommend"); // recommend, history, crops

    useEffect(() => {
        fetchAvailableCrops();
        fetchHistory();
        fetchStats();
    }, []);

    const fetchAvailableCrops = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/crops/available/");
            setAvailableCrops(response.data.crops);
        } catch (err) {
            console.error("Error fetching crops:", err);
        }
    };

    const fetchHistory = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.get("http://127.0.0.1:8000/api/user/crop-recommendations/", {
                headers: { Authorization: `Token ${token}` }
            });
            setHistory(response.data.recommendations);
        } catch (err) {
            console.error("Error fetching history:", err);
        }
    };

    const fetchStats = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.get("http://127.0.0.1:8000/api/crops/stats/", {
                headers: { Authorization: `Token ${token}` }
            });
            setStats(response.data.stats);
        } catch (err) {
            console.error("Error fetching stats:", err);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError("");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setResult(null);

        try {
            const token = localStorage.getItem("token");
            const response = await axios.post(
                "http://127.0.0.1:8000/api/crops/recommend/",
                {
                    N: parseFloat(formData.N),
                    P: parseFloat(formData.P),
                    K: parseFloat(formData.K),
                    temperature: parseFloat(formData.temperature),
                    humidity: parseFloat(formData.humidity),
                    ph: parseFloat(formData.ph),
                    rainfall: parseFloat(formData.rainfall),
                    location: formData.location
                },
                { headers: { Authorization: `Token ${token}` } }
            );

            setResult(response.data);
            fetchHistory();
            fetchStats();
        } catch (err) {
            setError(err.response?.data?.error || "Failed to get recommendation");
        } finally {
            setLoading(false);
        }
    };

    const getSuitabilityColor = (suitability) => {
        const colors = {
            excellent: "bg-green-100 text-green-800 border-green-300",
            good: "bg-blue-100 text-blue-800 border-blue-300",
            moderate: "bg-yellow-100 text-yellow-800 border-yellow-300",
            poor: "bg-red-100 text-red-800 border-red-300"
        };
        return colors[suitability] || colors.moderate;
    };

    const getConfidenceColor = (confidence) => {
        const conf = parseFloat(confidence);
        if (conf >= 80) return "text-green-600";
        if (conf >= 60) return "text-blue-600";
        if (conf >= 40) return "text-yellow-600";
        return "text-red-600";
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-6">
            {/* Header */}
            <div className="max-w-7xl mx-auto mb-8">
                <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-green-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-800 flex items-center">
                                🌾 Crop Recommendation System
                            </h1>
                            <p className="text-gray-600 mt-2">
                                AI-powered crop suggestions based on soil and climate analysis
                            </p>
                        </div>
                        {stats && (
                            <div className="text-right">
                                <div className="text-3xl font-bold text-green-600">{stats.total_recommendations}</div>
                                <div className="text-sm text-gray-600">Total Recommendations</div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="max-w-7xl mx-auto mb-6">
                <div className="bg-white rounded-xl shadow-md p-2 flex gap-2">
                    <button
                        onClick={() => setActiveTab("recommend")}
                        className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${activeTab === "recommend"
                                ? "bg-green-500 text-white shadow-md"
                                : "text-gray-600 hover:bg-gray-100"
                            }`}
                    >
                        🎯 Get Recommendation
                    </button>
                    <button
                        onClick={() => setActiveTab("history")}
                        className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${activeTab === "history"
                                ? "bg-green-500 text-white shadow-md"
                                : "text-gray-600 hover:bg-gray-100"
                            }`}
                    >
                        📜 My History ({history.length})
                    </button>
                    <button
                        onClick={() => setActiveTab("crops")}
                        className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${activeTab === "crops"
                                ? "bg-green-500 text-white shadow-md"
                                : "text-gray-600 hover:bg-gray-100"
                            }`}
                    >
                        🌱 All Crops ({availableCrops.length})
                    </button>
                </div>
            </div>

            <div className="max-w-7xl mx-auto">
                {/* Recommendation Tab */}
                {activeTab === "recommend" && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Input Form */}
                        <div className="bg-white rounded-2xl shadow-xl p-8">
                            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                                <span className="bg-green-100 p-2 rounded-lg mr-3">🧪</span>
                                Soil & Climate Data
                            </h2>

                            <form onSubmit={handleSubmit} className="space-y-4">
                                {/* NPK Values */}
                                <div className="bg-green-50 rounded-xl p-4">
                                    <h3 className="font-semibold text-gray-700 mb-3">NPK Values (mg/kg)</h3>
                                    <div className="grid grid-cols-3 gap-3">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Nitrogen (N)
                                            </label>
                                            <input
                                                type="number"
                                                name="N"
                                                value={formData.N}
                                                onChange={handleChange}
                                                placeholder="0-200"
                                                required
                                                min="0"
                                                max="200"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Phosphorous (P)
                                            </label>
                                            <input
                                                type="number"
                                                name="P"
                                                value={formData.P}
                                                onChange={handleChange}
                                                placeholder="0-200"
                                                required
                                                min="0"
                                                max="200"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Potassium (K)
                                            </label>
                                            <input
                                                type="number"
                                                name="K"
                                                value={formData.K}
                                                placeholder="0-250"
                                                onChange={handleChange}
                                                required
                                                min="0"
                                                max="250"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Climate Data */}
                                <div className="bg-blue-50 rounded-xl p-4">
                                    <h3 className="font-semibold text-gray-700 mb-3">Climate Conditions</h3>
                                    <div className="grid grid-cols-2 gap-3">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Temperature (°C)
                                            </label>
                                            <input
                                                type="number"
                                                name="temperature"
                                                value={formData.temperature}
                                                onChange={handleChange}
                                                placeholder="8-43"
                                                required
                                                min="-10"
                                                max="50"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Humidity (%)
                                            </label>
                                            <input
                                                type="number"
                                                name="humidity"
                                                value={formData.humidity}
                                                onChange={handleChange}
                                                placeholder="14-99"
                                                required
                                                min="0"
                                                max="100"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                pH Value
                                            </label>
                                            <input
                                                type="number"
                                                name="ph"
                                                value={formData.ph}
                                                onChange={handleChange}
                                                placeholder="3.5-9.9"
                                                required
                                                min="0"
                                                max="14"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Rainfall (mm)
                                            </label>
                                            <input
                                                type="number"
                                                name="rainfall"
                                                value={formData.rainfall}
                                                onChange={handleChange}
                                                placeholder="20-298"
                                                required
                                                min="0"
                                                max="3500"
                                                step="0.1"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Location */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Location (Optional)
                                    </label>
                                    <input
                                        type="text"
                                        name="location"
                                        value={formData.location}
                                        onChange={handleChange}
                                        placeholder="e.g., Pune, Maharashtra"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                    />
                                </div>

                                {/* Error Message */}
                                {error && (
                                    <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                                        <p className="text-sm text-red-700">{error}</p>
                                    </div>
                                )}

                                {/* Submit Button */}
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-4 rounded-xl font-semibold hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transform transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                                >
                                    {loading ? (
                                        <span className="flex items-center justify-center">
                                            <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                            </svg>
                                            Analyzing...
                                        </span>
                                    ) : (
                                        "🎯 Get Crop Recommendation"
                                    )}
                                </button>
                            </form>
                        </div>

                        {/* Results */}
                        <div>
                            {result ? (
                                <div className="space-y-4">
                                    {/* Main Recommendation */}
                                    <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl shadow-xl p-8 text-white">
                                        <div className="flex items-center justify-between mb-4">
                                            <h3 className="text-xl font-semibold">Recommended Crop</h3>
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold border-2 ${getSuitabilityColor(result.recommendation.soil_suitability)} bg-white`}>
                                                {result.recommendation.soil_suitability.toUpperCase()}
                                            </span>
                                        </div>

                                        <div className="text-5xl font-bold mb-2 capitalize">
                                            🌾 {result.recommendation.recommended_crop}
                                        </div>

                                        <div className="flex items-center gap-2 text-green-100">
                                            <div className="text-2xl font-semibold">
                                                {result.recommendation.confidence_percentage}
                                            </div>
                                            <div className="text-sm">Confidence</div>
                                        </div>

                                        <div className="mt-4 text-sm text-green-100">
                                            ⚡ Analyzed in {result.response_time_ms}ms
                                        </div>
                                    </div>

                                    {/* Top 5 Alternatives */}
                                    <div className="bg-white rounded-2xl shadow-xl p-6">
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Alternative Crops</h3>
                                        <div className="space-y-3">
                                            {result.recommendation.top_5_recommendations.slice(1).map((crop, index) => (
                                                <div key={index} className="flex items-center gap-4">
                                                    <div className="text-2xl font-bold text-gray-400">
                                                        {index + 2}
                                                    </div>
                                                    <div className="flex-1">
                                                        <div className="flex justify-between items-center mb-1">
                                                            <span className="font-semibold text-gray-700 capitalize">
                                                                {crop.crop}
                                                            </span>
                                                            <span className={`font-semibold ${getConfidenceColor(crop.confidence * 100)}`}>
                                                                {(crop.confidence * 100).toFixed(2)}%
                                                            </span>
                                                        </div>
                                                        <div className="w-full bg-gray-200 rounded-full h-2">
                                                            <div
                                                                className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all"
                                                                style={{ width: `${crop.confidence * 100}%` }}
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
                                    <div className="text-6xl mb-4">🌱</div>
                                    <h3 className="text-xl font-semibold text-gray-800 mb-2">
                                        Ready to Find Your Perfect Crop?
                                    </h3>
                                    <p className="text-gray-600">
                                        Enter your soil and climate data to get AI-powered crop recommendations
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* History Tab */}
                {activeTab === "history" && (
                    <div className="bg-white rounded-2xl shadow-xl p-8">
                        <h2 className="text-2xl font-bold text-gray-800 mb-6">📜 Recommendation History</h2>

                        {history.length === 0 ? (
                            <div className="text-center py-12">
                                <div className="text-6xl mb-4">📭</div>
                                <p className="text-gray-600">No recommendations yet. Start by analyzing your soil!</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {history.map((item, index) => (
                                    <div key={index} className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow">
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center gap-3">
                                                <span className="text-2xl">🌾</span>
                                                <div>
                                                    <h3 className="text-xl font-bold text-gray-800 capitalize">
                                                        {item.recommended_crop}
                                                    </h3>
                                                    <p className="text-sm text-gray-500">
                                                        {new Date(item.created_at).toLocaleDateString('en-US', {
                                                            year: 'numeric',
                                                            month: 'long',
                                                            day: 'numeric',
                                                            hour: '2-digit',
                                                            minute: '2-digit'
                                                        })}
                                                    </p>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className={`text-2xl font-bold ${getConfidenceColor(parseFloat(item.confidence_percentage))}`}>
                                                    {item.confidence_percentage}
                                                </div>
                                                <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold mt-1 ${getSuitabilityColor(item.soil_suitability)}`}>
                                                    {item.soil_suitability}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* All Crops Tab */}
                {activeTab === "crops" && (
                    <div className="bg-white rounded-2xl shadow-xl p-8">
                        <h2 className="text-2xl font-bold text-gray-800 mb-6">🌱 Available Crops</h2>

                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                            {availableCrops.map((crop, index) => (
                                <div
                                    key={index}
                                    className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-4 hover:shadow-lg hover:border-green-400 transition-all cursor-pointer"
                                >
                                    <div className="text-3xl mb-2">🌾</div>
                                    <h3 className="font-semibold text-gray-800 capitalize">{crop}</h3>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default CropRecommendations;
