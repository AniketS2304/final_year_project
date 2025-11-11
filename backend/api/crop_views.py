# backend/api/crop_views.py
"""
API Views for Crop Recommendation Feature
Uses ML model to recommend crops based on soil and climate data
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import SoilData, CropRecommendation, Land
from .serializers import (
    SoilDataSerializer, 
    CropRecommendationSerializer,
    CropRecommendationRequestSerializer,
    CropRequirementsSerializer
)
import time


class CropRecommendationAPI(APIView):
    """
    POST /api/crops/recommend/
    Get crop recommendations based on soil and climate parameters
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        start_time = time.time()
        
        try:
            # Validate input data
            serializer = CropRecommendationRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data = serializer.validated_data
            
            # Import ML model
            try:
                from .services.crop_recommender import CropRecommendationModel
            except Exception as e:
                return Response({
                    'error': f'Crop recommender not available: {str(e)}'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            # Get recommendation from ML model
            recommender = CropRecommendationModel()
            result = recommender.recommend_crop(
                N=data['N'],
                P=data['P'],
                K=data['K'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                ph=data['ph'],
                rainfall=data['rainfall']
            )
            
            # Save soil data if land_id provided
            soil_data = None
            if 'land_id' in data and data['land_id']:
                try:
                    land = get_object_or_404(Land, id=data['land_id'])
                    soil_data = SoilData.objects.create(
                        land=land,
                        user=request.user,
                        nitrogen=data['N'],
                        phosphorous=data['P'],
                        potassium=data['K'],
                        ph=data['ph'],
                        temperature=data['temperature'],
                        humidity=data['humidity'],
                        rainfall=data['rainfall'],
                        location=data.get('location', land.city)
                    )
                except Exception as e:
                    print(f"Error saving soil data: {e}")
            else:
                # Create soil data without land
                soil_data = SoilData.objects.create(
                    user=request.user,
                    nitrogen=data['N'],
                    phosphorous=data['P'],
                    potassium=data['K'],
                    ph=data['ph'],
                    temperature=data['temperature'],
                    humidity=data['humidity'],
                    rainfall=data['rainfall'],
                    location=data.get('location', '')
                )
            
            # Save recommendation
            crop_recommendation = CropRecommendation.objects.create(
                user=request.user,
                soil_data=soil_data,
                recommended_crop=result['recommended_crop'],
                confidence_score=result['confidence'],
                top_recommendations=result['top_5_recommendations'],
                soil_suitability=self._get_soil_suitability(result['confidence'])
            )
            
            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)
            
            return Response({
                'success': True,
                'response_time_ms': response_time,
                'recommendation': {
                    'id': crop_recommendation.id,
                    'recommended_crop': result['recommended_crop'],
                    'confidence': result['confidence'],
                    'confidence_percentage': f"{result['confidence'] * 100:.2f}%",
                    'top_5_recommendations': result['top_5_recommendations'],
                    'soil_suitability': crop_recommendation.soil_suitability,
                },
                'input_data': {
                    'nitrogen': data['N'],
                    'phosphorous': data['P'],
                    'potassium': data['K'],
                    'temperature': data['temperature'],
                    'humidity': data['humidity'],
                    'ph': data['ph'],
                    'rainfall': data['rainfall'],
                }
            })
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error in CropRecommendationAPI: {error_trace}")
            return Response({
                'error': f'Internal server error: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_soil_suitability(self, confidence: float) -> str:
        """Convert confidence to soil suitability rating"""
        if confidence >= 0.8:
            return 'excellent'
        elif confidence >= 0.6:
            return 'good'
        elif confidence >= 0.4:
            return 'moderate'
        else:
            return 'poor'


class CropRequirementsAPI(APIView):
    """
    GET /api/crops/{crop_name}/requirements/
    Get optimal growing conditions for a specific crop
    """
    permission_classes = [AllowAny]
    
    def get(self, request, crop_name):
        try:
            from .services.crop_recommender import CropRecommendationModel
        except Exception as e:
            return Response({
                'error': f'Crop recommender not available: {str(e)}'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        recommender = CropRecommendationModel()
        requirements = recommender.get_crop_requirements(crop_name)
        
        if 'error' in requirements:
            return Response(requirements, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CropRequirementsSerializer(requirements)
        return Response({
            'success': True,
            'data': serializer.data
        })


class AvailableCropsAPI(APIView):
    """
    GET /api/crops/available/
    Get list of all available crops in the database
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            from .services.crop_recommender import CropRecommendationModel
        except Exception as e:
            return Response({
                'error': f'Crop recommender not available: {str(e)}'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        recommender = CropRecommendationModel()
        crops = recommender.get_all_crops()
        
        return Response({
            'success': True,
            'count': len(crops),
            'crops': crops
        })


class UserCropHistoryAPI(APIView):
    """
    GET /api/user/crop-recommendations/
    Get user's crop recommendation history
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        recommendations = CropRecommendation.objects.filter(
            user=request.user
        ).order_by('-created_at')[:20]
        
        serializer = CropRecommendationSerializer(recommendations, many=True)
        
        return Response({
            'success': True,
            'count': len(recommendations),
            'recommendations': serializer.data
        })


class SoilDataAPI(APIView):
    """
    GET /api/soil-data/ - List all soil test data
    POST /api/soil-data/ - Create new soil test data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's soil test data"""
        soil_tests = SoilData.objects.filter(user=request.user).order_by('-created_at')
        serializer = SoilDataSerializer(soil_tests, many=True)
        
        return Response({
            'success': True,
            'count': len(soil_tests),
            'soil_tests': serializer.data
        })
    
    def post(self, request):
        """Save new soil test data"""
        serializer = SoilDataSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Soil data saved successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CropRecommendationStatsAPI(APIView):
    """
    GET /api/crops/stats/
    Get statistics about user's crop recommendations
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        recommendations = CropRecommendation.objects.filter(user=request.user)
        
        # Count by crop
        from django.db.models import Count
        crop_counts = recommendations.values('recommended_crop').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Average confidence
        from django.db.models import Avg
        avg_confidence = recommendations.aggregate(Avg('confidence_score'))['confidence_score__avg']
        
        return Response({
            'success': True,
            'stats': {
                'total_recommendations': recommendations.count(),
                'avg_confidence': round(avg_confidence * 100, 2) if avg_confidence else 0,
                'most_recommended_crops': list(crop_counts),
                'last_recommendation': recommendations.first().created_at if recommendations.exists() else None
            }
        })
