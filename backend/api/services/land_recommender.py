# backend/api/services/land_recommender.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from typing import List, Dict, Tuple
from api.models import Land

class LandRecommendationModel:
    """
    ML Model for Land Recommendation based on user requirements
    Uses content-based filtering + feature scoring
    """
    
    def __init__(self):
        self.model_path = 'ml_models/land_recommender.pkl'
        self.scaler_path = 'ml_models/land_scaler.pkl'
        self.scaler = None
        self.feature_weights = {
            'size_match': 0.25,
            'price_match': 0.20,
            'connectivity': 0.20,
            'infrastructure': 0.15,
            'location_match': 0.10,
            'soil_quality': 0.10
        }
        
    def prepare_features(self, land: Land) -> np.array:
        """
        Extract and normalize features from Land object
        Returns: normalized feature vector
        """
        features = {
            # Size features
            'size_in_acres': float(land.size_in_acres),
            'size_category': self._categorize_size(float(land.size_in_acres)),
            
            # Price features
            'price_per_acre': float(land.price_per_acre),
            'total_price': float(land.total_price),
            'price_category': self._categorize_price(float(land.total_price)),
            
            # Connectivity scores (0-100)
            'highway_proximity': land.highway_proximity_score,
            'metro_proximity': land.metro_proximity_score,
            'airport_proximity': land.airport_proximity_score,
            'avg_connectivity': (land.highway_proximity_score + 
                               land.metro_proximity_score + 
                               land.airport_proximity_score) / 3,
            
            # Infrastructure boolean to numeric
            'has_water': 1 if land.has_water_supply else 0,
            'has_electricity': 1 if land.has_electricity else 0,
            'has_road': 1 if land.has_road_access else 0,
            'infrastructure_score': sum([
                land.has_water_supply,
                land.has_electricity,
                land.has_road_access
            ]) / 3 * 100,
            
            # Land type encoded
            'land_type': self._encode_land_type(land.land_type),
            
            # Location features
            'latitude': float(land.latitude),
            'longitude': float(land.longitude),
            
            # Derived features
            'value_per_acre': float(land.total_price) / float(land.size_in_acres) if land.size_in_acres > 0 else 0,
        }
        
        return np.array(list(features.values()))
    
    def _categorize_size(self, size: float) -> int:
        """Categorize land size into buckets"""
        if size < 5:
            return 0  # Small
        elif size < 20:
            return 1  # Medium
        elif size < 50:
            return 2  # Large
        else:
            return 3  # Very Large
    
    def _categorize_price(self, price: float) -> int:
        """Categorize price into buckets"""
        if price < 500000:
            return 0  # Budget
        elif price < 2000000:
            return 1  # Mid-range
        elif price < 5000000:
            return 2  # Premium
        else:
            return 3  # Luxury
    
    def _encode_land_type(self, land_type: str) -> int:
        """Encode land type"""
        encoding = {
            'agricultural': 0,
            'residential': 1,
            'commercial': 2,
            'industrial': 3,
            'mixed': 4
        }
        return encoding.get(land_type, 0)
    
    def calculate_suitability_score(self, land: Land, user_requirements: Dict) -> Dict:
        """
        Calculate how well a land matches user requirements
        
        Args:
            land: Land object
            user_requirements: {
                'purpose': 'agricultural/residential/commercial',
                'min_size': 10,
                'max_size': 50,
                'min_price': 500000,
                'max_price': 5000000,
                'location_preference': 'Pune',
                'connectivity_importance': 0.8,  # 0-1
                'infrastructure_importance': 0.7,
            }
        
        Returns:
            {
                'overall_score': 85.5,
                'subscores': {...},
                'matching_features': [...],
                'concerns': [...]
            }
        """
        
        scores = {}
        matching_features = []
        concerns = []
        
        # 1. Size Match (0-100)
        size = float(land.size_in_acres)
        min_size = user_requirements.get('min_size', 0)
        max_size = user_requirements.get('max_size', float('inf'))
        
        if min_size <= size <= max_size:
            scores['size_match'] = 100
            matching_features.append(f"Perfect size match: {size} acres")
        elif size < min_size:
            deficit = (size / min_size) * 100
            scores['size_match'] = max(0, deficit)
            concerns.append(f"Land is smaller than required ({size} < {min_size} acres)")
        else:
            scores['size_match'] = 80  # Larger is usually acceptable
            matching_features.append(f"Spacious land: {size} acres")
        
        # 2. Price Match (0-100)
        price = float(land.total_price)
        min_price = user_requirements.get('min_price', 0)
        max_price = user_requirements.get('max_price', float('inf'))
        
        if min_price <= price <= max_price:
            # Give higher score if price is in lower range (better value)
            price_ratio = (price - min_price) / (max_price - min_price) if max_price > min_price else 0.5
            scores['price_match'] = 100 - (price_ratio * 20)  # 80-100 range
            matching_features.append(f"Within budget: ₹{price:,.0f}")
        else:
            overshoot = (price / max_price) * 100 if price > max_price else 100
            scores['price_match'] = max(0, 100 - overshoot)
            if price > max_price:
                concerns.append(f"Price exceeds budget (₹{price:,.0f} > ₹{max_price:,.0f})")
        
        # 3. Connectivity Score (0-100)
        connectivity_importance = user_requirements.get('connectivity_importance', 0.5)
        avg_connectivity = (land.highway_proximity_score + 
                          land.metro_proximity_score + 
                          land.airport_proximity_score) / 3
        
        scores['connectivity'] = avg_connectivity * connectivity_importance + (100 * (1 - connectivity_importance))
        
        if avg_connectivity > 70:
            matching_features.append("Excellent connectivity")
        elif avg_connectivity < 30:
            concerns.append("Limited connectivity to major transport")
        
        # 4. Infrastructure Score (0-100)
        infrastructure_importance = user_requirements.get('infrastructure_importance', 0.5)
        infra_available = sum([
            land.has_water_supply,
            land.has_electricity,
            land.has_road_access
        ])
        infra_score = (infra_available / 3) * 100
        
        scores['infrastructure'] = infra_score * infrastructure_importance + (100 * (1 - infrastructure_importance))
        
        if infra_available == 3:
            matching_features.append("All basic infrastructure available")
        elif infra_available == 0:
            concerns.append("No basic infrastructure available")
        
        # 5. Location Match (0-100)
        location_pref = user_requirements.get('location_preference', '')
        if location_pref and location_pref.lower() in land.city.lower():
            scores['location_match'] = 100
            matching_features.append(f"Located in preferred area: {land.city}")
        elif location_pref and location_pref.lower() in land.state.lower():
            scores['location_match'] = 70
        else:
            scores['location_match'] = 50  # Neutral if no preference
        
        # 6. Land Type Match (0-100)
        purpose = user_requirements.get('purpose', '')
        if purpose and purpose.lower() == land.land_type.lower():
            scores['land_type_match'] = 100
            matching_features.append(f"Perfect match: {land.land_type} land")
        else:
            scores['land_type_match'] = 60  # Partial match
        
        # Calculate weighted overall score
        overall_score = (
            scores['size_match'] * self.feature_weights['size_match'] +
            scores['price_match'] * self.feature_weights['price_match'] +
            scores['connectivity'] * self.feature_weights['connectivity'] +
            scores['infrastructure'] * self.feature_weights['infrastructure'] +
            scores['location_match'] * self.feature_weights['location_match'] +
            scores.get('land_type_match', 50) * self.feature_weights['soil_quality']
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'subscores': {k: round(v, 2) for k, v in scores.items()},
            'matching_features': matching_features,
            'concerns': concerns,
            'recommendation_level': self._get_recommendation_level(overall_score)
        }
    
    def _get_recommendation_level(self, score: float) -> str:
        """Get recommendation level based on score"""
        if score >= 85:
            return "Highly Recommended"
        elif score >= 70:
            return "Recommended"
        elif score >= 55:
            return "Consider"
        else:
            return "Not Recommended"
    
    def recommend_lands(self, user_requirements: Dict, limit: int = 10) -> List[Dict]:
        """
        Main recommendation function
        
        Args:
            user_requirements: User's search criteria
            limit: Number of recommendations to return
        
        Returns:
            List of recommended lands with scores
        """
        
        # Get all available lands
        lands = Land.objects.filter(status='available')
        
        # Apply hard filters first
        if 'purpose' in user_requirements and user_requirements['purpose']:
            lands = lands.filter(land_type=user_requirements['purpose'])
        
        if 'location_preference' in user_requirements:
            location = user_requirements['location_preference']
            lands = lands.filter(
                city__icontains=location
            ) | lands.filter(
                state__icontains=location
            )
        
        # Calculate scores for each land
        recommendations = []
        for land in lands:
            score_data = self.calculate_suitability_score(land, user_requirements)
            
            recommendations.append({
                'land_id': land.id,
                'name': land.name,
                'city': land.city,
                'size_in_acres': float(land.size_in_acres),
                'total_price': float(land.total_price),
                'price_per_acre': float(land.price_per_acre),
                'score': score_data['overall_score'],
                'subscores': score_data['subscores'],
                'matching_features': score_data['matching_features'],
                'concerns': score_data['concerns'],
                'recommendation_level': score_data['recommendation_level'],
                'latitude': float(land.latitude),
                'longitude': float(land.longitude),
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]
    
    def get_similar_lands(self, land_id: int, limit: int = 5) -> List[Dict]:
        """
        Find lands similar to a given land
        Uses feature similarity
        """
        try:
            target_land = Land.objects.get(id=land_id)
        except Land.DoesNotExist:
            return []
        
        target_features = self.prepare_features(target_land)
        
        all_lands = Land.objects.exclude(id=land_id).filter(status='available')
        similarities = []
        
        for land in all_lands:
            land_features = self.prepare_features(land)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                target_features.reshape(1, -1),
                land_features.reshape(1, -1)
            )[0][0]
            
            similarities.append({
                'land_id': land.id,
                'name': land.name,
                'city': land.city,
                'similarity_score': round(similarity * 100, 2),
                'size_in_acres': float(land.size_in_acres),
                'total_price': float(land.total_price),
            })
        
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similarities[:limit]


# Example usage function
def example_usage():
    """
    Example of how to use the recommendation model
    """
    recommender = LandRecommendationModel()
    
    # Example user requirements
    user_requirements = {
        'purpose': 'agricultural',
        'min_size': 10,
        'max_size': 50,
        'min_price': 500000,
        'max_price': 5000000,
        'location_preference': 'Pune',
        'connectivity_importance': 0.8,
        'infrastructure_importance': 0.7,
    }
    
    # Get recommendations
    recommendations = recommender.recommend_lands(user_requirements, limit=10)
    
    print("\n🎯 Top Recommendations:\n")
    for idx, rec in enumerate(recommendations[:5], 1):
        print(f"{idx}. {rec['name']} ({rec['city']})")
        print(f"   Score: {rec['score']}/100 - {rec['recommendation_level']}")
        print(f"   Size: {rec['size_in_acres']} acres | Price: ₹{rec['total_price']:,.0f}")
        print(f"   ✓ {', '.join(rec['matching_features'][:2])}")
        if rec['concerns']:
            print(f"   ⚠ {rec['concerns'][0]}")
        print()
    
    return recommendations