# backend/api/management/commands/seed_lands.py
# Create directory structure: api/management/commands/

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Land
from decimal import Decimal
from django.utils.text import slugify
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with sample land data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create test user if doesn't exist
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@agriwise.com'}
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Clear existing data
        Land.objects.all().delete()
        # Infrastructure.objects.all().delete()  # COMMENTED OUT
        # GovernmentProject.objects.all().delete()  # COMMENTED OUT
        
        # Sample data for different cities
        cities_data = [
            {
                'city': 'Pune', 'state': 'Maharashtra',
                'lat_base': 18.5204, 'lon_base': 73.8567
            },
            {
                'city': 'Mumbai', 'state': 'Maharashtra',
                'lat_base': 19.0760, 'lon_base': 72.8777
            },
            {
                'city': 'Nashik', 'state': 'Maharashtra',
                'lat_base': 19.9975, 'lon_base': 73.7898
            },
            {
                'city': 'Aurangabad', 'state': 'Maharashtra',
                'lat_base': 19.8762, 'lon_base': 75.3433
            },
            {
                'city': 'Nagpur', 'state': 'Maharashtra',
                'lat_base': 21.1458, 'lon_base': 79.0882
            },
        ]
        
        land_types = ['agricultural', 'residential', 'commercial', 'industrial', 'mixed']
        land_names = [
            'Green Valley Farm', 'Sunrise Orchards', 'Golden Fields Estate',
            'River View Plots', 'Hilltop Paradise', 'Meadow Gardens',
            'Royal Farms', 'Paradise Valley', 'Emerald Lands',
            'Crystal Waters Estate', 'Sunset Hills', 'Peaceful Acres',
            'Silver Oak Farm', 'Diamond Plains', 'Nature Bounty',
            'Heritage Lands', 'Prosperity Fields', 'Rainbow Meadows',
            'Dream Valley', 'Fortune Farms', 'Blissful Acres',
            'Harmony Gardens', 'Victory Fields', 'Serenity Estate'
        ]
        
        # Create 30 sample lands
        lands_created = 0
        for i in range(30):
            city_data = random.choice(cities_data)
            land_type = random.choice(land_types)
            
            # Vary location slightly
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)
            
            # Generate realistic values
            size_acres = random.choice([2, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100])
            price_per_acre = random.choice([200000, 300000, 500000, 800000, 1000000, 1500000, 2000000])
            
            # Connectivity scores (some lands have better connectivity)
            if land_type in ['commercial', 'residential']:
                highway_score = random.randint(60, 95)
                metro_score = random.randint(50, 90)
                airport_score = random.randint(40, 85)
            elif land_type == 'agricultural':
                highway_score = random.randint(30, 70)
                metro_score = random.randint(20, 60)
                airport_score = random.randint(10, 50)
            else:
                highway_score = random.randint(50, 85)
                metro_score = random.randint(40, 75)
                airport_score = random.randint(30, 70)
            
            # Infrastructure availability
            has_water = random.choice([True, True, True, False])  # 75% have water
            has_electricity = random.choice([True, True, True, False])
            has_road = random.choice([True, True, True, True, False])  # 80% have road
            
            # Generate unique slug
            land_name = f"{random.choice(land_names)} {i+1}"
            base_slug = slugify(land_name)
            slug = base_slug
            counter = 1
            while Land.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            land = Land.objects.create(
                name=land_name,
                description=f"Beautiful {land_type} land with great potential. "
                           f"Located in {city_data['city']}, this {size_acres} acre "
                           f"property offers excellent opportunities for development.",
                land_type=land_type,
                status='available',
                latitude=Decimal(str(city_data['lat_base'] + lat_offset)),
                longitude=Decimal(str(city_data['lon_base'] + lon_offset)),
                address=f"Survey No. {random.randint(100, 999)}, {city_data['city']}",
                city=city_data['city'],
                state=city_data['state'],
                pincode=f"{random.randint(400000, 499999)}",
                size_in_acres=Decimal(str(size_acres)),
                price_per_acre=Decimal(str(price_per_acre)),
                total_price=Decimal(str(size_acres * price_per_acre)),
                highway_proximity_score=highway_score,
                metro_proximity_score=metro_score,
                airport_proximity_score=airport_score,
                has_water_supply=has_water,
                has_electricity=has_electricity,
                has_road_access=has_road,
                owner=user,
                slug=slug,
                is_featured=random.choice([True, False, False])  # 33% featured
            )
            lands_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {lands_created} lands'))
        
        # COMMENTED OUT - Infrastructure and Government Projects not currently needed
        # # Create infrastructure
        # infra_types = [
        #     ('hospital', 'City Hospital'),
        #     ('school', 'Central School'),
        # ...]
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))