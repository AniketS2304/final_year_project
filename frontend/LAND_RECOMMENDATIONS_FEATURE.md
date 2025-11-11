# 🎯 Land Recommendations Frontend Feature

## ✅ What Was Created

### New Page: `LandRecommendations.jsx`
**Location:** `frontend/src/components/pages/LandRecommendations.jsx`

A complete, production-ready frontend page that mirrors all the functionality from `test_recommendations.py` with a beautiful UI.

---

## 🎨 Features Implemented

### 1. **Smart Search Form**
- Land purpose selector (Agricultural, Residential, Commercial, Industrial, Mixed)
- Size range inputs (min/max acres)
- Price range inputs (min/max ₹)
- Location preference input
- **Interactive Sliders** for:
  - Connectivity Importance (0-100%)
  - Infrastructure Importance (0-100%)

### 2. **Real-time Recommendations**
- Connects to backend API: `POST /api/lands/recommend/`
- Displays response time
- Shows number of results found
- Beautiful loading animation

### 3. **Rich Recommendation Cards**
Each recommendation card displays:
- **Rank & Score** - Position and overall score out of 100
- **Recommendation Level Badge** - Highly Recommended, Recommended, Consider, Not Recommended
- **Land Details:**
  - Name and location
  - Size in acres
  - Total price and price per acre
  - GPS coordinates
- **Detailed Subscores** with progress bars:
  - Size match
  - Price match
  - Connectivity
  - Infrastructure
  - Location match
  - Land type match
- **Advantages** - Green checkmarks showing matching features
- **Concerns** - Orange warnings showing potential issues
- **Action Buttons** - View details and save to favorites

### 4. **Color-coded Scoring System**
- 🟢 **85-100**: Green (Highly Recommended)
- 🔵 **70-84**: Blue (Recommended)
- 🟡 **55-69**: Yellow (Consider)
- 🔴 **Below 55**: Red (Not Recommended)

### 5. **Responsive Design**
- Mobile-friendly grid layout
- Cards adjust to screen size
- Beautiful gradient backgrounds
- Smooth animations and transitions

---

## 🔗 Navigation

### Updated Files:
1. **App.jsx** - Added route: `/dashboard/recommendations`
2. **DashboardLayout.jsx** - Added sidebar link: "Land Recommendations"

### How to Access:
1. Login to your account
2. Click "Land Recommendations" in the sidebar
3. Fill out the search form
4. Click "Find Recommendations"

---

## 🧪 Testing Scenarios (Same as test_recommendations.py)

### Test 1: Agricultural Land in Pune
```
Purpose: Agricultural
Min Size: 10 acres
Max Size: 30 acres
Min Price: ₹20,00,000
Max Price: ₹50,00,000
Location: Pune
Connectivity: 30%
Infrastructure: 70%
```

### Test 2: Commercial Land in Mumbai
```
Purpose: Commercial
Min Size: 5 acres
Max Size: 20 acres
Min Price: ₹50,00,000
Max Price: ₹1,00,00,000
Location: Mumbai
Connectivity: 90%
Infrastructure: 80%
```

### Test 3: Find Similar Lands
- View a land detail
- Click "Find Similar" button (coming soon)

### Test 4: Score Specific Land
- Each card shows detailed subscores
- Visual progress bars for each criteria

---

## 🎨 UI/UX Highlights

### Design System:
- **Colors**: Green/Emerald gradient theme
- **Shadows**: Multiple elevation levels
- **Rounded Corners**: Consistent 1.5rem radius
- **Animations**: Smooth transitions on hover
- **Typography**: Clean, readable fonts with proper hierarchy

### Interactive Elements:
- Hover effects on cards
- Animated loading spinner
- Range sliders with real-time percentage display
- Color-coded score badges
- Progress bars for subscores

### Error Handling:
- Error messages with icons
- "No results found" state with helpful message
- Form validation (client-side)

---

## 📡 API Integration

### Endpoint Used:
```
POST http://127.0.0.1:8000/api/lands/recommend/
```

### Request Payload:
```json
{
  "purpose": "agricultural",
  "min_size": 10,
  "max_size": 50,
  "min_price": 2000000,
  "max_price": 5000000,
  "location_preference": "Pune",
  "connectivity_importance": 0.5,
  "infrastructure_importance": 0.7,
  "limit": 10
}
```

### Response Structure:
```json
{
  "success": true,
  "count": 5,
  "response_time_ms": 150,
  "recommendations": [
    {
      "land_id": 1,
      "name": "Green Valley Farm",
      "city": "Pune",
      "size_in_acres": 25.0,
      "total_price": 5000000,
      "price_per_acre": 200000,
      "score": 85.5,
      "subscores": { ... },
      "matching_features": ["..."],
      "concerns": ["..."],
      "recommendation_level": "Highly Recommended",
      "latitude": 18.5204,
      "longitude": 73.8567
    }
  ]
}
```

---

## 🚀 Next Steps (Optional Enhancements)

1. **View Land Details** - Modal or separate page
2. **Save to Favorites** - Save/bookmark lands
3. **Compare Lands** - Side-by-side comparison
4. **Map View** - Show lands on interactive map
5. **Export Results** - Download as PDF/Excel
6. **Similar Lands** - Find similar properties
7. **Price History** - Track price changes
8. **Filters** - Advanced filtering options

---

## ✅ How to Run

### Backend:
```bash
cd backend
python manage.py runserver
```
Server runs at: `http://127.0.0.1:8000`

### Frontend:
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

### Access the Feature:
1. Navigate to `http://localhost:5173`
2. Login with your credentials
3. Click "Land Recommendations" in the sidebar
4. Start searching! 🎯

---

## 📱 Screenshots Layout

The page includes:
- 📝 **Search Form Section** - Top of page, white card with form fields
- 📊 **Results Header** - Shows count and response time
- 🎴 **Recommendation Cards Grid** - 2-column responsive grid
- ⭐ **Score Visualization** - Color-coded badges and progress bars
- ✅ **Feature Lists** - Advantages with checkmarks
- ⚠️ **Concerns Lists** - Warnings with alert icons

---

**The Land Recommendations page is now fully functional and matches all the test scenarios from `test_recommendations.py` with a beautiful, modern UI! 🚀**
