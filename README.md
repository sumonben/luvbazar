# Ecommerz - Django E-Commerce Project

A modern, scalable e-commerce platform built with Django and Django REST Framework.

## Features

- **Product Management**: Browse, search, and filter products by categories
- **Shopping Cart**: Add/remove items, manage quantities
- **Order Management**: Complete order lifecycle tracking
- **Payment Integration**: Support for Stripe, PayPal, and more
- **User Authentication**: Secure user registration and authentication
- **Reviews & Ratings**: Product reviews and ratings system
- **REST API**: Complete RESTful API for frontend integration
- **Admin Dashboard**: Comprehensive Django admin interface

## Project Structure

```
ecommerz/
├── products/           # Product catalog app
├── orders/            # Order management app
├── cart/              # Shopping cart app
├── payments/          # Payment processing app
├── users/             # User management app
├── ecommerce/         # Main project settings
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── README.md
```

## Apps

### Products
- Models: Category, Product, Review
- Features: Product listing, search, filtering, reviews

### Orders
- Models: Order, OrderItem
- Features: Order creation, status tracking, order history

### Cart
- Models: Cart, CartItem
- Features: Add to cart, remove items, cart totals

### Payments
- Models: Payment
- Features: Payment processing, transaction tracking

### Users
- Custom user authentication and profile management

## Installation

### Prerequisites
- Python 3.10+
- pip
- Virtual environment

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerz
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## API Endpoints

### Products
- `GET /api/v1/products/` - List all products
- `GET /api/v1/products/{slug}/` - Get product details
- `GET /api/v1/products/search/?q=query` - Search products
- `GET /api/v1/products/featured/` - Get featured products
- `POST /api/v1/products/{slug}/add_review/` - Add product review

### Categories
- `GET /api/v1/products/categories/` - List all categories

## Admin Dashboard

Access the admin dashboard at `http://localhost:8000/admin/`

- Create and manage products
- View and process orders
- Manage customer accounts
- Track payments
- Monitor reviews and ratings

## Configuration

### Database
By default, the project uses SQLite3. For production, configure PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Stripe Integration
1. Get your Stripe API keys from https://dashboard.stripe.com/
2. Add them to your `.env` file:
   ```
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   ```

## Development

### Run Tests
```bash
python manage.py test
```

### Create Database Fixtures
```bash
python manage.py dumpdata > fixtures.json
python manage.py loaddata fixtures.json
```

### Generate Sample Data
Create a management command in `<app>/management/commands/populate_data.py`

## Deployment

### Production Checklist
- Set `DEBUG=False`
- Update `ALLOWED_HOSTS`
- Configure a production database
- Set up static/media file serving
- Configure email backend
- Use environment variables for secrets
- Set up HTTPS/SSL
- Configure CORS properly

### Using Gunicorn
```bash
pip install gunicorn
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

## Dependencies

- **Django**: Web framework
- **Django REST Framework**: API development
- **django-cors-headers**: CORS handling
- **Pillow**: Image processing
- **Stripe**: Payment processing
- **Celery**: Asynchronous task queue
- **Redis**: Cache and task broker

## Security

- CSRF protection enabled
- SQL injection prevention (ORM usage)
- XSS protection
- Secure password hashing
- Token-based API authentication

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.

## Roadmap

- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Inventory management
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Wishlist feature
- [ ] Product variants
- [ ] Bulk operations

---

**Built with ❤️ using Django and React**
