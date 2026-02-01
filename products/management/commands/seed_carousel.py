from django.core.management.base import BaseCommand
from products.models import Carousel
from django.core.files.base import ContentFile
import urllib.request

class Command(BaseCommand):
    help = 'Seeds the database with initial carousel slides'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding carousel slides...')
        
        # Clear existing slides
        Carousel.objects.all().delete()
        
        slides_data = [
            {
                'title': 'Welcome to Ecommerz',
                'sub_title': 'Discover Amazing Products at Unbeatable Prices',
                'action_text': 'Shop Now',
                'action_url': '/products/',
                'order': 1,
                'image_url': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'title': 'New Arrivals',
                'sub_title': 'Check out the latest trends in our collection',
                'action_text': 'View Newest',
                'action_url': '/products/?sort=-created_at',
                'order': 2,
                'image_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'title': 'Flash Sale',
                'sub_title': 'Up to 50% off on selected items',
                'action_text': 'View Deals',
                'action_url': '/products/?sort=price',
                'order': 3,
                'image_url': 'https://images.unsplash.com/photo-1607082349566-187342175e2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            }
        ]

        for data in slides_data:
            image_url = data.pop('image_url')
            slide = Carousel(**data)
            
            try:
                # Download image
                img_content = urllib.request.urlopen(image_url).read()
                file_name = f"slide_{data['order']}.jpg"
                slide.image.save(file_name, ContentFile(img_content), save=False)
                self.stdout.write(f"Downloaded image for {slide.title}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not download image for slide {data['title']}: {e}"))
            
            slide.save()
            self.stdout.write(self.style.SUCCESS(f"Created slide: {slide.title}"))
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded carousel slides'))