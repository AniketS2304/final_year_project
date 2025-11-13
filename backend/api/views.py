from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.views import APIView

User = get_user_model()

# ------------------------
# Register API
# ------------------------
class RegisterAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("post api hitted")
        try:
            print('in try')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data.get('email', '')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create user and token
            user = User.objects.create_user(username=username, email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {"user": {"username": user.username, "email": user.email}, "token": token.key},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# Login API
# ------------------------
class LoginAPI(ObtainAuthToken):
    # print('login_api')
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username
        })


# ------------------------
# User Profile API
# ------------------------
class UserProfileAPI(APIView):
    """
    GET /api/user/profile/ - Get current user's profile
    PUT /api/user/profile/ - Update current user's profile
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user's profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update current user's profile"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# backend/api/views.py (Land recommendation views)

from django.shortcuts import get_object_or_404
from .models import Land, UserQuery
# Import the ML recommender lazily inside view methods to avoid import-time
# failures when optional packages (pandas/sklearn/...) are not available.
from .serializers import LandSerializer, LandRecommendationSerializer
import time

class LandRecommendationAPI(APIView):
    """
    POST /api/lands/recommend/
    Get personalized land recommendations based on user requirements
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        start_time = time.time()
        
        try:
            # Extract user requirements from request
            user_requirements = {
                'purpose': request.data.get('purpose', ''),
                'min_size': float(request.data.get('min_size', 0)),
                'max_size': float(request.data.get('max_size', 10000)),
                'min_price': float(request.data.get('min_price', 0)),
                'max_price': float(request.data.get('max_price', 100000000)),
                'location_preference': request.data.get('location_preference', '') or request.data.get('location', ''),
                'connectivity_importance': float(request.data.get('connectivity_importance', 0.5)),
                'infrastructure_importance': float(request.data.get('infrastructure_importance', 0.5)),
            }
            
            # Validate inputs
            if user_requirements['min_size'] > user_requirements['max_size']:
                return Response(
                    {'error': 'min_size cannot be greater than max_size'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user_requirements['min_price'] > user_requirements['max_price']:
                return Response(
                    {'error': 'min_price cannot be greater than max_price'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Import recommender lazily to avoid heavy imports at module load
            try:
                from .services.land_recommender import LandRecommendationModel
            except Exception as e:
                return Response({'error': f'Recommender not available: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # Get recommendations
            recommender = LandRecommendationModel()
            limit = request.data.get('limit', 10)
            recommendations = recommender.recommend_lands(user_requirements, limit=limit)
            
            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)
            
            # Log query for analytics
            try:
                UserQuery.objects.create(
                    user=request.user,
                    query_text=f"Land recommendation: {user_requirements.get('purpose', 'any')} in {user_requirements.get('location_preference', 'any location')}",
                    query_type='land_recommendation',
                    results_count=len(recommendations),
                    top_result_id=recommendations[0]['land_id'] if recommendations else None,
                    response_time_ms=response_time
                )
            except Exception as log_error:
                # Don't fail the request if logging fails
                print(f"Failed to log query: {log_error}")
            
            return Response({
                'success': True,
                'count': len(recommendations),
                'response_time_ms': response_time,
                'recommendations': recommendations,
                'search_criteria': user_requirements
            })
        
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error in LandRecommendationAPI: {error_trace}")
            return Response({
                'error': f'Internal server error: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SimilarLandsAPI(APIView):
    """
    GET /api/lands/{id}/similar/
    Find lands similar to a specific land
    """
    permission_classes = [AllowAny]
    
    def get(self, request, land_id):
        # Check if land exists
        land = get_object_or_404(Land, id=land_id)
        
        # Get similar lands (import recommender lazily)
        try:
            from .services.land_recommender import LandRecommendationModel
        except Exception as e:
            return Response({'error': f'Recommender not available: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        recommender = LandRecommendationModel()
        limit = int(request.query_params.get('limit', 5))
        similar_lands = recommender.get_similar_lands(land_id, limit=limit)
        
        return Response({
            'success': True,
            'reference_land': {
                'id': land.id,
                'name': land.name,
                'city': land.city,
            },
            'similar_lands': similar_lands,
            'count': len(similar_lands)
        })


class LandDetailWithScoreAPI(APIView):
    """
    POST /api/lands/{id}/score/
    Calculate suitability score for a specific land based on user requirements
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, land_id):
        land = get_object_or_404(Land, id=land_id)
        
        user_requirements = {
            'purpose': request.data.get('purpose', ''),
            'min_size': float(request.data.get('min_size', 0)),
            'max_size': float(request.data.get('max_size', 10000)),
            'min_price': float(request.data.get('min_price', 0)),
            'max_price': float(request.data.get('max_price', 100000000)),
            'location_preference': request.data.get('location', ''),
            'connectivity_importance': float(request.data.get('connectivity_importance', 0.5)),
            'infrastructure_importance': float(request.data.get('infrastructure_importance', 0.5)),
        }
        
        try:
            from .services.land_recommender import LandRecommendationModel
        except Exception as e:
            return Response({'error': f'Recommender not available: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        recommender = LandRecommendationModel()
        score_data = recommender.calculate_suitability_score(land, user_requirements)
        
        return Response({
            'success': True,
            'land': LandSerializer(land).data,
            'suitability_analysis': score_data
        })


class QuickMatchAPI(APIView):
    """
    GET /api/lands/quick-match/?purpose=agricultural&budget=5000000&location=Pune
    Quick match endpoint for simple searches
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        purpose = request.query_params.get('purpose', '')
        budget = float(request.query_params.get('budget', 10000000))
        location = request.query_params.get('location', '')
        size = float(request.query_params.get('size', 0))
        
        user_requirements = {
            'purpose': purpose,
            'min_size': size * 0.8 if size > 0 else 0,
            'max_size': size * 1.2 if size > 0 else 10000,
            'min_price': 0,
            'max_price': budget,
            'location_preference': location,
            'connectivity_importance': 0.5,
            'infrastructure_importance': 0.5,
        }
        
        try:
            from .services.land_recommender import LandRecommendationModel
        except Exception as e:
            return Response({'error': f'Recommender not available: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        recommender = LandRecommendationModel()
        recommendations = recommender.recommend_lands(user_requirements, limit=5)
        
        return Response({
            'success': True,
            'count': len(recommendations),
            'recommendations': recommendations
        })


# COMMENTED OUT - Advanced feature not currently needed
# class RecommendationStatsAPI(APIView):
#     """
#     GET /api/recommendations/stats/
#     Get statistics about recommendations
#     """
#     permission_classes = [IsAuthenticated]
#     
#     def get(self, request):
#         # ensure `models` is available for aggregation
#         from django.db import models
# 
#         user_queries = UserQuery.objects.filter(
#             user=request.user,
#             query_type='land_recommendation'
#         )
#         
#         total_searches = user_queries.count()
#         avg_response_time = user_queries.aggregate(
#             avg_time=models.Avg('response_time_ms')
#         )['avg_time'] or 0
#         
#         # Most searched criteria
#         popular_purposes = Land.objects.filter(
#             id__in=user_queries.values_list('top_result_id', flat=True)
#         ).values('land_type').annotate(
#             count=models.Count('id')
#         ).order_by('-count')[:5]
#         
#         return Response({
#             'total_searches': total_searches,
#             'avg_response_time_ms': round(avg_response_time, 2),
#             'popular_land_types': list(popular_purposes),
#             'last_search': user_queries.last().created_at if user_queries.exists() else None
#         })