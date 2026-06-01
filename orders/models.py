from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from region.models import Union,Upazilla,District,Division

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('product', 'Product Order'),
        ('room', 'Room Booking'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),  # For room bookings
        ('checked_in', 'Checked In'),  # For room bookings
        ('checked_out', 'Checked Out'),  # For room bookings
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_number = models.CharField(max_length=50, unique=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='product')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    
    # Customer information
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Shipping information (for products)
    
    shipping_address = models.TextField(blank=True, null=True)
    union = models.ForeignKey(Union, on_delete=models.SET_NULL, null=True, blank=True)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)

    
    # Room booking specific fields
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    number_of_guests = models.IntegerField(null=True, blank=True)
    special_requests = models.TextField(blank=True, null=True)
    
    # Order totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"
    
    def get_duration_nights(self):
        """Calculate number of nights for room bookings"""
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.product:
            return f"{self.product.name} - Order {self.order.order_number}"
        return f"Order Item {self.id}"
    
    def get_total_price(self):
        """Calculate total price for this item"""
        return self.price * self.quantity
    
    def get_item_name(self):
        """Get the name of the item (product)"""
        if self.product:
            return self.product.name
        return "Unknown Item"
