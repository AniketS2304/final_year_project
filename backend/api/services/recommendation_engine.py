# backend/api/services/recommendation_engine.py

import numpy as np
from typing import List, Dict, Tuple
from django.db.models import Q
from geopy.distance import geodesic
from api.models import (
    Land, Infrastructure, GovernmentProject, 
    DevelopmentUseCase, LandRecommendation
)

class InvestorRecommendationEngine:
    """
    AI Engine to generate investment recommendations for land
    Combines rule-based logic + scoring algorithms
    """
    
    def __init__(self, land: Land):
        self.land = land
        self.location = (float(land.latitude), float(land.longitude))
        
    def generate_recommendations(self) -> List[Dict]:
        """
        Main method to generate all recommendations for a land
        Returns list of recommendations sorted by confidence score
        """
        recommendations = []
        
        # Get all possible use cases
        use_cases = DevelopmentUseCase.objects.all()
        
        for use_case in use_cases:
            score, reasoning = self._calculate_suitability_score(use_case)
            
            if score >= 30:  # Only consider if score > 30%
                rec = {
                    'use_case': use_case,
                    'confidence_score': round(score, 2),
                    'predicted_roi': self._estimate_roi(use_case, score),
                    'predicted_appreciation': self._estimate_appreciation(use_case, score),
                    'reasoning': reasoning,
                    'pros': self._generate_pros(use_case),
                    'cons': self._generate_cons(use_case),
                    'nearby_infrastructure': self._get_nearby_infra_summary(),
                    'govt_projects_impact': self._get_govt_projects_impact()
                }
                recommendations.append(rec)
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        # Assign ranks
        for idx, rec in enumerate(recommendations, 1):
            rec['rank'] = idx
        
        return recommendations[:5]  # Return top 5
    
    def _calculate_suitability_score(self, use_case: DevelopmentUseCase) -> Tuple[float, str]:
        """
        Calculate suitability score (0-100) for a use case
        Returns: (score, reasoning_text)
        """
        scores = {}
        reasoning_parts = []
        
        # 1. Size Check (20 points)
        if self.land.size_in_acres >= use_case.min_size_acres:
            size_score = min(20, (self.land.size_in_acres / use_case.min_size_acres) * 10)
            scores['size'] = size_score
            reasoning_parts.append(f"Land size ({self.land.size_in_acres} acres) is suitable")
        else:
            scores['size'] = 0
            reasoning_parts.append(f"Land size too small (needs {use_case.min_size_acres} acres)")
        
        # 2. Connectivity Score (30 points)
        connectivity_score = self._evaluate_connectivity(use_case)
        scores['connectivity'] = connectivity_score
        if connectivity_score > 20:
            reasoning_parts.append("Excellent connectivity")
        
        # 3. Infrastructure Proximity (25 points)
        infra_score = self._evaluate_infrastructure(use_case)
        scores['infrastructure'] = infra_score
        if infra_score > 15:
            reasoning_parts.append("Strong infrastructure nearby")
        
        # 4. Government Projects Impact (15 points)
        govt_score = self._evaluate_govt_projects(use_case)
        scores['government'] = govt_score
        if govt_score > 10:
            reasoning_parts.append("Upcoming government projects will boost value")
        
        # 5. Market Conditions (10 points)
        market_score = self._evaluate_market_conditions(use_case)
        scores['market'] = market_score
        
        # Total Score
        total_score = sum(scores.values())
        reasoning = " | ".join(reasoning_parts)
        
        return total_score, reasoning
    
    def _evaluate_connectivity(self, use_case: DevelopmentUseCase) -> float:
        """Evaluate connectivity based on use case requirements"""
        score = 0
        
        # Different use cases prioritize different connectivity
        if use_case.name in ['logistics', 'industrial']:
            # Highway proximity is critical
            score += self.land.highway_proximity_score * 0.3
        elif use_case.name in ['residential', 'commercial', 'it_park']:
            # Metro + Airport important
            score += self.land.metro_proximity_score * 0.15
            score += self.land.airport_proximity_score * 0.1
            score += self.land.highway_proximity_score * 0.05
        elif use_case.name in ['hospitality', 'mixed']:
            # Balanced
            score += (self.land.metro_proximity_score + 
                     self.land.airport_proximity_score + 
                     self.land.highway_proximity_score) * 0.1
        
        return min(30, score)
    
    def _evaluate_infrastructure(self, use_case: DevelopmentUseCase) -> float:
        """Calculate score based on nearby infrastructure"""
        score = 0
        
        # Get infrastructure within 5km radius
        nearby_infra = self._get_nearby_infrastructure(radius_km=5)
        
        # Scoring rules based on use case
        scoring_rules = {
            'residential': {
                'school': 3, 'college': 2, 'hospital': 4, 
                'mall': 3, 'metro': 5
            },
            'commercial': {
                'metro': 5, 'mall': 4, 'it_park': 3, 
                'highway': 4
            },
            'industrial': {
                'highway': 5, 'railway': 4, 'sez': 3, 
                'industrial': 3
            },
            'it_park': {
                'metro': 5, 'airport': 4, 'residential': 3, 
                'college': 3
            },
            'education': {
                'residential': 4, 'metro': 3, 'college': 2, 
                'hospital': 2
            },
            'hospitality': {
                'airport': 5, 'metro': 4, 'mall': 3, 
                'highway': 3
            },
            'logistics': {
                'highway': 5, 'railway': 5, 'airport': 4, 
                'industrial': 3
            },
        }
        
        use_case_rules = scoring_rules.get(use_case.name, {})
        
        for infra_type, count in nearby_infra.items():
            points = use_case_rules.get(infra_type, 1)
            score += min(count, 3) * points  # Cap at 3 of each type
        
        return min(25, score)
    
    def _evaluate_govt_projects(self, use_case: DevelopmentUseCase) -> float:
        """Evaluate impact of nearby government projects"""
        score = 0
        
        # Get projects within 10km
        nearby_projects = GovernmentProject.objects.filter(
            city=self.land.city,
            status__in=['planned', 'under_construction', 'announced']
        )
        
        for project in nearby_projects:
            distance = self._calculate_distance(
                (float(project.latitude), float(project.longitude))
            )
            
            if distance <= project.radius_km:
                # Project is relevant
                if use_case.name == 'residential' and project.project_type in ['metro', 'smart_city']:
                    score += 5
                elif use_case.name == 'industrial' and project.project_type in ['sez', 'industrial_park']:
                    score += 5
                elif use_case.name == 'logistics' and project.project_type in ['highway', 'port']:
                    score += 5
                else:
                    score += 2
        
        return min(15, score)
    
    def _evaluate_market_conditions(self, use_case: DevelopmentUseCase) -> float:
        """
        Placeholder for market conditions evaluation
        In production: integrate with real estate market APIs
        """
        # Simplified: return random score based on typical market
        city_growth_multiplier = {
            'Mumbai': 1.2, 'Delhi': 1.2, 'Bangalore': 1.3,
            'Pune': 1.1, 'Hyderabad': 1.15, 'Chennai': 1.1
        }
        
        multiplier = city_growth_multiplier.get(self.land.city, 1.0)
        return min(10, 8 * multiplier)
    
    def _estimate_roi(self, use_case: DevelopmentUseCase, confidence_score: float) -> float:
        """Estimate ROI based on use case and confidence"""
        base_roi = (use_case.typical_roi_min + use_case.typical_roi_max) / 2
        confidence_factor = confidence_score / 100
        return round(base_roi * confidence_factor * 1.2, 2)
    
    def _estimate_appreciation(self, use_case: DevelopmentUseCase, confidence_score: float) -> float:
        """Estimate 5-year appreciation"""
        # Simplified model
        base_appreciation = 30  # 30% over 5 years baseline
        confidence_bonus = (confidence_score / 100) * 20
        return round(base_appreciation + confidence_bonus, 2)
    
    def _generate_pros(self, use_case: DevelopmentUseCase) -> List[str]:
        """Generate list of advantages"""
        pros = []
        
        if self.land.highway_proximity_score > 70:
            pros.append("Excellent highway connectivity")
        if self.land.metro_proximity_score > 70:
            pros.append("Near metro station")
        if self.land.has_water_supply:
            pros.append("Water supply available")
        if self.land.has_electricity:
            pros.append("Electricity connection available")
        
        # Use case specific
        if use_case.name == 'residential':
            nearby_schools = Infrastructure.objects.filter(
                city=self.land.city, 
                infra_type='school'
            ).count()
            if nearby_schools > 5:
                pros.append("Multiple schools in vicinity")
        
        return pros
    
    def _generate_cons(self, use_case: DevelopmentUseCase) -> List[str]:
        """Generate list of disadvantages"""
        cons = []
        
        if not self.land.has_water_supply:
            cons.append("Water supply not available")
        if self.land.size_in_acres < use_case.min_size_acres * 1.5:
            cons.append("Limited space for expansion")
        if self.land.highway_proximity_score < 30:
            cons.append("Far from major highways")
        
        return cons
    
    def _get_nearby_infrastructure(self, radius_km: float = 5) -> Dict[str, int]:
        """Get count of infrastructure types within radius"""
        nearby = Infrastructure.objects.filter(city=self.land.city)
        
        infra_counts = {}
        for infra in nearby:
            distance = self._calculate_distance(
                (float(infra.latitude), float(infra.longitude))
            )
            if distance <= radius_km:
                infra_type = infra.infra_type
                infra_counts[infra_type] = infra_counts.get(infra_type, 0) + 1
        
        return infra_counts
    
    def _get_nearby_infra_summary(self) -> Dict:
        """Get detailed summary of nearby infrastructure"""
        infra_counts = self._get_nearby_infrastructure(radius_km=5)
        return {
            'within_5km': infra_counts,
            'total_count': sum(infra_counts.values())
        }
    
    def _get_govt_projects_impact(self) -> List[Dict]:
        """Get list of relevant government projects"""
        projects = GovernmentProject.objects.filter(
            city=self.land.city,
            status__in=['planned', 'under_construction', 'announced']
        )[:5]
        
        return [
            {
                'name': p.name,
                'type': p.get_project_type_display(),
                'status': p.get_status_display(),
                'expected_appreciation': float(p.expected_land_appreciation or 0)
            }
            for p in projects
        ]
    
    def _calculate_distance(self, other_location: Tuple[float, float]) -> float:
        """Calculate distance in km between two points"""
        return geodesic(self.location, other_location).km
    
    def save_recommendations(self) -> None:
        """Save generated recommendations to database"""
        recommendations = self.generate_recommendations()
        
        # Delete existing recommendations for this land
        LandRecommendation.objects.filter(land=self.land).delete()
        
        # Create new recommendations
        for rec in recommendations:
            LandRecommendation.objects.create(
                land=self.land,
                use_case=rec['use_case'],
                confidence_score=rec['confidence_score'],
                predicted_roi=rec['predicted_roi'],
                predicted_appreciation_5yr=rec['predicted_appreciation'],
                reasoning=rec['reasoning'],
                pros=rec['pros'],
                cons=rec['cons'],
                nearby_infrastructure=rec['nearby_infrastructure'],
                govt_projects_impact=rec['govt_projects_impact'],
                rank=rec['rank']
            )


# ============================================
# HELPER FUNCTION
# ============================================

def generate_recommendations_for_land(land_id: int) -> List[Dict]:
    """
    Wrapper function to generate recommendations
    Usage: recommendations = generate_recommendations_for_land(land_id=123)
    """
    land = Land.objects.get(id=land_id)
    engine = InvestorRecommendationEngine(land)
    return engine.generate_recommendations()