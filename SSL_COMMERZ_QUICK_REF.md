# SSL Commerz Integration - Quick Reference

## ⚡ 30-Second Setup

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Create .env
echo "SSL_COMMERZ_STORE_ID=testbox" > .env
echo "SSL_COMMERZ_STORE_PASSWORD=5f48f6d6b7e661d" >> .env
echo "SITE_URL=http://localhost:8000" >> .env

# 3. Migrate database
python manage.py migrate

# 4. Run server
python manage.py runserver

# 5. Visit checkout
# http://localhost:8000/checkout/
```

## 🎯 Core URLs

| Purpose | URL |
|---------|-----|
| Checkout | `/checkout/` |
| Initiate Payment | `/payments/ssl-commerz/initiate/<order_id>/` |
| Check Status | `/payments/status/<order_id>/` |
| Admin | `/admin/payments/payment/` |

## 🧪 Test Credentials

| Field | Value |
|-------|-------|
| Store ID | testbox |
| Password | 5f48f6d6b7e661d |
| Visa | 4111111111111111 |
| Mastercard | 5555555555554444 |
| CVV | Any (e.g., 123) |
| Date | Any future date |

## 📝 Environment Variables

```env
SSL_COMMERZ_STORE_ID=testbox
SSL_COMMERZ_STORE_PASSWORD=5f48f6d6b7e661d
SITE_URL=http://localhost:8000
```

## 🔄 Payment Flow

1. User → Checkout
2. Select SSL Commerz
3. Create Order
4. Redirect to Gateway
5. Complete Payment
6. Success Callback
7. Update Order Status
8. Show Confirmation

## 🛠️ Key Files

| File | Purpose |
|------|---------|
| `payments/models.py` | Payment model |
| `payments/views.py` | Payment processing |
| `payments/urls.py` | Payment endpoints |
| `templates/checkout/checkout.html` | Checkout form |
| `templates/payments/payment_status.html` | Status page |
| `ecommerce/settings.py` | Configuration |

## 🔐 Security

- ✅ Hash verification
- ✅ CSRF protection
- ✅ Card data security
- ✅ SSL/TLS encryption
- ✅ Admin protection

## 📋 Payment Fields

| Field | Type | Purpose |
|-------|------|---------|
| `sslc_val_id` | String | Validation ID |
| `sslc_tran_id` | String | Transaction ID |
| `bank_tran_id` | String | Bank Transaction ID |
| `card_type` | String | Card Type |
| `card_issuer` | String | Card Issuer |
| `card_number` | String | Last 4 digits |

## 🎨 Payment Methods

- SSL Commerz
- Cash on Delivery  
- Bank Transfer

## 📊 Views Functions

| Function | Purpose |
|----------|---------|
| `initiate_ssl_payment()` | Start payment |
| `ssl_payment_success()` | Handle success |
| `ssl_payment_fail()` | Handle failure |
| `ssl_payment_cancel()` | Handle cancel |
| `ssl_payment_ipn()` | Handle webhook |
| `payment_status()` | Show status |

## 🚀 Production Setup

1. Get SSL Commerz merchant account
2. Update Store ID & Password
3. Change SITE_URL to production
4. Update SSL_COMMERZ_BASE_URL URLs
5. Set DEBUG=False
6. Enable HTTPS
7. Configure ALLOWED_HOSTS
8. Set up logging

## ✅ Testing Checklist

- [ ] Create user
- [ ] Add products to cart
- [ ] Go to checkout
- [ ] Select SSL Commerz
- [ ] Complete order
- [ ] Use test card
- [ ] Verify payment
- [ ] Check admin

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Store ID not found | Check .env file |
| Payment fails | Use correct test card |
| Order not updated | Check SITE_URL |
| IPN not working | Verify SITE_URL is public |

## 📚 Documentation Files

| File | Contains |
|------|----------|
| `SSL_COMMERZ_README.md` | Overview |
| `SSL_COMMERZ_SETUP.md` | Setup guide |
| `SSL_COMMERZ_INTEGRATION.md` | Details |
| `SSL_COMMERZ_COMPLETE.md` | Summary |

## 🎯 Important Notes

1. Use **testbox** credentials for development
2. Update to **production** credentials before going live
3. Ensure **HTTPS** in production
4. Set **SITE_URL** correctly
5. Keep **credentials** in .env
6. Monitor **payment logs**
7. Test **thoroughly** before launch

## 💡 Pro Tips

- Use sandbox for testing
- Monitor IPN requests in logs
- Keep detailed transaction records
- Set up email notifications
- Regular database backups
- Monitor payment success rate

## 🔗 Useful Links

- **SSL Commerz:** https://www.sslcommerz.com
- **Docs:** https://www.sslcommerz.com/doc/
- **Django:** https://docs.djangoproject.com/

---

**Ready to process payments? Start with `pip install -r requirements.txt`**
