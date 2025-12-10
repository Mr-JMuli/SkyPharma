from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pharmacy.models import Category, Medicine
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@skypharma.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))
        
        categories_data = [
            {'name': 'Pain Relief', 'description': 'Medicines for pain management and relief'},
            {'name': 'Vitamins & Supplements', 'description': 'Essential vitamins and dietary supplements'},
            {'name': 'Cold & Flu', 'description': 'Medicines for cold, flu, and respiratory issues'},
            {'name': 'First Aid', 'description': 'First aid supplies and wound care products'},
            {'name': 'Digestive Health', 'description': 'Products for digestive wellness'},
            {'name': 'Skin Care', 'description': 'Dermatological products and skin treatments'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'Created category: {cat.name}')
        
        medicines_data = [
            {
                'name': 'Paracetamol 500mg',
                'description': 'Fast-acting pain relief and fever reducer. Suitable for headaches, muscle aches, and mild to moderate pain.',
                'category': 'Pain Relief',
                'price': Decimal('150.00'),
                'stock': 100,
                'dosage': '1-2 tablets every 4-6 hours',
                'manufacturer': 'GSK',
                'featured': True,
            },
            {
                'name': 'Ibuprofen 400mg',
                'description': 'Anti-inflammatory pain reliever. Effective for joint pain, dental pain, and menstrual cramps.',
                'category': 'Pain Relief',
                'price': Decimal('200.00'),
                'stock': 80,
                'dosage': '1 tablet every 6-8 hours with food',
                'manufacturer': 'Pfizer',
                'featured': True,
            },
            {
                'name': 'Vitamin C 1000mg',
                'description': 'High-strength vitamin C supplement for immune support and overall health.',
                'category': 'Vitamins & Supplements',
                'price': Decimal('450.00'),
                'stock': 60,
                'dosage': '1 tablet daily',
                'manufacturer': 'Nature Made',
                'featured': True,
            },
            {
                'name': 'Multivitamin Complex',
                'description': 'Complete daily multivitamin with essential vitamins and minerals for optimal health.',
                'category': 'Vitamins & Supplements',
                'price': Decimal('850.00'),
                'stock': 45,
                'dosage': '1 tablet daily with breakfast',
                'manufacturer': 'Centrum',
                'featured': True,
            },
            {
                'name': 'Cold & Flu Relief',
                'description': 'Multi-symptom relief for cold and flu. Relieves congestion, fever, and body aches.',
                'category': 'Cold & Flu',
                'price': Decimal('350.00'),
                'stock': 70,
                'dosage': '2 tablets every 6 hours',
                'manufacturer': 'Vicks',
                'featured': False,
            },
            {
                'name': 'Cough Syrup',
                'description': 'Effective cough suppressant for dry and productive coughs. Soothes throat irritation.',
                'category': 'Cold & Flu',
                'price': Decimal('280.00'),
                'stock': 55,
                'dosage': '10ml every 4-6 hours',
                'manufacturer': 'Benylin',
                'featured': False,
            },
            {
                'name': 'Antiseptic Cream',
                'description': 'Antibacterial cream for minor cuts, burns, and skin infections.',
                'category': 'First Aid',
                'price': Decimal('180.00'),
                'stock': 90,
                'dosage': 'Apply thin layer 2-3 times daily',
                'manufacturer': 'Dettol',
                'featured': True,
            },
            {
                'name': 'Bandage Pack',
                'description': 'Assorted sterile bandages for wound care and protection.',
                'category': 'First Aid',
                'price': Decimal('250.00'),
                'stock': 120,
                'dosage': 'As needed',
                'manufacturer': 'Johnson & Johnson',
                'featured': False,
            },
            {
                'name': 'Antacid Tablets',
                'description': 'Fast relief from heartburn, acid indigestion, and upset stomach.',
                'category': 'Digestive Health',
                'price': Decimal('220.00'),
                'stock': 65,
                'dosage': '1-2 tablets as needed',
                'manufacturer': 'Tums',
                'featured': False,
            },
            {
                'name': 'Probiotic Capsules',
                'description': 'Daily probiotic supplement for digestive health and immune support.',
                'category': 'Digestive Health',
                'price': Decimal('780.00'),
                'stock': 40,
                'dosage': '1 capsule daily',
                'manufacturer': 'Culturelle',
                'featured': True,
            },
            {
                'name': 'Hydrocortisone Cream',
                'description': 'Anti-itch cream for skin irritation, rashes, and eczema.',
                'category': 'Skin Care',
                'price': Decimal('320.00'),
                'stock': 50,
                'dosage': 'Apply thin layer 2 times daily',
                'manufacturer': 'Cortizone',
                'featured': False,
                'requires_prescription': True,
            },
            {
                'name': 'Sunscreen SPF 50',
                'description': 'High protection sunscreen for all skin types. Water resistant.',
                'category': 'Skin Care',
                'price': Decimal('550.00'),
                'stock': 35,
                'dosage': 'Apply 15 minutes before sun exposure',
                'manufacturer': 'Nivea',
                'featured': True,
            },
        ]
        
        for med_data in medicines_data:
            category = categories.get(med_data.pop('category'))
            if category:
                med, created = Medicine.objects.get_or_create(
                    name=med_data['name'],
                    defaults={**med_data, 'category': category}
                )
                if created:
                    self.stdout.write(f'Created medicine: {med.name}')
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
        self.stdout.write(self.style.SUCCESS('Admin credentials: username=admin, password=admin123'))
