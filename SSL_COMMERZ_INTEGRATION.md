# SSL Commerz Integration Guide

## Overview
This guide explains how to integrate SSL Commerz payment gateway with the Django ecommerce project.

## Features
- ✅ SSL Commerz payment gateway integration
- ✅ Support for credit/debit cards, mobile banking
- ✅ IPN (Instant Payment Notification) handling
- ✅ Payment validation and verification
- ✅ Multiple payment methods (SSL Commerz, Cash on Delivery, Bank Transfer)
- ✅ Order status tracking
- ✅ Transaction logging

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

The following packages are required:
- `sslcommerz-lib>=3.0.0` - SSL Commerz Python library
- `requests>=2.28.0` - HTTP library for API calls

### 2. Database Migration
Create migration for the new Payment model fields:
```bash
python manage.py makemigrations payments
python manage.py migrate payments
```

The migration will add SSL Commerz specific fields to the Payment model:
- `sslc_val_id` - SSL Commerz Validation ID
- `sslc_tran_id` - SSL Commerz Transaction ID
- `bank_tran_id` - Bank Transaction ID
- `card_type` - Card type (Visa, Mastercard, etc.)
- `card_issuer` - Card issuing bank
- `card_number` - Last 4 digits of card (for security)

## Configuration

### 1. Environment Variables
Create a `.env` file in the project root with the following:

```env
# SSL Commerz Sandbox (Testing)
SSL_COMMERZ_STORE_ID=testbox
SSL_COMMERZ_STORE_PASSWORD=5f48f6d6b7e661d
SITE_URL=http://localhost:8000

# For production, update with your credentials:
# SSL_COMMERZ_STORE_ID=your_production_store_id
# SSL_COMMERZ_STORE_PASSWORD=your_production_password
# SITE_URL=https://your-domain.com
```

### 2. Settings Configuration
The following settings are automatically configured in `ecommerce/settings.py`:

```python
# SSL Commerz Payment Gateway Configuration
SSL_COMMERZ_STORE_ID = os.getenv('SSL_COMMERZ_STORE_ID', 'testbox')
SSL_COMMERZ_STORE_PASSWORD = os.getenv('SSL_COMMERZ_STORE_PASSWORD', '5f48f6d6b7e661d')
SSL_COMMERZ_BASE_URL = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'  # Sandbox
SSL_COMMERZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/gateway.php'  # Sandbox

# Site configuration
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')
```

### 3. Production Setup
For production deployment:

1. Get your SSL Commerz credentials:
   - Visit https://www.sslcommerz.com
   - Register and get your Store ID and Store Password

2. Update environment variables:
   ```env
   SSL_COMMERZ_STORE_ID=your_production_store_id
   SSL_COMMERZ_STORE_PASSWORD=your_production_password
   SITE_URL=https://your-domain.com
   ```

3. Update `settings.py` SSL Commerz URLs (uncomment production URLs):
   ```python
   SSL_COMMERZ_BASE_URL = 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'
   SSL_COMMERZ_SESSION_API = 'https://securepay.sslcommerz.com/gwprocess/v4/gateway.php'
   ```

## URL Endpoints

The payment URLs are available at `/payments/`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/payments/ssl-commerz/initiate/<order_id>/` | GET | Initiate SSL Commerz payment |
| `/payments/ssl-commerz/success/` | POST | Success callback from SSL Commerz |
| `/payments/ssl-commerz/fail/` | POST | Payment failure callback |
| `/payments/ssl-commerz/cancel/` | POST | Payment cancellation callback |
| `/payments/ssl-commerz/ipn/` | POST | IPN webhook from SSL Commerz |
| `/payments/status/<order_id>/` | GET | Check payment status |

## Usage

### 1. Payment Flow

```
User → Checkout → Place Order → Select SSL Commerz → Redirect to SSL Commerz Gateway
                                                      ↓
                                        User completes payment
                                                      ↓
                                    SSL Commerz redirects to success URL
                                                      ↓
                                        Order marked as paid
```

### 2. Checkout Page
The checkout page (`/checkout/`) includes payment method selection:
- SSL Commerz (Recommended for online payments)
- Cash on Delivery
- Bank Transfer

### 3. Payment Processing

When a user selects SSL Commerz:

1. Order is created with status 'processing'
2. User is redirected to SSL Commerz payment gateway
3. After payment, SSL Commerz redirects to success/fail callback
4. Payment record is updated with transaction details
5. Order payment status is updated to 'paid'

## Models

### Payment Model
Located in `payments/models.py`

```python
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20)  # sslcommerz, stripe, etc.
    status = models.CharField(max_length=20)  # pending, completed, failed, refunded
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    
    # SSL Commerz specific fields
    sslc_val_id = models.CharField(max_length=100)  # Validation ID
    sslc_tran_id = models.CharField(max_length=100)  # Transaction ID
    bank_tran_id = models.CharField(max_length=100)  # Bank Transaction ID
    card_type = models.CharField(max_length=50)  # Visa, Mastercard, etc.
    card_issuer = models.CharField(max_length=100)  # Card issuing bank
    card_number = models.CharField(max_length=20)  # Last 4 digits
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
```

## Views

### Payment Views (`payments/views.py`)

**SSLCommerzHelper Class**
Helper class with static methods:
- `init_payment(order)` - Initialize payment session
- `validate_payment(val_id)` - Validate transaction
- `verify_ipn_hash(ipn_dict)` - Verify IPN hash

**View Functions**
- `initiate_ssl_payment(order_id)` - Start payment process
- `ssl_payment_success()` - Handle successful payment
- `ssl_payment_fail()` - Handle failed payment
- `ssl_payment_cancel()` - Handle cancelled payment
- `ssl_payment_ipn()` - Handle IPN notifications
- `payment_status(order_id)` - Check payment status

## Security

### Hash Verification
All IPN requests are verified using MD5 hash:
```
hash_string = val_id|store_password|amount|card_type|store_amount|status
```

### CSRF Exemption
Payment callbacks are CSRF-exempt to allow direct callbacks from SSL Commerz servers.

### Card Data Security
- Never store full card numbers (only last 4 digits)
- All sensitive data is encrypted in transit
- PCI DSS compliance is handled by SSL Commerz

## Testing

### 1. Sandbox Testing
SSL Commerz provides sandbox credentials:
- Store ID: `testbox`
- Store Password: `5f48f6d6b7e661d`

### 2. Test Cards
Use these test cards in sandbox:
- **Visa**: 4111111111111111 (Any CVV, Any future date)
- **Mastercard**: 5555555555554444 (Any CVV, Any future date)

### 3. Testing Payment Flow
1. Create a user account
2. Add products to cart
3. Go to checkout
4. Select SSL Commerz
5. Use test card credentials
6. Complete payment
7. Verify order status changes to 'paid'

## Troubleshooting

### Common Issues

**1. Payment fails with "Invalid Store ID"**
- Check SSL_COMMERZ_STORE_ID in settings
- Ensure environment variables are loaded
- Verify credentials match your SSL Commerz account

**2. IPN requests not processed**
- Check SITE_URL is accessible from internet
- Verify IPN URL is registered in SSL Commerz account
- Check server logs for connection errors

**3. Validation fails**
- Ensure SSL_COMMERZ_STORE_PASSWORD is correct
- Verify payment amount matches order total
- Check transaction ID format

**4. Payment successful but order not updated**
- Check database connection
- Verify Order exists with correct order_number
- Check application logs for errors

## Logging

Enable debug logging in Django settings to troubleshoot:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## Support and Documentation

- SSL Commerz Documentation: https://www.sslcommerz.com/doc/
- SSL Commerz Python Library: https://github.com/sslcommerz/sslcommerz-lib
- Django Documentation: https://docs.djangoproject.com/

## Future Enhancements

- [ ] Refund processing
- [ ] Recurring payments/Subscriptions
- [ ] Payment installments
- [ ] Mobile app integration
- [ ] Advanced analytics and reporting
- [ ] Webhook retry mechanism
- [ ] Payment method statistics

## Changelog

### Version 1.0
- Initial SSL Commerz integration
- Payment processing and validation
- IPN handling
- Order status tracking
- Multiple payment methods support
