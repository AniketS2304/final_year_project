import { useState } from 'react';
import axios from 'axios';

function LandRecommendations() {
    const [searchParams, setSearchParams] = useState({
        purpose: 'agricultural',
        min_size: '',
        max_size: '',
        min_price: '',
        max_price: '',
        location_preference: '',
        connectivity_importance: 0.5,
        infrastructure_importance: 0.5,
        limit: 10
    });

    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [searchDone, setSearchDone] = useState(false);
    const [responseTime, setResponseTime] = useState(0);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setSearchParams(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSliderChange = (e) => {
        const { name, value } = e.target;
        setSearchParams(prev => ({
            ...prev,
            [name]: parseFloat(value)
        }));
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setRecommendations([]);
        setSearchDone(false);

        try {
            const token = localStorage.getItem('token');
            console.log('getting lands...')
            const response = await axios.post(
                'http://127.0.0.1:8000/api/lands/recommend/',
                {
                    purpose: searchParams.purpose || undefined,
                    min_size: parseFloat(searchParams.min_size) || 0,
                    max_size: parseFloat(searchParams.max_size) || 10000,
                    min_price: parseFloat(searchParams.min_price) || 0,
                    max_price: parseFloat(searchParams.max_price) || 100000000,
                    location_preference: searchParams.location_preference || '',
                    connectivity_importance: searchParams.connectivity_importance,
                    infrastructure_importance: searchParams.infrastructure_importance,
                    limit: parseInt(searchParams.limit) || 10
                },
                {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (response.data.success) {
                setRecommendations(response.data.recommendations);
                setResponseTime(response.data.response_time_ms);
                setSearchDone(true);
            }
        } catch (err) {
            const errorMessage = err.response?.data?.error || err.message || 'Failed to fetch recommendations';
            setError(errorMessage);
            console.error('Error fetching recommendations:', err);
            console.error('Error details:', err.response?.data);
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 85) return 'text-green-600 bg-green-100';
        if (score >= 70) return 'text-blue-600 bg-blue-100';
        if (score >= 55) return 'text-yellow-600 bg-yellow-100';
        return 'text-red-600 bg-red-100';
    };

    const getRecommendationBadge = (level) => {
        const badges = {
            'Highly Recommended': 'bg-green-500 text-white',
            'Recommended': 'bg-blue-500 text-white',
            'Consider': 'bg-yellow-500 text-white',
            'Not Recommended': 'bg-red-500 text-white'
        };
        return badges[level] || 'bg-gray-500 text-white';
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 p-6">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                    🎯 Land Recommendations
                </h1>
                <p className="text-gray-600">
                    Find the perfect land based on your requirements using AI-powered recommendations
                </p>
            </div>

            {/* Search Form */}
            <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
                <form onSubmit={handleSearch}>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Land Purpose */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Land Purpose
                            </label>
                            <select
                                name="purpose"
                                value={searchParams.purpose}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            >
                                <option value="">Any</option>
                                <option value="agricultural">Agricultural</option>
                                <option value="residential">Residential</option>
                                <option value="commercial">Commercial</option>
                                <option value="industrial">Industrial</option>
                                <option value="mixed">Mixed Use</option>
                            </select>
                        </div>

                        {/* Min Size */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Min Size (acres)
                            </label>
                            <input
                                type="number"
                                name="min_size"
                                value={searchParams.min_size}
                                onChange={handleInputChange}
                                placeholder="e.g., 10"
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            />
                        </div>

                        {/* Max Size */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Max Size (acres)
                            </label>
                            <input
                                type="number"
                                name="max_size"
                                value={searchParams.max_size}
                                onChange={handleInputChange}
                                placeholder="e.g., 50"
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            />
                        </div>

                        {/* Min Price */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Min Price (₹)
                            </label>
                            <input
                                type="number"
                                name="min_price"
                                value={searchParams.min_price}
                                onChange={handleInputChange}
                                placeholder="e.g., 2000000"
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            />
                        </div>

                        {/* Max Price */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Max Price (₹)
                            </label>
                            <input
                                type="number"
                                name="max_price"
                                value={searchParams.max_price}
                                onChange={handleInputChange}
                                placeholder="e.g., 5000000"
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            />
                        </div>

                        {/* Location */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Preferred Location
                            </label>
                            <input
                                type="text"
                                name="location_preference"
                                value={searchParams.location_preference}
                                onChange={handleInputChange}
                                placeholder="e.g., Pune, Mumbai"
                                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring focus:ring-green-200 transition"
                            />
                        </div>
                    </div>

                    {/* Importance Sliders */}
                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Connectivity Importance: {(searchParams.connectivity_importance * 100).toFixed(0)}%
                            </label>
                            <input
                                type="range"
                                name="connectivity_importance"
                                min="0"
                                max="1"
                                step="0.1"
                                value={searchParams.connectivity_importance}
                                onChange={handleSliderChange}
                                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-600"
                            />
                            <div className="flex justify-between text-xs text-gray-500 mt-1">
                                <span>Less Important</span>
                                <span>Very Important</span>
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Infrastructure Importance: {(searchParams.infrastructure_importance * 100).toFixed(0)}%
                            </label>
                            <input
                                type="range"
                                name="infrastructure_importance"
                                min="0"
                                max="1"
                                step="0.1"
                                value={searchParams.infrastructure_importance}
                                onChange={handleSliderChange}
                                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-600"
                            />
                            <div className="flex justify-between text-xs text-gray-500 mt-1">
                                <span>Less Important</span>
                                <span>Very Important</span>
                            </div>
                        </div>
                    </div>

                    {/* Submit Button */}
                    <div className="mt-8 flex justify-center">
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-semibold text-lg hover:from-green-600 hover:to-emerald-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Searching...</span>
                                </>
                            ) : (
                                <>
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                    <span>Find Recommendations</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-lg">
                    <div className="flex items-center">
                        <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        <span className="font-semibold">{error}</span>
                    </div>
                </div>
            )}

            {/* Results Header */}
            {searchDone && (
                <div className="bg-white rounded-xl shadow-md p-6 mb-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900">
                                Found {recommendations.length} Recommendations
                            </h2>
                            <p className="text-gray-600 mt-1">
                                Response time: {responseTime}ms
                            </p>
                        </div>
                        <div className="text-right">
                            <div className="text-sm text-gray-600">Sorted by best match</div>
                        </div>
                    </div>
                </div>
            )}

            {/* No Results */}
            {searchDone && recommendations.length === 0 && (
                <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
                    <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">No lands found</h3>
                    <p className="text-gray-600 mb-6">Try adjusting your search criteria</p>
                </div>
            )}

            {/* Recommendations Grid */}
            {recommendations.length > 0 && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {recommendations.map((land, index) => (
                        <div key={land.land_id} className="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow">
                            {/* Card Header */}
                            <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-6 text-white">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-2 mb-2">
                                            <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-semibold">
                                                #{index + 1}
                                            </span>
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getRecommendationBadge(land.recommendation_level)}`}>
                                                {land.recommendation_level}
                                            </span>
                                        </div>
                                        <h3 className="text-2xl font-bold">{land.name}</h3>
                                        <p className="text-green-100 mt-1">📍 {land.city}</p>
                                    </div>
                                    <div className={`text-4xl font-bold px-4 py-2 rounded-xl ${getScoreColor(land.score)}`}>
                                        {land.score.toFixed(1)}
                                    </div>
                                </div>
                            </div>

                            {/* Card Body */}
                            <div className="p-6">
                                {/* Basic Info */}
                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div className="bg-gray-50 rounded-xl p-4">
                                        <div className="text-gray-600 text-sm mb-1">Size</div>
                                        <div className="text-2xl font-bold text-gray-900">{land.size_in_acres} <span className="text-base font-normal">acres</span></div>
                                    </div>
                                    <div className="bg-gray-50 rounded-xl p-4">
                                        <div className="text-gray-600 text-sm mb-1">Total Price</div>
                                        <div className="text-2xl font-bold text-gray-900">₹{(land.total_price / 100000).toFixed(1)}L</div>
                                    </div>
                                    <div className="bg-gray-50 rounded-xl p-4">
                                        <div className="text-gray-600 text-sm mb-1">Price/Acre</div>
                                        <div className="text-xl font-bold text-gray-900">₹{(land.price_per_acre / 100000).toFixed(2)}L</div>
                                    </div>
                                    <div className="bg-gray-50 rounded-xl p-4">
                                        <div className="text-gray-600 text-sm mb-1">Location</div>
                                        <div className="text-sm font-semibold text-gray-900">{land.latitude.toFixed(4)}, {land.longitude.toFixed(4)}</div>
                                    </div>
                                </div>

                                {/* Subscores */}
                                <div className="mb-6">
                                    <h4 className="font-semibold text-gray-900 mb-3">Detailed Scores:</h4>
                                    <div className="space-y-2">
                                        {Object.entries(land.subscores).map(([key, value]) => (
                                            <div key={key} className="flex items-center">
                                                <span className="text-sm text-gray-600 capitalize w-40">{key.replace('_', ' ')}:</span>
                                                <div className="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                                                    <div
                                                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all"
                                                        style={{ width: `${value}%` }}
                                                    ></div>
                                                </div>
                                                <span className="text-sm font-semibold text-gray-900 w-12 text-right">{value.toFixed(0)}/100</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Matching Features */}
                                {land.matching_features.length > 0 && (
                                    <div className="mb-4">
                                        <h4 className="font-semibold text-green-700 mb-2 flex items-center">
                                            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                            </svg>
                                            Advantages
                                        </h4>
                                        <ul className="space-y-1">
                                            {land.matching_features.map((feature, idx) => (
                                                <li key={idx} className="text-sm text-gray-700 flex items-start">
                                                    <span className="text-green-500 mr-2">✓</span>
                                                    {feature}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Concerns */}
                                {land.concerns.length > 0 && (
                                    <div>
                                        <h4 className="font-semibold text-orange-700 mb-2 flex items-center">
                                            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                            </svg>
                                            Concerns
                                        </h4>
                                        <ul className="space-y-1">
                                            {land.concerns.map((concern, idx) => (
                                                <li key={idx} className="text-sm text-gray-700 flex items-start">
                                                    <span className="text-orange-500 mr-2">⚠</span>
                                                    {concern}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>

                            {/* Card Footer */}
                            <div className="bg-gray-50 px-6 py-4 flex justify-between items-center">
                                <button className="text-green-600 hover:text-green-700 font-semibold flex items-center space-x-1">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                    <span>View Details</span>
                                </button>
                                <button className="text-gray-600 hover:text-gray-700">
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default LandRecommendations;
