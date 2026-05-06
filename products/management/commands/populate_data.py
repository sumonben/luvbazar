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
            {'name': 'Vegetables', 'slug': 'vegetables'},
            {'name': 'Grocery', 'slug': 'grocery'},
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
            # Vegetables
            {'name': 'Fresh Tomatoes', 'category': 'vegetables'},
            {'name': 'Organic Carrots', 'category': 'vegetables'},
            {'name': 'Crispy Lettuce', 'category': 'vegetables'},
            {'name': 'Green Bell Peppers', 'category': 'vegetables'},
            {'name': 'Fresh Cucumbers', 'category': 'vegetables'},
            {'name': 'Purple Onions', 'category': 'vegetables'},
            {'name': 'Broccoli Florets', 'category': 'vegetables'},
            {'name': 'Cauliflower', 'category': 'vegetables'},
            {'name': 'Spinach Bunch', 'category': 'vegetables'},
            {'name': 'Garlic Bulbs', 'category': 'vegetables'},
            {'name': 'Potatoes', 'category': 'vegetables'},
            {'name': 'Sweet Potatoes', 'category': 'vegetables'},
            {'name': 'Radishes', 'category': 'vegetables'},
            {'name': 'Green Beans', 'category': 'vegetables'},
            {'name': 'Cabbage', 'category': 'vegetables'},
            # Grocery
            {'name': 'Basmati Rice (5kg)', 'category': 'grocery'},
            {'name': 'Whole Wheat Flour (2kg)', 'category': 'grocery'},
            {'name': 'Olive Oil (500ml)', 'category': 'grocery'},
            {'name': 'Vegetable Oil (1L)', 'category': 'grocery'},
            {'name': 'Salt (1kg)', 'category': 'grocery'},
            {'name': 'Sugar (1kg)', 'category': 'grocery'},
            {'name': 'Milk (1L)', 'category': 'grocery'},
            {'name': 'Butter (250g)', 'category': 'grocery'},
            {'name': 'Cheese Block (500g)', 'category': 'grocery'},
            {'name': 'Eggs (12 pack)', 'category': 'grocery'},
            {'name': 'Chicken Breast (1kg)', 'category': 'grocery'},
            {'name': 'Ground Beef (1kg)', 'category': 'grocery'},
            {'name': 'Pasta (500g)', 'category': 'grocery'},
            {'name': 'Canned Tomatoes (400g)', 'category': 'grocery'},
            {'name': 'Black Beans (400g)', 'category': 'grocery'},
            {'name': 'Chickpeas (400g)', 'category': 'grocery'},
            {'name': 'Peanut Butter (500g)', 'category': 'grocery'},
            {'name': 'Honey (500ml)', 'category': 'grocery'},
            {'name': 'Tea Bags (50 pack)', 'category': 'grocery'},
            {'name': 'Coffee (500g)', 'category': 'grocery'},
            {'name': 'Bread Loaf', 'category': 'grocery'},
            {'name': 'Cereal Mix (400g)', 'category': 'grocery'},
            {'name': 'Yogurt (500ml)', 'category': 'grocery'},
            {'name': 'Apple Juice (1L)', 'category': 'grocery'},
            {'name': 'Orange Juice (1L)', 'category': 'grocery'},
            {'name': 'Almonds (250g)', 'category': 'grocery'},
            {'name': 'Cashews (250g)', 'category': 'grocery'},
            {'name': 'Raisins (200g)', 'category': 'grocery'},
            {'name': 'Dark Chocolate (100g)', 'category': 'grocery'},
        ]

        for prod_data in products_data:
            category = next(c for c in categories if c.slug == prod_data['category'])
            
            # Set price ranges based on category
            if prod_data['category'] == 'vegetables':
                price = round(random.uniform(2, 15), 2)
                stock = random.randint(20, 200)
            elif prod_data['category'] == 'grocery':
                price = round(random.uniform(1.5, 50), 2)
                stock = random.randint(15, 150)
            else:
                price = round(random.uniform(10, 500), 2)
                stock = random.randint(5, 100)
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': fake.text(max_nb_chars=500),
                    'category': category,
                    'price': price,
                    'stock': stock,
                    'slug': prod_data['name'].lower().replace(' ', '-').replace('(', '').replace(')', ''),
                    'status': 'active',
                    'rating': round(random.uniform(3, 5), 1),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
