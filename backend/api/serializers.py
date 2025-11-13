from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Land  # , LandImage, Infrastructure, GovernmentProject - COMMENTED OUT

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile information"""
    full_name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'initials', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
    
    def get_full_name(self, obj):
        """Get user's full name or username if name not set"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        else:
            return obj.username
    
    def get_initials(self, obj):
        """Get user initials for avatar"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name[0]}{obj.last_name[0]}".upper()
        elif obj.first_name:
            return obj.first_name[0:2].upper()
        else:
            return obj.username[0:2].upper()


# COMMENTED OUT - LandImage not currently used
# class LandImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LandImage
#         fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']


class LandSerializer(serializers.ModelSerializer):
    """Serializer for Land model"""
    # images = LandImageSerializer(many=True, read_only=True)  # COMMENTED OUT
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    # Computed fields
    avg_connectivity = serializers.SerializerMethodField()
    infrastructure_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Land
        fields = [
            'id', 'name', 'description', 'land_type', 'status',
            'latitude', 'longitude', 'address', 'city', 'state', 'pincode',
            'size_in_acres', 'price_per_acre', 'total_price',
            'highway_proximity_score', 'metro_proximity_score', 'airport_proximity_score',
            'has_water_supply', 'has_electricity', 'has_road_access',
            'owner', 'owner_username', 'created_at', 'updated_at',
            'slug', 'is_featured', 'views_count',
            # 'images',  # COMMENTED OUT
            'avg_connectivity', 'infrastructure_available'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count', 'slug']
    
    def get_avg_connectivity(self, obj):
        """Calculate average connectivity score"""
        return round((obj.highway_proximity_score + 
                     obj.metro_proximity_score + 
                     obj.airport_proximity_score) / 3, 2)
    
    def get_infrastructure_available(self, obj):
        """Get list of available infrastructure"""
        available = []
        if obj.has_water_supply:
            available.append('Water Supply')
        if obj.has_electricity:
            available.append('Electricity')
        if obj.has_road_access:
            available.append('Road Access')
        return available


class LandListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for land listing"""
    avg_connectivity = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Land
        fields = [
            'id', 'name', 'land_type', 'status',
            'city', 'state',
            'size_in_acres', 'price_per_acre', 'total_price',
            'avg_connectivity', 'is_featured', 'primary_image'
        ]
    
    def get_avg_connectivity(self, obj):
        return round((obj.highway_proximity_score + 
                     obj.metro_proximity_score + 
                     obj.airport_proximity_score) / 3, 2)
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return {
                'url': primary.image.url if primary.image else None,
                'caption': primary.caption
            }
        return None


class LandRecommendationSerializer(serializers.Serializer):
    """Serializer for recommendation results"""
    land_id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    size_in_acres = serializers.FloatField()
    total_price = serializers.FloatField()
    price_per_acre = serializers.FloatField()
    score = serializers.FloatField()
    subscores = serializers.DictField()
    matching_features = serializers.ListField(child=serializers.CharField())
    concerns = serializers.ListField(child=serializers.CharField())
    recommendation_level = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


# COMMENTED OUT - Advanced features not currently needed
# class InfrastructureSerializer(serializers.ModelSerializer):
#     """Serializer for Infrastructure"""
#     infra_type_display = serializers.CharField(source='get_infra_type_display', read_only=True)
#     
#     class Meta:
#         model = Infrastructure
#         fields = [
#             'id', 'name', 'infra_type', 'infra_type_display',
#             'latitude', 'longitude', 'address', 'city',
#             'description', 'capacity', 'is_operational', 'established_year'
#         ]


# class GovernmentProjectSerializer(serializers.ModelSerializer):
#     """Serializer for Government Projects"""
#     project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
#     status_display = serializers.CharField(source='get_status_display', read_only=True)
#     
#     class Meta:
#         model = GovernmentProject
#         fields = [
#             'id', 'name', 'project_type', 'project_type_display',
#             'status', 'status_display',
#             'latitude', 'longitude', 'radius_km', 'city', 'state',
#             'description', 'budget_crores', 'start_date', 'completion_date',
#             'expected_land_appreciation', 'source_url', 'last_updated'
#         ]


# class UserRequirementsSerializer(serializers.Serializer):
#     """Serializer for user search requirements"""
#     purpose = serializers.CharField(required=False, allow_blank=True)
#     min_size = serializers.FloatField(default=0)
#     max_size = serializers.FloatField(default=10000)
#     min_price = serializers.FloatField(default=0)
#     max_price = serializers.FloatField(default=100000000)
#     location = serializers.CharField(required=False, allow_blank=True)
#     connectivity_importance = serializers.FloatField(default=0.5, min_value=0, max_value=1)
#     infrastructure_importance = serializers.FloatField(default=0.5, min_value=0, max_value=1)
#     limit = serializers.IntegerField(default=10, min_value=1, max_value=50)


# ============================================
# CROP RECOMMENDATION SERIALIZERS
# ============================================

from .models import SoilData, CropRecommendation

class SoilDataSerializer(serializers.ModelSerializer):
    """Serializer for soil test data"""
    land_name = serializers.CharField(source='land.name', read_only=True)
    
    class Meta:
        model = SoilData
        fields = [
            'id', 'land', 'land_name', 'user',
            'nitrogen', 'phosphorous', 'potassium', 'ph',
            'temperature', 'humidity', 'rainfall',
            'location', 'test_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'test_date', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Auto-assign user from request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CropRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for crop recommendation results"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    confidence_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = CropRecommendation
        fields = [
            'id', 'user', 'user_name', 'soil_data',
            'recommended_crop', 'confidence_score', 'confidence_percentage',
            'top_recommendations', 'soil_suitability',
            'created_at', 'model_version'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_confidence_percentage(self, obj):
        return obj.get_confidence_percentage()


class CropRecommendationRequestSerializer(serializers.Serializer):
    """Serializer for crop recommendation API request"""
    N = serializers.FloatField(min_value=0, max_value=200, help_text="Nitrogen (mg/kg)")
    P = serializers.FloatField(min_value=0, max_value=200, help_text="Phosphorous (mg/kg)")
    K = serializers.FloatField(min_value=0, max_value=250, help_text="Potassium (mg/kg)")
    temperature = serializers.FloatField(min_value=-10, max_value=50, help_text="Temperature (°C)")
    humidity = serializers.FloatField(min_value=0, max_value=100, help_text="Humidity (%)")
    ph = serializers.FloatField(min_value=0, max_value=14, help_text="pH value")
    rainfall = serializers.FloatField(min_value=0, max_value=3500, help_text="Rainfall (mm)")
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    land_id = serializers.IntegerField(required=False, allow_null=True)


class CropRequirementsSerializer(serializers.Serializer):
    """Serializer for crop growing requirements"""
    crop_name = serializers.CharField()
    optimal_conditions = serializers.DictField()
    samples_count = serializers.IntegerField()