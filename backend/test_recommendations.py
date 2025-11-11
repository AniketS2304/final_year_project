# backend/test_recommendations.py
# Run this file to test the recommendation system

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriwise_backend.settings')
django.setup()

from api.services.land_recommender import LandRecommendationModel
from api.models import Land

def test_recommendations():
    print("=" * 80)
    print("🎯 TESTING LAND RECOMMENDATION MODEL")
    print("=" * 80)
    
    # Initialize recommender
    recommender = LandRecommendationModel()
    
    # Test Case 1: Agricultural land in Pune
    print("\n📍 TEST 1: Agricultural Land in Pune (Budget: ₹20-50L)")
    print("-" * 80)
    
    requirements_1 = {
        'purpose': 'agricultural',
        'min_size': 10,
        'max_size': 30,
        'min_price': 2000000,
        'max_price': 5000000,
        'location_preference': 'Pune',
        'connectivity_importance': 0.3,  # Less important for farms
        'infrastructure_importance': 0.7,  # More important
    }
    
    recommendations = recommender.recommend_lands(requirements_1, limit=5)
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            print(f"\n{idx}. {rec['name']}")
            print(f"   📍 Location: {rec['city']}")
            print(f"   📏 Size: {rec['size_in_acres']} acres")
            print(f"   💰 Price: ₹{rec['total_price']:,.0f} (₹{rec['price_per_acre']:,.0f}/acre)")
            print(f"   ⭐ Score: {rec['score']}/100 - {rec['recommendation_level']}")
            print(f"   ✓ {', '.join(rec['matching_features'][:3])}")
            if rec['concerns']:
                print(f"   ⚠️  {rec['concerns'][0]}")
    else:
        print("❌ No recommendations found")
    
    # Test Case 2: Commercial land in Mumbai
    print("\n\n📍 TEST 2: Commercial Land in Mumbai (Budget: ₹50L-1Cr)")
    print("-" * 80)
    
    requirements_2 = {
        'purpose': 'commercial',
        'min_size': 5,
        'max_size': 20,
        'min_price': 5000000,
        'max_price': 10000000,
        'location_preference': 'Mumbai',
        'connectivity_importance': 0.9,  # Very important for commercial
        'infrastructure_importance': 0.8,
    }
    
    recommendations = recommender.recommend_lands(requirements_2, limit=5)
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            print(f"\n{idx}. {rec['name']}")
            print(f"   📍 Location: {rec['city']}")
            print(f"   📏 Size: {rec['size_in_acres']} acres")
            print(f"   💰 Price: ₹{rec['total_price']:,.0f}")
            print(f"   ⭐ Score: {rec['score']}/100 - {rec['recommendation_level']}")
            
            # Show detailed subscores
            print(f"   📊 Subscores:")
            for key, value in rec['subscores'].items():
                print(f"      • {key}: {value}/100")
    else:
        print("❌ No recommendations found")
    
    # Test Case 3: Find similar lands
    print("\n\n📍 TEST 3: Find Similar Lands")
    print("-" * 80)
    
    first_land = Land.objects.first()
    if first_land:
        print(f"\nReference Land: {first_land.name} ({first_land.city})")
        print(f"Type: {first_land.land_type} | Size: {first_land.size_in_acres} acres")
        
        similar = recommender.get_similar_lands(first_land.id, limit=3)
        
        if similar:
            print("\nSimilar Lands:")
            for idx, sim in enumerate(similar, 1):
                print(f"\n{idx}. {sim['name']} ({sim['city']})")
                print(f"   Similarity: {sim['similarity_score']}/100")
                print(f"   Size: {sim['size_in_acres']} acres | Price: ₹{sim['total_price']:,.0f}")
    
    # Test Case 4: Specific land scoring
    print("\n\n📍 TEST 4: Score Specific Land")
    print("-" * 80)
    
    test_land = Land.objects.filter(land_type='agricultural').first()
    if test_land:
        print(f"\nEvaluating: {test_land.name}")
        
        test_requirements = {
            'purpose': 'agricultural',
            'min_size': 15,
            'max_size': 40,
            'min_price': 1000000,
            'max_price': 4000000,
            'location_preference': test_land.city,
            'connectivity_importance': 0.5,
            'infrastructure_importance': 0.6,
        }
        
        score_data = recommender.calculate_suitability_score(test_land, test_requirements)
        
        print(f"\n⭐ Overall Score: {score_data['overall_score']}/100")
        print(f"📊 Recommendation Level: {score_data['recommendation_level']}")
        
        print("\n✅ Matching Features:")
        for feature in score_data['matching_features']:
            print(f"   • {feature}")
        
        if score_data['concerns']:
            print("\n⚠️  Concerns:")
            for concern in score_data['concerns']:
                print(f"   • {concern}")
        
        print("\n📈 Detailed Subscores:")
        for key, value in score_data['subscores'].items():
            print(f"   {key}: {value}/100")
    
    print("\n" + "=" * 80)
    print("✅ TESTING COMPLETE!")
    print("=" * 80)

if __name__ == '__main__':
    # Check if data exists
    land_count = Land.objects.count()
    print(f"\n📊 Database Status: {land_count} lands available")
    
    if land_count == 0:
        print("\n⚠️  No land data found!")
        print("Run: python manage.py seed_lands")
        print("=" * 80)
    else:
        test_recommendations()