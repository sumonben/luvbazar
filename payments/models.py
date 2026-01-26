from django.db import models
from orders.models import Order


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('sslcommerz', 'SSL Commerz'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    
    # SSL Commerz specific fields
    sslc_val_id = models.CharField(max_length=100, null=True, blank=True, help_text="SSL Commerz Validation ID")
    sslc_tran_id = models.CharField(max_length=100, null=True, blank=True, help_text="SSL Commerz Transaction ID")
    bank_tran_id = models.CharField(max_length=100, null=True, blank=True, help_text="Bank Transaction ID")
    card_type = models.CharField(max_length=50, null=True, blank=True)
    card_issuer = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)  # Last 4 digits
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order {self.order.order_number}"
