from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Land, 
    # LandImage, Infrastructure, GovernmentProject,  # COMMENTED OUT
    # DevelopmentUseCase, LandRecommendation, ROICalculation,  # COMMENTED OUT
    UserQuery, SavedLand,
    SoilData, CropRecommendation
)

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin for CustomUser model"""
    list_display = ['username', 'email', 'user_type', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'address', 'profile_picture', 'bio', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'email')
        }),
    )


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'land_type', 'size_in_acres', 'total_price', 'status', 'is_featured', 'created_at']
    list_filter = ['land_type', 'status', 'city', 'state', 'is_featured', 'has_water_supply', 'has_electricity', 'has_road_access']
    search_fields = ['name', 'city', 'state', 'address', 'description']
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'land_type', 'status', 'owner', 'slug', 'is_featured')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address', 'city', 'state', 'pincode')
        }),
        ('Size & Pricing', {
            'fields': ('size_in_acres', 'price_per_acre', 'total_price')
        }),
        ('Connectivity Scores', {
            'fields': ('highway_proximity_score', 'metro_proximity_score', 'airport_proximity_score')
        }),
        ('Infrastructure', {
            'fields': ('has_water_supply', 'has_electricity', 'has_road_access')
        }),
        ('Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# COMMENTED OUT - LandImage not currently used
# @admin.register(LandImage)
# class LandImageAdmin(admin.ModelAdmin):
#     list_display = ['land', 'caption', 'is_primary', 'uploaded_at']
#     list_filter = ['is_primary', 'uploaded_at']
#     search_fields = ['land__name', 'caption']
#     ordering = ['-uploaded_at']


# COMMENTED OUT - Infrastructure not currently used
# @admin.register(Infrastructure)
# class InfrastructureAdmin(admin.ModelAdmin):
#     list_display = ['name', 'infra_type', 'city', 'is_operational', 'established_year']
#     list_filter = ['infra_type', 'city', 'is_operational']
#     search_fields = ['name', 'city', 'address']
#     ordering = ['city', 'infra_type']


# COMMENTED OUT - GovernmentProject not currently used
# @admin.register(GovernmentProject)
# class GovernmentProjectAdmin(admin.ModelAdmin):
#     list_display = ['name', 'project_type', 'status', 'city', 'state', 'budget_crores', 'completion_date']
#     list_filter = ['project_type', 'status', 'city', 'state']
#     search_fields = ['name', 'city', 'state', 'description']
#     ordering = ['-start_date']
#     date_hierarchy = 'start_date'
#     
#     fieldsets = (
#         ('Project Information', {
#             'fields': ('name', 'project_type', 'status', 'description')
#         }),
#         ('Location', {
#             'fields': ('latitude', 'longitude', 'radius_km', 'city', 'state')
#         }),
#         ('Financial & Timeline', {
#             'fields': ('budget_crores', 'start_date', 'completion_date')
#         }),
#         ('Impact', {
#             'fields': ('expected_land_appreciation', 'source_url')
#         }),
#     )


# COMMENTED OUT - DevelopmentUseCase not currently used
# @admin.register(DevelopmentUseCase)
# class DevelopmentUseCaseAdmin(admin.ModelAdmin):
#     list_display = ['display_name', 'name', 'min_size_acres', 'typical_roi_min', 'typical_roi_max', 'payback_period_years']
#     list_filter = ['name']
#     search_fields = ['display_name', 'description']


# COMMENTED OUT - LandRecommendation not currently used
# @admin.register(LandRecommendation)
# class LandRecommendationAdmin(admin.ModelAdmin):
#     list_display = ['land', 'use_case', 'confidence_score', 'predicted_roi', 'rank', 'generated_at']
#     list_filter = ['use_case', 'rank', 'generated_at']
#     search_fields = ['land__name', 'use_case__display_name', 'reasoning']
#     ordering = ['land', 'rank']
#     readonly_fields = ['generated_at']


# COMMENTED OUT - ROICalculation not currently used
# @admin.register(ROICalculation)
# class ROICalculationAdmin(admin.ModelAdmin):
#     list_display = ['land', 'use_case', 'user', 'total_investment', 'net_profit', 'roi_percentage', 'calculated_at']
#     list_filter = ['use_case', 'calculated_at']
#     search_fields = ['land__name', 'use_case__display_name', 'user__username']
#     readonly_fields = ['calculated_at']
#     ordering = ['-calculated_at']


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_type', 'query_text_short', 'results_count', 'response_time_ms', 'created_at']
    list_filter = ['query_type', 'created_at']
    search_fields = ['query_text', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def query_text_short(self, obj):
        return obj.query_text[:50] + '...' if len(obj.query_text) > 50 else obj.query_text
    query_text_short.short_description = 'Query'


@admin.register(SavedLand)
class SavedLandAdmin(admin.ModelAdmin):
    list_display = ['user', 'land', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'land__name', 'notes']
    ordering = ['-saved_at']
    date_hierarchy = 'saved_at'


@admin.register(SoilData)
class SoilDataAdmin(admin.ModelAdmin):
    """Admin for SoilData model"""
    list_display = ['id', 'user', 'land', 'location', 'test_date', 'ph', 'nitrogen', 'phosphorous', 'potassium']
    list_filter = ['test_date', 'created_at']
    search_fields = ['user__username', 'land__name', 'location', 'notes']
    ordering = ['-created_at']
    date_hierarchy = 'test_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'land', 'location', 'notes')
        }),
        ('NPK Values', {
            'fields': ('nitrogen', 'phosphorous', 'potassium')
        }),
        ('Soil Properties', {
            'fields': ('ph',)
        }),
        ('Climate Data', {
            'fields': ('temperature', 'humidity', 'rainfall')
        }),
        ('Metadata', {
            'fields': ('test_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['test_date', 'created_at', 'updated_at']


@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    """Admin for CropRecommendation model"""
    list_display = ['id', 'user', 'recommended_crop', 'confidence_percentage', 'soil_suitability', 'created_at']
    list_filter = ['recommended_crop', 'soil_suitability', 'created_at']
    search_fields = ['user__username', 'recommended_crop']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'confidence_percentage']
    
    def confidence_percentage(self, obj):
        return f"{obj.get_confidence_percentage()}%"
    confidence_percentage.short_description = 'Confidence'


