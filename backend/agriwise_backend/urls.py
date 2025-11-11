"""
URL configuration for agriwise_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import (
    RegisterAPI, LoginAPI, UserProfileAPI,
    LandRecommendationAPI, SimilarLandsAPI, 
    LandDetailWithScoreAPI, QuickMatchAPI,
    # RecommendationStatsAPI  # COMMENTED OUT
)
from api.crop_views import (
    CropRecommendationAPI, CropRequirementsAPI, AvailableCropsAPI,
    UserCropHistoryAPI, SoilDataAPI, CropRecommendationStatsAPI
)
from api.password_reset_views import PasswordResetRequestAPI, PasswordResetConfirmAPI

urlpatterns = [
    # Authentication
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/user/profile/', UserProfileAPI.as_view(), name='user-profile'),
    path('admin/', admin.site.urls),
    
    # Land Recommendations
    path('api/lands/recommend/', LandRecommendationAPI.as_view(), name='land-recommend'),
    path('api/lands/<int:land_id>/similar/', SimilarLandsAPI.as_view(), name='similar-lands'),
    path('api/lands/<int:land_id>/score/', LandDetailWithScoreAPI.as_view(), name='land-score'),
    path('api/lands/quick-match/', QuickMatchAPI.as_view(), name='quick-match'),
    
    # Crop Recommendations (NEW!)
    path('api/crops/recommend/', CropRecommendationAPI.as_view(), name='crop-recommend'),
    path('api/crops/<str:crop_name>/requirements/', CropRequirementsAPI.as_view(), name='crop-requirements'),
    path('api/crops/available/', AvailableCropsAPI.as_view(), name='available-crops'),
    path('api/crops/stats/', CropRecommendationStatsAPI.as_view(), name='crop-stats'),
    path('api/user/crop-recommendations/', UserCropHistoryAPI.as_view(), name='user-crop-history'),
    path('api/soil-data/', SoilDataAPI.as_view(), name='soil-data'),
    
    # Password Reset endpoints
    path('api/password-reset/', PasswordResetRequestAPI.as_view(), name='password-reset-request'),
    path('api/password-reset/confirm/', PasswordResetConfirmAPI.as_view(), name='password-reset-confirm'),
    
    # Stats - COMMENTED OUT
    # path('api/recommendations/stats/', RecommendationStatsAPI.as_view(), name='recommendation-stats'),
]
