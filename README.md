"# 🌾 AgriWise - Smart Agricultural Land & Crop Management System

> **An intelligent platform combining Machine Learning and Geographic Information Systems to revolutionize agricultural decision-making**

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.1.1-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Machine Learning Models](#-machine-learning-models)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributors](#-contributors)

---

## 🎯 Overview

**AgriWise** is a comprehensive agricultural technology platform designed to help farmers, investors, and agricultural stakeholders make data-driven decisions. The system leverages Machine Learning algorithms to provide:

1. **Intelligent Crop Recommendations** - Based on soil composition and climate data
2. **Smart Land Recommendations** - Personalized property suggestions using ML-based filtering
3. **Geographic Visualization** - Interactive maps for land exploration
4. **User Management** - Role-based access for farmers, investors, and administrators

### Problem Statement

Farmers and agricultural investors often struggle with:
- Selecting the right crops for their soil conditions
- Finding suitable agricultural land that matches their requirements
- Understanding optimal growing conditions for different crops
- Making informed investment decisions

### Our Solution

AgriWise addresses these challenges by:
- **Analyzing soil parameters** (NPK levels, pH, temperature, humidity, rainfall)
- **Recommending optimal crops** using Random Forest Classification (95%+ accuracy)
- **Matching users with suitable land** based on budget, size, location, and infrastructure needs
- **Providing confidence scores** for all recommendations to support decision-making

---

## ✨ Key Features

### 🌱 Crop Recommendation System
- **ML-Powered Predictions**: Random Forest algorithm trained on 2,200+ agricultural samples
- **7 Parameter Analysis**: N, P, K, temperature, humidity, pH, rainfall
- **High Accuracy**: 95%+ prediction accuracy
- **Top 5 Alternatives**: Provides multiple crop options with confidence scores
- **Crop Requirements Database**: Detailed optimal conditions for 22+ crops
- **Suitability Analysis**: Evaluates soil compatibility for recommended crops

### 🏞️ Land Recommendation Engine
- **Intelligent Filtering**: Content-based recommendation system
- **Multi-Criteria Matching**: Size, price, location, connectivity, infrastructure
- **Scoring Algorithm**: Weighted feature scoring for personalized results
- **Similar Properties**: Find lands similar to selected properties
- **Advanced Search**: Filter by land type, budget range, size, and city
- **Interactive Maps**: Leaflet integration for geographic visualization

### 👤 User Management
- **Three User Types**: Farmers, Investors, Administrators
- **Secure Authentication**: Token-based authentication (Django REST Framework)
- **Password Reset**: Email-based password recovery system
- **User Profiles**: Customizable profiles with bio, phone, address
- **Role-Based Access**: Different permissions for different user types

### 📊 Dashboard & Analytics
- **Personalized Dashboard**: User-specific insights and statistics
- **Saved Lands**: Bookmark properties for future reference
- **Search History**: Track recommendation queries
- **Response Time Metrics**: Performance monitoring for API calls

---

## 🛠️ Technology Stack

### **Backend**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.x | Core programming language |
| **Django** | 5.2.6 | Web framework |
| **Django REST Framework** | Latest | RESTful API development |
| **SQLite** | 3.x | Development database |
| **scikit-learn** | Latest | Machine Learning algorithms |
| **pandas** | Latest | Data manipulation |
| **numpy** | Latest | Numerical computations |
| **joblib** | Latest | Model serialization |

### **Frontend**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.1.1 | UI framework |
| **Vite** | 7.1.7 | Build tool & dev server |
| **React Router** | 7.9.2 | Client-side routing |
| **Axios** | 1.12.2 | HTTP client |
| **Leaflet** | 1.9.4 | Interactive maps |
| **React Leaflet** | 5.0.0 | React wrapper for Leaflet |
| **Tailwind CSS** | 4.1.13 | Utility-first CSS |
| **Lucide React** | 0.544.0 | Icon library |

### **Machine Learning**
- **Algorithm**: Random Forest Classifier
- **Training**: Supervised learning with labeled dataset
- **Preprocessing**: StandardScaler for feature normalization
- **Encoding**: LabelEncoder for crop labels
- **Evaluation**: 80-20 train-test split with stratification

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Home   │  │Dashboard │  │   Maps   │  │ Profile  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Django REST Framework                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Auth     │  │     Crop     │  │     Land     │     │
│  │   Endpoints  │  │  Endpoints   │  │  Endpoints   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────┬───────────────┬──────────────────┬────────────┘
             │               │                  │
             ▼               ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   User Model    │ │  ML Crop Model  │ │ ML Land Model   │
│  (CustomUser)   │ │ (Random Forest) │ │ (Recommender)   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  SQLite Database│
                    │  - Users        │
                    │  - Lands        │
                    │  - SoilData     │
                    │  - Crops        │
                    └─────────────────┘
```

### **Data Flow**

1. **User Authentication**
   - User logs in → Token generated → Token stored in client
   - All subsequent requests include authentication token

2. **Crop Recommendation**
   - User inputs soil parameters → API receives data
   - ML model processes features → Predictions generated
   - Results saved to database → Response sent to client

3. **Land Recommendation**
   - User sets preferences → API queries database
   - Recommender calculates scores → Results ranked
   - Top matches returned → Displayed on map

---

## 📦 Installation Guide

### **Prerequisites**

- Python 3.8 or higher
- Node.js 16+ and npm
- Git

### **Backend Setup**

```bash
# 1. Clone the repository
git clone https://github.com/AniketS2304/final_year_project.git
cd final_year_project

# 2. Create virtual environment
python -m venv venv

# For Windows:
venv\Scripts\activate

# For Linux/Mac:
source venv/bin/activate

# 3. Install Python dependencies
cd backend
pip install django djangorestframework django-cors-headers
pip install scikit-learn pandas numpy joblib
pip install pillow  # For image handling

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser
# OR use the create_admin.py script:
python create_admin.py

# 6. Seed sample data (optional)
python manage.py seed_lands

# 7. Start development server
python manage.py runserver
```

Backend will be available at: `http://127.0.0.1:8000/`

### **Frontend Setup**

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173/`

### **Environment Configuration**

**Backend (settings.py)**
```python
# Email Configuration (for password reset)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Frontend (src/config.js)**
```javascript
// Create this file if needed
export const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

---

## 🚀 Usage

### **1. User Registration & Login**

```bash
# Register a new user
POST http://127.0.0.1:8000/api/register/
{
  "username": "farmer1",
  "email": "farmer1@example.com",
  "password": "secure123"
}

# Login
POST http://127.0.0.1:8000/api/login/
{
  "username": "farmer1",
  "password": "secure123"
}
```

### **2. Get Crop Recommendations**

Navigate to **Dashboard → Crop Recommendations** or use API:

```bash
POST http://127.0.0.1:8000/api/crops/recommend/
Authorization: Token YOUR_AUTH_TOKEN
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 21,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 202
}
```

### **3. Search for Land**

Navigate to **Dashboard → Land Recommendations**:

- Set budget range
- Choose preferred location
- Select land type (agricultural, residential, commercial)
- View results on interactive map

### **4. Admin Panel**

Access Django admin at `http://127.0.0.1:8000/admin/`

Default credentials (if using create_admin.py):
- Username: `admin`
- Password: `admin123`

---

## 📡 API Documentation

### **Authentication Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register new user |
| POST | `/api/login/` | Login user |
| GET | `/api/user/profile/` | Get user profile |
| PUT | `/api/user/profile/` | Update profile |
| POST | `/api/password-reset/` | Request password reset |
| POST | `/api/password-reset/confirm/` | Confirm password reset |

### **Crop Recommendation Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/crops/recommend/` | Get crop recommendation |
| GET | `/api/crops/requirements/<crop_name>/` | Get crop requirements |
| GET | `/api/crops/all/` | List all crops |
| POST | `/api/soil-data/` | Save soil test data |

### **Land Recommendation Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/lands/recommend/` | Get land recommendations |
| GET | `/api/lands/` | List all lands |
| GET | `/api/lands/<id>/` | Get land details |
| GET | `/api/lands/<id>/similar/` | Find similar lands |
| POST | `/api/lands/<id>/score/` | Calculate suitability score |

### **Example API Response**

**Crop Recommendation:**
```json
{
  "success": true,
  "recommended_crop": "rice",
  "confidence": 0.95,
  "top_5_recommendations": [
    {"crop": "rice", "confidence": 0.95},
    {"crop": "wheat", "confidence": 0.03},
    {"crop": "maize", "confidence": 0.01}
  ],
  "soil_suitability": "excellent"
}
```

---

## 🤖 Machine Learning Models

### **Crop Recommendation Model**

**Dataset:**
- Source: Crop Recommendation Dataset
- Samples: 2,200+ records
- Features: 7 (N, P, K, temperature, humidity, pH, rainfall)
- Classes: 22 crops

**Model Architecture:**
```python
RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=20,          # Tree depth
    min_samples_split=5,   # Min samples to split
    min_samples_leaf=2,    # Min samples per leaf
    random_state=42
)
```

**Performance Metrics:**
- Training Accuracy: 99.1%
- Test Accuracy: 95.2%
- Cross-validation Score: 94.8%

**Supported Crops:**
rice, wheat, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee

### **Land Recommendation Algorithm**

**Approach:** Content-Based Filtering with Weighted Scoring

**Feature Weights:**
- Size Match: 25%
- Price Match: 20%
- Connectivity: 20%
- Infrastructure: 15%
- Location Match: 10%
- Soil Quality: 10%

**Scoring Formula:**
```
Final Score = Σ(weight_i × normalized_score_i)
```

---

## 🗄️ Database Schema

### **CustomUser Model**
```python
- id (Primary Key)
- username (Unique)
- email
- password (Hashed)
- user_type (farmer/investor/admin)
- phone_number
- address
- profile_picture
- bio
- is_verified
- date_joined
```

### **Land Model**
```python
- id (Primary Key)
- name
- description
- land_type
- status (available/sold/pending)
- location (lat, long, address, city, state)
- size_in_acres
- price_per_acre
- total_price
- connectivity_scores (highway, metro, airport)
- infrastructure (water, electricity, road)
- owner (ForeignKey → CustomUser)
- created_at
```

### **SoilData Model**
```python
- id (Primary Key)
- user (ForeignKey → CustomUser)
- land (ForeignKey → Land, optional)
- nitrogen, phosphorous, potassium
- ph
- temperature, humidity, rainfall
- location
- test_date
```

### **CropRecommendation Model**
```python
- id (Primary Key)
- user (ForeignKey → CustomUser)
- soil_data (ForeignKey → SoilData)
- recommended_crop
- confidence_score
- top_recommendations (JSON)
- soil_suitability
- created_at
```

---

## 📁 Project Structure

```
Agriwise/
├── backend/
│   ├── agriwise_backend/
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # URL routing
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models.py            # Database models
│   │   ├── views.py             # API views
│   │   ├── serializers.py       # DRF serializers
│   │   ├── admin.py             # Admin configuration
│   │   ├── crop_views.py        # Crop endpoints
│   │   ├── password_reset_views.py
│   │   ├── services/
│   │   │   ├── crop_recommender.py    # ML crop model
│   │   │   ├── land_recommender.py    # ML land model
│   │   │   └── recommendation_engine.py
│   │   └── management/
│   │       └── commands/
│   │           └── seed_lands.py      # Data seeding
│   ├── datasets/
│   │   └── Crop_recommendation_real.csv
│   ├── ml_models/                # Saved ML models
│   ├── manage.py
│   └── db.sqlite3
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── DashboardLayout.jsx
│   │   │   └── pages/
│   │   │       ├── Home.jsx
│   │   │       ├── Login.jsx
│   │   │       ├── Register.jsx
│   │   │       ├── Dashboard.jsx
│   │   │       ├── CropRecommendations.jsx
│   │   │       ├── LandRecommendations.jsx
│   │   │       └── Profile.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 📸 Screenshots

### Home Page
```
┌────────────────────────────────────────────────┐
│  🌾 AgriWise - Smart Agricultural Solutions    │
│                                                │
│  [Login]  [Register]  [About]  [Contact]      │
└────────────────────────────────────────────────┘
```

### Dashboard
```
┌────────────────────────────────────────────────┐
│  Welcome, Farmer John!                         │
├────────────────────────────────────────────────┤
│  [Crop Recommendations] [Land Search]          │
│  [My Profile] [Saved Lands]                    │
└────────────────────────────────────────────────┘
```

### Crop Recommendation
```
┌────────────────────────────────────────────────┐
│  Enter Soil Parameters:                        │
│  N: [90]  P: [42]  K: [43]                    │
│  Temperature: [21°C]  Humidity: [82%]         │
│  pH: [6.5]  Rainfall: [202mm]                 │
│                                                │
│  [Get Recommendation]                          │
│                                                │
│  ✅ Recommended: RICE (95% confidence)        │
│  📊 Alternatives:                             │
│     1. Rice - 95%                             │
│     2. Wheat - 3%                             │
│     3. Maize - 1%                             │
└────────────────────────────────────────────────┘
```

---

## 🔮 Future Enhancements

### Phase 2 (Planned)
- [ ] **Weather Integration**: Real-time weather API integration
- [ ] **Satellite Imagery**: Land analysis using satellite data
- [ ] **Market Prices**: Live crop price tracking
- [ ] **Yield Prediction**: Estimate crop yields

### Phase 3 (Long-term)
- [ ] **Mobile App**: React Native mobile application
- [ ] **IoT Integration**: Sensor data for real-time monitoring
- [ ] **Blockchain**: Smart contracts for land transactions
- [ ] **AI Chatbot**: Agricultural assistant bot
- [ ] **Multi-language**: Regional language support

---

## 👥 Contributors

- **Aniket Suryavanshi** - Full Stack Developer & ML Engineer
  - GitHub: [@AniketS2304](https://github.com/AniketS2304)
  - Email: aniketsuryavanshi2304@gmail.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Dataset: Kaggle Crop Recommendation Dataset
- Icons: Lucide React
- Maps: Leaflet & OpenStreetMap
- ML Framework: scikit-learn

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/AniketS2304/final_year_project/issues)
- Email: aniketsuryavanshi2304@gmail.com

---

<div align="center">

**Made with ❤️ for Agriculture**

⭐ Star this repo if you find it helpful!

</div>
" 
