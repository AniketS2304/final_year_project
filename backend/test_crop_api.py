# backend/test_crop_api.py
"""
Test script for Crop Recommendation API endpoints
Run this to verify the API is working correctly
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriwise_backend.settings')
django.setup()

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def get_auth_token():
    """Login and get authentication token"""
    response = requests.post(f'{BASE_URL}/api/login/', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        token = response.json()['token']
        print(f"✅ Logged in successfully")
        print(f"   Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None


def test_crop_recommendation(token):
    """Test POST /api/crops/recommend/"""
    print("\n" + "=" * 80)
    print("🌾 TEST 1: Crop Recommendation API")
    print("=" * 80)
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test data (rice-friendly conditions)
    test_data = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 21,
        'humidity': 82,
        'ph': 6.5,
        'rainfall': 202,
        'location': 'Pune'
    }
    
    print(f"\n📤 Sending request with data:")
    print(f"   Nitrogen: {test_data['N']} mg/kg")
    print(f"   Phosphorous: {test_data['P']} mg/kg")
    print(f"   Potassium: {test_data['K']} mg/kg")
    print(f"   Temperature: {test_data['temperature']}°C")
    print(f"   Humidity: {test_data['humidity']}%")
    print(f"   pH: {test_data['ph']}")
    print(f"   Rainfall: {test_data['rainfall']} mm")
    
    response = requests.post(
        f'{BASE_URL}/api/crops/recommend/',
        json=test_data,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS! Response received in {result['response_time_ms']}ms")
        print(f"\n🎯 Recommended Crop: {result['recommendation']['recommended_crop'].upper()}")
        print(f"⭐ Confidence: {result['recommendation']['confidence_percentage']}")
        print(f"🌱 Soil Suitability: {result['recommendation']['soil_suitability'].upper()}")
        
        print(f"\n📊 Top 5 Recommendations:")
        for i, crop in enumerate(result['recommendation']['top_5_recommendations'], 1):
            print(f"   {i}. {crop['crop']:15s} - {crop['confidence'] * 100:.2f}%")
        
        return True
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"   {response.text}")
        return False


def test_available_crops():
    """Test GET /api/crops/available/"""
    print("\n" + "=" * 80)
    print("📋 TEST 2: Available Crops API")
    print("=" * 80)
    
    response = requests.get(f'{BASE_URL}/api/crops/available/')
    
    if response.status_code == 200:
        result = response.json()
        crops = result['crops']
        print(f"\n✅ SUCCESS! Found {result['count']} crops")
        print(f"\n🌾 Available Crops:")
        for i, crop in enumerate(crops, 1):
            print(f"   {i:2d}. {crop}")
        return True
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"   {response.text}")
        return False


def test_crop_requirements():
    """Test GET /api/crops/{crop_name}/requirements/"""
    print("\n" + "=" * 80)
    print("📖 TEST 3: Crop Requirements API")
    print("=" * 80)
    
    crop_name = 'rice'
    response = requests.get(f'{BASE_URL}/api/crops/{crop_name}/requirements/')
    
    if response.status_code == 200:
        result = response.json()
        data = result['data']
        conditions = data['optimal_conditions']
        
        print(f"\n✅ SUCCESS! Got requirements for {crop_name.upper()}")
        print(f"📊 Based on {data['samples_count']} samples")
        print(f"\n🌱 Optimal Growing Conditions:")
        print(f"   Nitrogen:     {conditions['nitrogen']['min']:.1f} - {conditions['nitrogen']['max']:.1f} mg/kg (avg: {conditions['nitrogen']['avg']:.1f})")
        print(f"   Phosphorous:  {conditions['phosphorous']['min']:.1f} - {conditions['phosphorous']['max']:.1f} mg/kg (avg: {conditions['phosphorous']['avg']:.1f})")
        print(f"   Potassium:    {conditions['potassium']['min']:.1f} - {conditions['potassium']['max']:.1f} mg/kg (avg: {conditions['potassium']['avg']:.1f})")
        print(f"   Temperature:  {conditions['temperature']['min']:.1f} - {conditions['temperature']['max']:.1f}°C (avg: {conditions['temperature']['avg']:.1f})")
        print(f"   Humidity:     {conditions['humidity']['min']:.1f} - {conditions['humidity']['max']:.1f}% (avg: {conditions['humidity']['avg']:.1f})")
        print(f"   pH:           {conditions['ph']['min']:.1f} - {conditions['ph']['max']:.1f} (avg: {conditions['ph']['avg']:.1f})")
        print(f"   Rainfall:     {conditions['rainfall']['min']:.1f} - {conditions['rainfall']['max']:.1f} mm (avg: {conditions['rainfall']['avg']:.1f})")
        
        return True
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"   {response.text}")
        return False


def test_user_history(token):
    """Test GET /api/user/crop-recommendations/"""
    print("\n" + "=" * 80)
    print("📜 TEST 4: User Crop History API")
    print("=" * 80)
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(
        f'{BASE_URL}/api/user/crop-recommendations/',
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS! Found {result['count']} recommendations in history")
        
        if result['count'] > 0:
            print(f"\n📊 Recent Recommendations:")
            for i, rec in enumerate(result['recommendations'][:5], 1):
                print(f"   {i}. {rec['recommended_crop']:15s} - {rec['confidence_percentage']}% (Suitability: {rec['soil_suitability']})")
        
        return True
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"   {response.text}")
        return False


def test_crop_stats(token):
    """Test GET /api/crops/stats/"""
    print("\n" + "=" * 80)
    print("📈 TEST 5: Crop Statistics API")
    print("=" * 80)
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(
        f'{BASE_URL}/api/crops/stats/',
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        stats = result['stats']
        
        print(f"\n✅ SUCCESS! Statistics retrieved")
        print(f"\n📊 Your Statistics:")
        print(f"   Total Recommendations: {stats['total_recommendations']}")
        print(f"   Average Confidence: {stats['avg_confidence']:.2f}%")
        
        if stats['most_recommended_crops']:
            print(f"\n🌾 Most Recommended Crops:")
            for i, crop_stat in enumerate(stats['most_recommended_crops'], 1):
                print(f"   {i}. {crop_stat['recommended_crop']:15s} - {crop_stat['count']} times")
        
        return True
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"   {response.text}")
        return False


def main():
    print("\n" + "=" * 80)
    print("🚀 CROP RECOMMENDATION API TESTING")
    print("=" * 80)
    print("\n⚠️  Make sure the Django server is running:")
    print("   cd backend && python manage.py runserver")
    print("\nPress Enter to continue...")
    input()
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        return
    
    # Run tests
    tests = [
        ('Crop Recommendation', lambda: test_crop_recommendation(token)),
        ('Available Crops', test_available_crops),
        ('Crop Requirements', test_crop_requirements),
        ('User History', lambda: test_user_history(token)),
        ('Crop Statistics', lambda: test_crop_stats(token)),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Crop Recommendation API is working perfectly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
