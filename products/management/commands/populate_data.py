from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Populate the database with sample product data'

    def handle(self, *args, **options):
        fake = Faker()
        
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Clothing', 'slug': 'clothing'},
            {'name': 'Home & Garden', 'slug': 'home-garden'},
            {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors'},
            {'name': 'Books', 'slug': 'books'},
        ]

        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': fake.text()}
            )
            categories.append(cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {cat.name}'))

        # Create products
        products_data = [
            {'name': 'Wireless Bluetooth Headphones', 'category': 'electronics'},
            {'name': 'USB-C Fast Charger', 'category': 'electronics'},
            {'name': 'Premium Cotton T-Shirt', 'category': 'clothing'},
            {'name': 'Running Shoes', 'category': 'clothing'},
            {'name': 'Stainless Steel Water Bottle', 'category': 'sports-outdoors'},
            {'name': 'Yoga Mat', 'category': 'sports-outdoors'},
            {'name': 'LED Desk Lamp', 'category': 'home-garden'},
            {'name': 'Plant Pot Set', 'category': 'home-garden'},
            {'name': 'Python Programming Book', 'category': 'books'},
            {'name': 'Web Development Guide', 'category': 'books'},
            {'name': 'Gaming Mouse', 'category': 'electronics'},
            {'name': 'Mechanical Keyboard', 'category': 'electronics'},
            {'name': 'Winter Jacket', 'category': 'clothing'},
            {'name': 'Gym Dumbbell Set', 'category': 'sports-outdoors'},
            {'name': 'Coffee Table', 'category': 'home-garden'},
        ]

        for prod_data in products_data:
            category = next(c for c in categories if c.slug == prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': fake.text(max_nb_chars=500),
                    'category': category,
                    'price': round(random.uniform(10, 500), 2),
                    'stock': random.randint(5, 100),
                    'slug': prod_data['name'].lower().replace(' ', '-'),
                    'status': 'active',
                    'rating': round(random.uniform(3, 5), 1),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
