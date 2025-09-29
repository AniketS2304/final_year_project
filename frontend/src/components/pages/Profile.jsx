import { useState } from "react";

function Profile() {
    const [activeTab, setActiveTab] = useState("personal");
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        fullName: "John Doe",
        email: "john.doe@example.com",
        phone: "+91 98765 43210",
        location: "Patna, Bihar",
        bio: "Passionate farmer and agricultural investor with 10 years of experience.",
        farmSize: "25 Acres",
        cropTypes: "Wheat, Rice, Cotton",
        experience: "10 Years"
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = () => {
        setEditing(false);
        alert("Profile updated successfully!");
    };

    const stats = [
        { label: "Properties Owned", value: "12", icon: "🏠" },
        { label: "Total Investment", value: "₹45.2L", icon: "💰" },
        { label: "Years Active", value: "3", icon: "📅" },
        { label: "Success Rate", value: "92%", icon: "📈" }
    ];

    const achievements = [
        { title: "Early Adopter", desc: "Joined in first year", icon: "🏆" },
        { title: "Top Investor", desc: "₹50L+ invested", icon: "💎" },
        { title: "Green Thumb", desc: "5+ successful harvests", icon: "🌾" },
        { title: "Community Leader", desc: "Helped 50+ farmers", icon: "👥" }
    ];

    const activities = [
        { action: "Added new property", item: "Green Valley Farm", time: "2 days ago" },
        { action: "Completed harvest", item: "Sunset Orchards", time: "1 week ago" },
        { action: "ROI Calculation", item: "River Side Plot", time: "2 weeks ago" },
        { action: "Got crop recommendation", item: "Northern Fields", time: "3 weeks ago" }
    ];

    return (
        <div className="space-y-6">
            {/* Profile Header */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-8 text-white">
                <div className="flex items-center space-x-6">
                    <div className="relative">
                        <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-4xl font-bold text-green-600">
                            JD
                        </div>
                        <button className="absolute bottom-0 right-0 w-8 h-8 bg-white rounded-full flex items-center justify-center text-green-600 shadow-lg hover:scale-110 transition-transform">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                            </svg>
                        </button>
                    </div>
                    <div className="flex-1">
                        <h1 className="text-3xl font-bold mb-2">{formData.fullName}</h1>
                        <p className="text-green-50 mb-4">{formData.bio}</p>
                        <div className="flex items-center space-x-4 text-sm">
                            <span className="flex items-center space-x-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <span>{formData.location}</span>
                            </span>
                            <span className="flex items-center space-x-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                                <span>{formData.email}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((stat, idx) => (
                    <div key={idx} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
                        <div className="text-3xl mb-2">{stat.icon}</div>
                        <p className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</p>
                        <p className="text-sm text-gray-600">{stat.label}</p>
                    </div>
                ))}
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
                <div className="border-b border-gray-200 px-6">
                    <nav className="flex space-x-8">
                        {["personal", "farm", "achievements", "activity"].map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`py-4 px-2 font-medium capitalize border-b-2 transition-colors ${activeTab === tab
                                        ? "border-green-500 text-green-600"
                                        : "border-transparent text-gray-600 hover:text-gray-900"
                                    }`}
                            >
                                {tab}
                            </button>
                        ))}
                    </nav>
                </div>

                <div className="p-6">
                    {/* Personal Info Tab */}
                    {activeTab === "personal" && (
                        <div className="space-y-6">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl font-bold text-gray-900">Personal Information</h2>
                                {!editing ? (
                                    <button
                                        onClick={() => setEditing(true)}
                                        className="px-4 py-2 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors"
                                    >
                                        Edit Profile
                                    </button>
                                ) : (
                                    <div className="space-x-3">
                                        <button
                                            onClick={() => setEditing(false)}
                                            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-colors"
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            onClick={handleSave}
                                            className="px-4 py-2 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors"
                                        >
                                            Save Changes
                                        </button>
                                    </div>
                                )}
                            </div>

                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                                    <input
                                        type="text"
                                        name="fullName"
                                        value={formData.fullName}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                                    <input
                                        type="tel"
                                        name="phone"
                                        value={formData.phone}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                                    <input
                                        type="text"
                                        name="location"
                                        value={formData.location}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div className="md:col-span-2">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                                    <textarea
                                        name="bio"
                                        value={formData.bio}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        rows={4}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Farm Details Tab */}
                    {activeTab === "farm" && (
                        <div className="space-y-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-6">Farm Details</h2>
                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Total Farm Size</label>
                                    <input
                                        type="text"
                                        name="farmSize"
                                        value={formData.farmSize}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Crop Types</label>
                                    <input
                                        type="text"
                                        name="cropTypes"
                                        value={formData.cropTypes}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Experience</label>
                                    <input
                                        type="text"
                                        name="experience"
                                        value={formData.experience}
                                        onChange={handleChange}
                                        disabled={!editing}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Achievements Tab */}
                    {activeTab === "achievements" && (
                        <div>
                            <h2 className="text-xl font-bold text-gray-900 mb-6">Your Achievements</h2>
                            <div className="grid md:grid-cols-2 gap-4">
                                {achievements.map((achievement, idx) => (
                                    <div key={idx} className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
                                        <div className="text-4xl mb-3">{achievement.icon}</div>
                                        <h3 className="font-bold text-gray-900 mb-1">{achievement.title}</h3>
                                        <p className="text-sm text-gray-600">{achievement.desc}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Activity Tab */}
                    {activeTab === "activity" && (
                        <div>
                            <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Activity</h2>
                            <div className="space-y-4">
                                {activities.map((activity, idx) => (
                                    <div key={idx} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl">
                                        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                                            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                            </svg>
                                        </div>
                                        <div className="flex-1">
                                            <p className="font-medium text-gray-900">{activity.action}</p>
                                            <p className="text-sm text-gray-600">{activity.item}</p>
                                        </div>
                                        <span className="text-sm text-gray-500">{activity.time}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Profile;