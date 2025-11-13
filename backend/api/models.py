
# Create your models here.
# backend/api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    """Extended user model with additional fields for AgriWise"""
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('investor', 'Investor'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='farmer',
        help_text='Type of user account'
    )
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text='User biography')
    is_verified = models.BooleanField(default=False, help_text='Email/Phone verified')
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Land(models.Model):
    """Core land/property data"""
    LAND_TYPE_CHOICES = [
        ('agricultural', 'Agricultural'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('mixed', 'Mixed Use'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
        ('reserved', 'Reserved'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    land_type = models.CharField(max_length=20, choices=LAND_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Size & Price
    size_in_acres = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_acre = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Connectivity Scores (0-100)
    highway_proximity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    metro_proximity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    airport_proximity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    
    # Infrastructure Nearby (boolean flags)
    has_water_supply = models.BooleanField(default=False)
    has_electricity = models.BooleanField(default=False)
    has_road_access = models.BooleanField(default=True)
    
    # Metadata
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='lands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO & Search
    slug = models.SlugField(unique=True, blank=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'land_type']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class UserQuery(models.Model):
    """Track semantic search queries for analytics"""
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    query_text = models.TextField()
    query_type = models.CharField(max_length=50)  # 'land_potential', 'roi_estimate', 'semantic_search'
    
    # Results
    results_count = models.IntegerField(default=0)
    top_result_id = models.IntegerField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user or 'Anonymous'}: {self.query_text[:50]}"


class SavedLand(models.Model):
    """User's saved/favorite lands"""
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='saved_lands')
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'land']
    
    def __str__(self):
        return f"{self.user.username} saved {self.land.name}"


# ============================================
# CROP RECOMMENDATION MODELS
# ============================================

class SoilData(models.Model):
    """Soil analysis data for lands"""
    land = models.OneToOneField(Land, on_delete=models.CASCADE, related_name='soil_data', null=True, blank=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='soil_tests')
    
    # NPK Values (mg/kg)
    nitrogen = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        help_text="Nitrogen content in mg/kg (0-200)"
    )
    phosphorous = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        help_text="Phosphorous content in mg/kg (0-200)"
    )
    potassium = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        help_text="Potassium content in mg/kg (0-250)"
    )
    
    # Soil Properties
    ph = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        help_text="pH value of soil (0-14)"
    )
    
    # Climate Data
    temperature = models.FloatField(
        validators=[MinValueValidator(-10), MaxValueValidator(50)],
        help_text="Average temperature in Celsius"
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Relative humidity in percentage"
    )
    rainfall = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(3500)],
        help_text="Annual rainfall in mm"
    )
    
    # Metadata
    location = models.CharField(max_length=255, blank=True)
    test_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Soil Data'
        verbose_name_plural = 'Soil Data'
    
    def __str__(self):
        if self.land:
            return f"Soil data for {self.land.name}"
        return f"Soil test by {self.user.username} on {self.test_date}"


class CropRecommendation(models.Model):
    """Store crop recommendations generated by ML model"""
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='crop_recommendations')
    soil_data = models.ForeignKey(SoilData, on_delete=models.CASCADE, related_name='recommendations')
    
    # ML Model Results
    recommended_crop = models.CharField(max_length=100)
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Model confidence (0-1)"
    )
    
    # Top 5 alternatives stored as JSON
    top_recommendations = models.JSONField(
        default=list,
        help_text="List of top 5 crop recommendations with confidence scores"
    )
    
    # Additional Analysis
    soil_suitability = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('moderate', 'Moderate'),
            ('poor', 'Poor'),
        ],
        default='good'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default='v1.0')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recommended_crop} for {self.user.username} ({self.confidence_score * 100:.1f}%)"
    
    def get_confidence_percentage(self):
        """Get confidence as percentage"""
        return round(self.confidence_score * 100, 2)