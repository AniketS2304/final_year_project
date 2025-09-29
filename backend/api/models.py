
# Create your models here.
# backend/api/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================
# LAND & PROPERTY MODELS
# ============================================

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lands')
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


class LandImage(models.Model):
    """Multiple images per land"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='land_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']


# ============================================
# INFRASTRUCTURE & DEVELOPMENT DATA
# ============================================

class Infrastructure(models.Model):
    """Nearby infrastructure (hospitals, schools, malls, etc.)"""
    INFRA_TYPE_CHOICES = [
        ('hospital', 'Hospital'),
        ('school', 'School'),
        ('college', 'College/University'),
        ('mall', 'Shopping Mall'),
        ('metro', 'Metro Station'),
        ('airport', 'Airport'),
        ('highway', 'Highway'),
        ('it_park', 'IT Park'),
        ('sez', 'SEZ'),
        ('industrial', 'Industrial Area'),
        ('railway', 'Railway Station'),
    ]
    
    name = models.CharField(max_length=255)
    infra_type = models.CharField(max_length=20, choices=INFRA_TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    # Metadata
    description = models.TextField(blank=True)
    capacity = models.CharField(max_length=100, blank=True)  # e.g., "500 beds", "2000 students"
    is_operational = models.BooleanField(default=True)
    established_year = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['city', 'infra_type']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_infra_type_display()})"


class GovernmentProject(models.Model):
    """Government development projects (metro, highways, smart city, etc.)"""
    PROJECT_TYPE_CHOICES = [
        ('metro', 'Metro/Rail'),
        ('highway', 'Highway/Expressway'),
        ('smart_city', 'Smart City'),
        ('sez', 'Special Economic Zone'),
        ('airport', 'Airport'),
        ('port', 'Port'),
        ('it_corridor', 'IT Corridor'),
        ('industrial_park', 'Industrial Park'),
    ]
    
    STATUS_CHOICES = [
        ('announced', 'Announced'),
        ('planned', 'Planned'),
        ('under_construction', 'Under Construction'),
        ('operational', 'Operational'),
        ('delayed', 'Delayed'),
    ]
    
    name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Location (can be a line/polygon, but simplified as point + radius)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius_km = models.DecimalField(max_digits=6, decimal_places=2, default=5.0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    # Details
    description = models.TextField()
    budget_crores = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Impact
    expected_land_appreciation = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True,
        help_text="Expected % appreciation in nearby land value"
    )
    
    # Sources
    source_url = models.URLField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


# ============================================
# INVESTMENT INSIGHTS & RECOMMENDATIONS
# ============================================

class DevelopmentUseCase(models.Model):
    """Possible development types for land"""
    USE_CASE_CHOICES = [
        ('residential', 'Residential Complex'),
        ('commercial', 'Commercial Building/Mall'),
        ('industrial', 'Industrial/Warehouse'),
        ('it_park', 'IT Park/Tech Hub'),
        ('hospitality', 'Hotel/Resort'),
        ('education', 'School/College/Hostel'),
        ('healthcare', 'Hospital/Clinic'),
        ('logistics', 'Logistics Hub'),
        ('mixed', 'Mixed-Use Development'),
        ('agricultural', 'Agricultural/Farm'),
    ]
    
    name = models.CharField(max_length=100, choices=USE_CASE_CHOICES, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='building')  # For frontend
    
    # Requirements
    min_size_acres = models.DecimalField(max_digits=6, decimal_places=2)
    typical_roi_min = models.DecimalField(max_digits=5, decimal_places=2)
    typical_roi_max = models.DecimalField(max_digits=5, decimal_places=2)
    investment_range_min_crores = models.DecimalField(max_digits=8, decimal_places=2)
    investment_range_max_crores = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Time
    typical_construction_months = models.IntegerField()
    payback_period_years = models.DecimalField(max_digits=4, decimal_places=1)
    
    def __str__(self):
        return self.display_name


class LandRecommendation(models.Model):
    """AI-generated recommendations for specific land"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='recommendations')
    use_case = models.ForeignKey(DevelopmentUseCase, on_delete=models.CASCADE)
    
    # Scores & Prediction
    confidence_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    predicted_roi = models.DecimalField(max_digits=6, decimal_places=2)
    predicted_appreciation_5yr = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Reasoning (for explainability)
    reasoning = models.TextField()
    pros = models.JSONField(default=list)  # List of advantages
    cons = models.JSONField(default=list)  # List of disadvantages
    
    # Supporting Data
    nearby_infrastructure = models.JSONField(default=dict)  # Summary of nearby infra
    govt_projects_impact = models.JSONField(default=list)  # Relevant govt projects
    
    # Ranking
    rank = models.IntegerField(default=0)  # 1 = best recommendation
    
    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default='v1.0')
    
    class Meta:
        ordering = ['land', 'rank']
        unique_together = ['land', 'use_case']
    
    def __str__(self):
        return f"{self.land.name} → {self.use_case.display_name} (Score: {self.confidence_score})"


class ROICalculation(models.Model):
    """Detailed ROI calculation for a land + use case combination"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    use_case = models.ForeignKey(DevelopmentUseCase, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Inputs
    project_size_sqft = models.DecimalField(max_digits=12, decimal_places=2)
    construction_cost_per_sqft = models.DecimalField(max_digits=8, decimal_places=2)
    land_cost = models.DecimalField(max_digits=15, decimal_places=2)
    other_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Revenue Assumptions
    selling_price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rental_yield_monthly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Outputs
    total_investment = models.DecimalField(max_digits=15, decimal_places=2)
    expected_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)
    roi_percentage = models.DecimalField(max_digits=6, decimal_places=2)
    payback_years = models.DecimalField(max_digits=4, decimal_places=1)
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"ROI: {self.land.name} - {self.use_case.display_name}"


# ============================================
# USER INTERACTIONS
# ============================================

class UserQuery(models.Model):
    """Track semantic search queries for analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_lands')
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'land']
    
    def __str__(self):
        return f"{self.user.username} saved {self.land.name}"