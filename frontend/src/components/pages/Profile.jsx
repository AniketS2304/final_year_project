import { useState, useEffect } from "react";
import axios from "axios";

function Profile() {
    const [editing, setEditing] = useState(false);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        date_joined: "",
    });

    useEffect(() => {
        fetchUserProfile();
    }, []);

    const fetchUserProfile = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.get("http://127.0.0.1:8000/api/user/profile/", {
                headers: {
                    Authorization: `Token ${token}`,
                },
            });
            setFormData({
                username: response.data.username || "",
                email: response.data.email || "",
                first_name: response.data.first_name || "",
                last_name: response.data.last_name || "",
                date_joined: response.data.date_joined || "",
            });
        } catch (error) {
            console.error("Error fetching user profile:", error);
            alert("Failed to load profile data");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async () => {
        try {
            const token = localStorage.getItem("token");
            await axios.put(
                "http://127.0.0.1:8000/api/user/profile/",
                {
                    email: formData.email,
                    first_name: formData.first_name,
                    last_name: formData.last_name,
                },
                {
                    headers: {
                        Authorization: `Token ${token}`,
                    },
                }
            );
            setEditing(false);
            alert("Profile updated successfully!");
            fetchUserProfile(); // Refresh data
        } catch (error) {
            console.error("Error updating profile:", error);
            alert("Failed to update profile: " + (error.response?.data?.error || error.message));
        }
    };

    const getInitials = () => {
        if (formData.first_name && formData.last_name) {
            return `${formData.first_name[0]}${formData.last_name[0]}`.toUpperCase();
        } else if (formData.first_name) {
            return formData.first_name.substring(0, 2).toUpperCase();
        } else if (formData.username) {
            return formData.username.substring(0, 2).toUpperCase();
        }
        return "U";
    };

    const getFullName = () => {
        if (formData.first_name && formData.last_name) {
            return `${formData.first_name} ${formData.last_name}`;
        } else if (formData.first_name) {
            return formData.first_name;
        }
        return formData.username;
    };

    const formatDate = (dateString) => {
        if (!dateString) return "N/A";
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading profile...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Profile Header */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-8 text-white">
                <div className="flex items-center space-x-6">
                    <div className="relative">
                        <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-4xl font-bold text-green-600">
                            {getInitials()}
                        </div>
                    </div>
                    <div className="flex-1">
                        <h1 className="text-3xl font-bold mb-2">{getFullName()}</h1>
                        <p className="text-green-50 mb-4">Welcome to AgriWise! Manage your agricultural investments and land recommendations.</p>
                        <div className="flex items-center flex-wrap gap-4 text-sm">
                            <span className="flex items-center space-x-2">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                <span>@{formData.username}</span>
                            </span>
                            <span className="flex items-center space-x-2">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                                <span>{formData.email || "No email set"}</span>
                            </span>
                            <span className="flex items-center space-x-2">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span>Member since {formatDate(formData.date_joined)}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Personal Information Card */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
                <div className="p-6">
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
                                    onClick={() => {
                                        setEditing(false);
                                        fetchUserProfile(); // Reset form data
                                    }}
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
                            <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                disabled={true}
                                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none bg-gray-100 text-gray-600 cursor-not-allowed"
                            />
                            <p className="text-xs text-gray-500 mt-1">Username cannot be changed</p>
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
                            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                            <input
                                type="text"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                disabled={!editing}
                                placeholder="Enter your first name"
                                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                            <input
                                type="text"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                disabled={!editing}
                                placeholder="Enter your last name"
                                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none disabled:bg-gray-50 disabled:text-gray-600"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;