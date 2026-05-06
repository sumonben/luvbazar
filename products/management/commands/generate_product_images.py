from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product
from PIL import Image, ImageDraw, ImageFont
import io
import os
import random


class Command(BaseCommand):
    help = 'Generate lightweight placeholder images for all products without images'

    # Category colors for visual distinction
    CATEGORY_COLORS = {
        'electronics': '#3498db',      # Blue
        'clothing': '#e74c3c',         # Red
        'home-garden': '#2ecc71',      # Green
        'sports-outdoors': '#f39c12',  # Orange
        'books': '#9b59b6',            # Purple
        'vegetables': '#27ae60',       # Dark Green
        'grocery': '#e67e22',          # Dark Orange
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generate images for all products, even if they have images',
        )

    def handle(self, *args, **options):
        if options['all']:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(image__isnull=True) | Product.objects.filter(image='')

        total = products.count()
        if total == 0:
            self.stdout.write(self.style.WARNING('No products need images'))
            return

        self.stdout.write(f'Generating images for {total} products...')

        for index, product in enumerate(products, 1):
            try:
                # Generate lightweight image
                image_data = self.generate_lightweight_image(product)
                
                # Save image
                filename = f"{product.slug}.webp"
                image_path = os.path.join('products', product.category.slug, filename)
                
                product.image.save(
                    image_path,
                    ContentFile(image_data),
                    save=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ [{index}/{total}] {product.name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to generate image for {product.name}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'✓ Generated {total} product images!'))

    def generate_lightweight_image(self, product):
        """Generate a lightweight WebP placeholder image"""
        # Create a small image (300x300) for lightweight size
        width, height = 300, 300
        
        # Get color based on category
        category_slug = product.category.slug if product.category else 'electronics'
        hex_color = self.CATEGORY_COLORS.get(category_slug, '#3498db')
        
        # Convert hex to RGB
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Create image with gradient effect
        img = Image.new('RGB', (width, height), rgb_color)
        draw = ImageDraw.Draw(img)
        
        # Add a subtle pattern
        for i in range(0, width, 20):
            for j in range(0, height, 20):
                opacity = (i + j) % 50
                if opacity > 25:
                    draw.rectangle(
                        [(i, j), (i+20, j+20)],
                        outline=self._adjust_brightness(rgb_color, -30),
                        width=1
                    )
        
        # Add product name text
        try:
            # Try to use default font, fallback to default if not available
            font_size = 20
            # Use default font
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Wrap text and center it
        text = product.name[:30]  # Limit text length
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw white text with slight shadow
        draw.text((x+1, y+1), text, fill=(0, 0, 0), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Add category label at bottom
        category_text = product.category.name if product.category else 'Product'
        bbox = draw.textbbox((0, 0), category_text, font=font)
        cat_width = bbox[2] - bbox[0]
        draw.text(
            ((width - cat_width) // 2, height - 40),
            category_text,
            fill=(255, 255, 255),
            font=font
        )
        
        # Save as WebP for lightweight size
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=75, method=6)
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def _adjust_brightness(rgb, amount):
        """Adjust brightness of RGB color"""
        return tuple(
            max(0, min(255, c + amount))
            for c in rgb
        )
