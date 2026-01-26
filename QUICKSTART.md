# Django E-Commerce Project - Getting Started Guide

## Quick Start

### 1. Verify Installation
The project has been created with a virtual environment at `.venv/` with all dependencies installed.

### 2. Create Superuser (Admin Account)
```bash
cd d:\Django Project\ecommerz
.venv\Scripts\activate
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 3. Populate Sample Data (Optional)
```bash
python manage.py populate_data
```

This will create sample categories and products in the database.

### 4. Run the Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

### 5. Access the Admin Dashboard
1. Go to `http://localhost:8000/admin/`
2. Login with the superuser credentials you created
3. You can now manage:
   - Products & Categories
   - Orders
   - Customers
   - Payments

## Project Structure

### Apps

#### Products (`products/`)
- **Models**: Category, Product, Review
- **API Endpoints**:
  - `GET /api/v1/products/` - List all products
  - `GET /api/v1/products/{slug}/` - Product details
  - `GET /api/v1/products/search/?q=query` - Search
  - `GET /api/v1/products/featured/` - Featured products
  - `POST /api/v1/products/{slug}/add_review/` - Add review

#### Orders (`orders/`)
- **Models**: Order, OrderItem
- Status tracking and order history

#### Cart (`cart/`)
- **Models**: Cart, CartItem
- Shopping cart functionality

#### Payments (`payments/`)
- **Models**: Payment
- Payment processing and tracking

#### Users (`users/`)
- User authentication and profiles

## Important Files

- `ecommerce/settings.py` - Project configuration
- `ecommerce/urls.py` - URL routing
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

## Database

The project uses **SQLite3** by default (file: `db.sqlite3`).

To use **PostgreSQL** for production:
1. Install PostgreSQL
2. Create a database
3. Update `settings.py` DATABASES configuration
4. Run migrations

## API Documentation

### Base URL
`http://localhost:8000/api/v1/`

### Products Endpoints
```
GET    /products/                      # List all products (paginated)
GET    /products/{slug}/               # Get product details
POST   /products/                      # Create product (admin only)
PUT    /products/{slug}/               # Update product (admin only)
DELETE /products/{slug}/               # Delete product (admin only)
GET    /products/search/?q=query       # Search products
GET    /products/featured/             # Get featured products
POST   /products/{slug}/add_review/    # Add product review
```

### Categories Endpoints
```
GET    /products/categories/           # List all categories
GET    /products/categories/{slug}/    # Get category details
```

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_data

# Run tests
python manage.py test

# Django shell (interactive Python with Django context)
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run development server on specific port
python manage.py runserver 0.0.0.0:8000

# Check for issues
python manage.py check
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
DEBUG=True                          # Set to False in production
SECRET_KEY=your-secret-key         # Change in production
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your domain in production

# Stripe (optional)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## Testing

Create test files in each app:

```bash
touch products/tests.py
```

Run tests:
```bash
python manage.py test products
python manage.py test              # Run all tests
```

## Troubleshooting

### Issue: "No module named 'rest_framework'"
**Solution**: Install packages
```bash
pip install -r requirements.txt
```

### Issue: Static files warning
**Solution**: Already created the static directory and configured settings.py

### Issue: Port 8000 already in use
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

### Issue: Database locked
**Solution**: Delete `db.sqlite3` and run migrations again
```bash
rm db.sqlite3
python manage.py migrate
```

## Next Steps

1. **Add more product data** via admin or `populate_data` command
2. **Create cart & order endpoints** in a new views file
3. **Add payment processing** using Stripe API
4. **Frontend integration** - Create React/Vue frontend
5. **Authentication** - Implement JWT tokens for API
6. **Email notifications** - Setup email for orders
7. **Logging** - Configure logging for production
8. **Performance** - Add caching with Redis

## Useful Links

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Stripe API: https://stripe.com/docs/api
- PostgreSQL: https://www.postgresql.org/
- Redis: https://redis.io/

## Support

For more information, see:
- `README.md` - Project overview
- Django documentation
- DRF documentation
