# SSL Commerz Integration - Setup Instructions

## Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `sslcommerz-lib>=3.0.0` - SSL Commerz Python library
- `requests>=2.28.0` - For HTTP requests

### Step 2: Configure Environment Variables
Create a `.env` file in the project root:

```env
# SSL Commerz Configuration
SSL_COMMERZ_STORE_ID=testbox
SSL_COMMERZ_STORE_PASSWORD=5f48f6d6b7e661d
SITE_URL=http://localhost:8000

# For production:
# SSL_COMMERZ_STORE_ID=your_production_store_id
# SSL_COMMERZ_STORE_PASSWORD=your_production_password
# SITE_URL=https://your-domain.com
```

### Step 3: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

This creates/updates the Payment model with SSL Commerz fields:
- `sslc_val_id` - Validation ID from SSL Commerz
- `sslc_tran_id` - Transaction ID from SSL Commerz
- `bank_tran_id` - Bank Transaction ID
- `card_type` - Type of card used (Visa, Mastercard, etc.)
- `card_issuer` - Bank that issued the card
- `card_number` - Last 4 digits of card number

### Step 4: Update Django Settings
The settings are already configured in `ecommerce/settings.py`:

```python
SSL_COMMERZ_STORE_ID = os.getenv('SSL_COMMERZ_STORE_ID', 'testbox')
SSL_COMMERZ_STORE_PASSWORD = os.getenv('SSL_COMMERZ_STORE_PASSWORD', '5f48f6d6b7e661d')
SSL_COMMERZ_BASE_URL = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'
SSL_COMMERZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/gateway.php'
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')
```

### Step 5: Update Main URLs
The payment URLs are included in `ecommerce/urls.py`:

```python
path('payments/', include('payments.urls')),
```

### Step 6: Test the Integration

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Create a test user:**
   - Go to http://localhost:8000/auth/register/
   - Register a new account

3. **Add items to cart:**
   - Browse products and add some to your cart

4. **Go to checkout:**
   - Navigate to http://localhost:8000/checkout/
   - Fill in shipping information
   - Select "SSL Commerz" as payment method
   - Click "Complete Order"

5. **Complete test payment:**
   - Use test card: 4111111111111111
   - Any CVV (e.g., 123)
   - Any future expiry date
   - Complete the payment

6. **Verify payment:**
   - Check if order status changes to "paid"
   - Verify payment record is created in admin

## File Structure

New/Modified files:
```
├── payments/
│   ├── models.py                    # Updated Payment model
│   ├── views.py                     # SSL Commerz views
│   ├── urls.py                      # Payment URLs
│   └── migrations/
│       └── 0002_add_ssl_commerz_fields.py
├── templates/
│   ├── checkout/checkout.html       # Updated checkout template
│   └── payments/
│       └── payment_status.html      # Payment status page
├── cart/
│   └── views.py                     # Updated checkout view
├── ecommerce/
│   ├── settings.py                  # SSL Commerz configuration
│   └── urls.py                      # Payment URLs included
├── requirements.txt                 # Updated with sslcommerz-lib
├── .env.example                     # Environment variables template
└── SSL_COMMERZ_INTEGRATION.md        # Integration documentation
```

## Payment Flow

```
1. User adds items to cart
   ↓
2. User navigates to checkout (/checkout/)
   ↓
3. User fills shipping information
   ↓
4. User selects payment method (SSL Commerz)
   ↓
5. Order is created in database
   ↓
6. User is redirected to SSL Commerz payment gateway
   ↓
7. User completes payment at SSL Commerz
   ↓
8. SSL Commerz redirects to success/fail callback
   ↓
9. Payment record is created/updated with transaction details
   ↓
10. Order status is updated to 'processing' with payment_status 'paid'
   ↓
11. User is shown payment status page
```

## API Endpoints

### Payment Initiation
```
GET /payments/ssl-commerz/initiate/<order_id>/
```
Initiates a payment session with SSL Commerz

### Success Callback
```
POST /payments/ssl-commerz/success/
```
Called by SSL Commerz after successful payment

### Failure Callback
```
POST /payments/ssl-commerz/fail/
```
Called by SSL Commerz after failed payment

### Cancellation Callback
```
POST /payments/ssl-commerz/cancel/
```
Called by SSL Commerz if user cancels payment

### IPN Webhook
```
POST /payments/ssl-commerz/ipn/
```
Instant Payment Notification from SSL Commerz servers

### Payment Status
```
GET /payments/status/<order_id>/
```
Check payment status for an order

## Testing Credentials (Sandbox)

Store ID: `testbox`
Store Password: `5f48f6d6b7e661d`

Test Cards:
- Visa: 4111111111111111
- Mastercard: 5555555555554444

Any CVV and future expiry date will work.

## Production Setup

### 1. Get SSL Commerz Account
- Visit https://www.sslcommerz.com
- Create merchant account
- Get Store ID and Store Password

### 2. Update Configuration
In `.env`:
```env
SSL_COMMERZ_STORE_ID=your_store_id
SSL_COMMERZ_STORE_PASSWORD=your_store_password
SITE_URL=https://your-domain.com
```

### 3. Update Settings (if needed)
In `ecommerce/settings.py`, uncomment production URLs:
```python
SSL_COMMERZ_BASE_URL = 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'
SSL_COMMERZ_SESSION_API = 'https://securepay.sslcommerz.com/gwprocess/v4/gateway.php'
```

### 4. Security Checklist
- [ ] Use HTTPS only
- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up proper logging
- [ ] Enable CSRF protection
- [ ] Use environment variables for sensitive data
- [ ] Set up email notifications
- [ ] Configure database backups
- [ ] Monitor payment logs

## Troubleshooting

### Issue: "Store ID not recognized"
**Solution:**
- Verify SSL_COMMERZ_STORE_ID in settings
- Check .env file is being loaded
- Ensure credentials match your SSL Commerz account

### Issue: Payment success but order not updated
**Solution:**
- Check SITE_URL is correct and accessible
- Verify order number format matches expected
- Check application logs for errors
- Ensure database connection is working

### Issue: IPN requests not being processed
**Solution:**
- Ensure SITE_URL is publicly accessible
- Register IPN URL in SSL Commerz account settings
- Check firewall allows incoming POST requests
- Monitor server logs for IPN requests

### Issue: Test payment not working
**Solution:**
- Use correct test credentials (testbox)
- Use correct test card numbers
- Ensure development server is running
- Check browser console for JavaScript errors
- Verify CSRF token in form

## Additional Resources

- **SSL Commerz Documentation:** https://www.sslcommerz.com/doc/
- **Python Library:** https://github.com/sslcommerz/sslcommerz-lib
- **Django Docs:** https://docs.djangoproject.com/
- **Security Best Practices:** https://owasp.org/www-project-web-security-testing-guide/

## Support

For issues or questions:
1. Check SSL_COMMERZ_INTEGRATION.md for detailed documentation
2. Review SSL Commerz official documentation
3. Check Django logs for errors
4. Contact SSL Commerz support

## Next Steps

After setup:
1. Customize payment status page
2. Set up email notifications
3. Configure order processing workflow
4. Set up payment refund handling
5. Add advanced analytics
6. Implement subscription payments
7. Add payment failure recovery

---

**Setup completed! Your Django ecommerce project is now integrated with SSL Commerz.**
