# backend/api/services/crop_recommender.py
"""
Crop Recommendation ML Model
Uses Random Forest Classifier to recommend crops based on soil and climate data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class CropRecommendationModel:
    """
    Machine Learning model for crop recommendation
    Input: N, P, K, temperature, humidity, pH, rainfall
    Output: Recommended crop with confidence score
    """
    
    def __init__(self):
        self.model_dir = 'ml_models'
        self.model_path = os.path.join(self.model_dir, 'crop_model.pkl')
        self.scaler_path = os.path.join(self.model_dir, 'crop_scaler.pkl')
        self.label_encoder_path = os.path.join(self.model_dir, 'crop_label_encoder.pkl')
        
        self.model = None
        self.scaler = None
        self.label_encoder = None
        
        # Load or train model
        self._load_or_train()
    
    def _load_or_train(self):
        """Load existing model or train new one"""
        if self._model_exists():
            self._load_model()
            print("✅ Loaded existing crop recommendation model")
        else:
            print("🔄 Training new crop recommendation model...")
            self._train_model()
            print("✅ Model trained and saved")
    
    def _model_exists(self) -> bool:
        """Check if model files exist"""
        return (os.path.exists(self.model_path) and 
                os.path.exists(self.scaler_path) and
                os.path.exists(self.label_encoder_path))
    
    def _load_model(self):
        """Load saved model"""
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.label_encoder = joblib.load(self.label_encoder_path)
    
    def _train_model(self):
        """Train the ML model on crop dataset"""
        
        # Load dataset
        # dataset_path = os.path.join('datasets', 'crop_recommendation.csv')
        dataset_path = os.path.join('datasets', 'Crop_recommendation_real.csv')
        
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(
                f"Dataset not found at {dataset_path}. "
                "Please ensure crop_recommendation.csv is in the datasets folder."
            )
        
        # Read data
        df = pd.read_csv(dataset_path)
        
        print(f"📊 Dataset loaded: {len(df)} samples, {len(df['label'].unique())} crops")
        
        # Prepare features and labels
        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        print("🔄 Training model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
        
        # Save model
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        joblib.dump(self.label_encoder, self.label_encoder_path)
        
        print(f"💾 Model saved to {self.model_path}")
    
    def recommend_crop(self, N: float, P: float, K: float, 
                      temperature: float, humidity: float, 
                      ph: float, rainfall: float) -> Dict:
        """
        Recommend a crop based on soil and climate parameters
        
        Args:
            N: Nitrogen content (mg/kg)
            P: Phosphorous content (mg/kg)
            K: Potassium content (mg/kg)
            temperature: Temperature in Celsius
            humidity: Relative humidity (%)
            ph: pH value of soil
            rainfall: Rainfall in mm
        
        Returns:
            {
                'crop': 'rice',
                'confidence': 0.95,
                'top_5_crops': [('rice', 0.95), ('wheat', 0.03), ...]
            }
        """
        
        # Prepare input
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        features_scaled = self.scaler.transform(features)
        
        # Get prediction
        prediction = self.model.predict(features_scaled)[0]
        predicted_crop = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get confidence scores for all crops
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get top 5 crops with probabilities
        top_indices = np.argsort(probabilities)[::-1][:5]
        top_crops = [
            {
                'crop': self.label_encoder.inverse_transform([idx])[0],
                'confidence': float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        return {
            'recommended_crop': predicted_crop,
            'confidence': float(probabilities[prediction]),
            'top_5_recommendations': top_crops
        }
    
    def recommend_crops_batch(self, soil_climate_data: List[Dict]) -> List[Dict]:
        """
        Recommend crops for multiple locations/conditions
        
        Args:
            soil_climate_data: List of dicts with N, P, K, temp, humidity, ph, rainfall
        
        Returns:
            List of recommendation results
        """
        results = []
        
        for data in soil_climate_data:
            recommendation = self.recommend_crop(
                N=data['N'],
                P=data['P'],
                K=data['K'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                ph=data['ph'],
                rainfall=data['rainfall']
            )
            recommendation['input_data'] = data
            results.append(recommendation)
        
        return results
    
    def get_crop_requirements(self, crop_name: str) -> Dict:
        """
        Get optimal conditions for a specific crop
        
        Args:
            crop_name: Name of the crop
        
        Returns:
            Dictionary with optimal parameter ranges
        """
        
        dataset_path = os.path.join('datasets', 'Crop_recommendation_real.csv')
        df = pd.read_csv(dataset_path)
        
        # Filter data for the specific crop
        crop_data = df[df['label'].str.lower() == crop_name.lower()]
        
        if len(crop_data) == 0:
            return {'error': f'Crop "{crop_name}" not found in database'}
        
        # Calculate statistics
        requirements = {
            'crop_name': crop_name,
            'optimal_conditions': {
                'nitrogen': {
                    'min': float(crop_data['N'].min()),
                    'max': float(crop_data['N'].max()),
                    'avg': float(crop_data['N'].mean()),
                },
                'phosphorous': {
                    'min': float(crop_data['P'].min()),
                    'max': float(crop_data['P'].max()),
                    'avg': float(crop_data['P'].mean()),
                },
                'potassium': {
                    'min': float(crop_data['K'].min()),
                    'max': float(crop_data['K'].max()),
                    'avg': float(crop_data['K'].mean()),
                },
                'temperature': {
                    'min': float(crop_data['temperature'].min()),
                    'max': float(crop_data['temperature'].max()),
                    'avg': float(crop_data['temperature'].mean()),
                },
                'humidity': {
                    'min': float(crop_data['humidity'].min()),
                    'max': float(crop_data['humidity'].max()),
                    'avg': float(crop_data['humidity'].mean()),
                },
                'ph': {
                    'min': float(crop_data['ph'].min()),
                    'max': float(crop_data['ph'].max()),
                    'avg': float(crop_data['ph'].mean()),
                },
                'rainfall': {
                    'min': float(crop_data['rainfall'].min()),
                    'max': float(crop_data['rainfall'].max()),
                    'avg': float(crop_data['rainfall'].mean()),
                }
            },
            'samples_count': len(crop_data)
        }
        
        return requirements
    
    def get_all_crops(self) -> List[str]:
        """Get list of all crops in the dataset"""
        dataset_path = os.path.join('datasets', 'Crop_recommendation_real.csv')
        df = pd.read_csv(dataset_path)
        return sorted(df['label'].unique().tolist())
    
    def retrain_model(self):
        """Retrain the model (useful after adding more data)"""
        print("🔄 Retraining model...")
        self._train_model()
        print("✅ Model retrained successfully")


def test_crop_recommender():
    """Test function for the crop recommender"""
    
    print("=" * 80)
    print("🌾 TESTING CROP RECOMMENDATION MODEL")
    print("=" * 80)
    
    recommender = CropRecommendationModel()
    
    # Test Case 1: Rice-friendly conditions
    print("\n📍 TEST 1: Rice-friendly soil (high NPK, warm, humid)")
    print("-" * 80)
    
    result = recommender.recommend_crop(
        N=90, P=42, K=43,
        temperature=21, humidity=82,
        ph=6.5, rainfall=202
    )
    
    print(f"✅ Recommended Crop: {result['recommended_crop']}")
    print(f"⭐ Confidence: {result['confidence'] * 100:.2f}%")
    print(f"\n📊 Top 5 Recommendations:")
    for i, crop in enumerate(result['top_5_recommendations'], 1):
        print(f"   {i}. {crop['crop']:15s} - {crop['confidence'] * 100:.2f}%")
    
    # Test Case 2: Different conditions
    print("\n\n📍 TEST 2: Different soil conditions")
    print("-" * 80)
    
    result2 = recommender.recommend_crop(
        N=20, P=67, K=70,
        temperature=24, humidity=60,
        ph=5.6, rainfall=64
    )
    
    print(f"✅ Recommended Crop: {result2['recommended_crop']}")
    print(f"⭐ Confidence: {result2['confidence'] * 100:.2f}%")
    
    # Test Case 3: Get crop requirements
    print("\n\n📍 TEST 3: Get optimal conditions for 'rice'")
    print("-" * 80)
    
    requirements = recommender.get_crop_requirements('rice')
    print(f"Crop: {requirements['crop_name']}")
    print(f"Samples in dataset: {requirements['samples_count']}")
    print(f"\nOptimal Conditions:")
    for param, values in requirements['optimal_conditions'].items():
        print(f"  {param:12s}: {values['min']:.1f} - {values['max']:.1f} (avg: {values['avg']:.1f})")
    
    # Test Case 4: List all crops
    print("\n\n📍 TEST 4: Available crops in database")
    print("-" * 80)
    crops = recommender.get_all_crops()
    print(f"Total crops: {len(crops)}")
    print(f"Crops: {', '.join(crops)}")
    
    print("\n" + "=" * 80)
    print("✅ TESTING COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    test_crop_recommender()
