from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def is_in_stock(self):
        return self.stock > 0

    def update_rating(self):
        """Calculate and update product rating based on customer reviews"""
        from django.db.models import Avg
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating else 0
        self.save(update_fields=['rating', 'updated_at'])
        return self.rating


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='customers/%Y/%m/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name or str(self.phone)


class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel/')
    title = models.CharField(max_length=150, blank=True, null=True)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    action_text = models.CharField(max_length=50, blank=True, null=True)
    action_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=(('active', 'Active'), ('inactive', 'Inactive')), default='active')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Slide {self.id}"


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default='Ecommerz')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    site_caption = models.CharField(max_length=200, blank=True, default='Online Shopping')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    footer_copyright = models.CharField(max_length=200, blank=True, default='All rights reserved.')

    def __str__(self):
        return self.site_name
