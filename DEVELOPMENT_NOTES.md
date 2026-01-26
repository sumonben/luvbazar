# Development Notes & Common Tasks

## Getting Started

### First Time Setup
```bash
cd d:\Django Project\ecommerz
.venv\Scripts\activate
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_data
python manage.py runserver
```

Then visit:
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/v1/products/

---

## Common Development Tasks

### 1. Adding a New Field to a Model

```python
# In products/models.py
class Product(models.Model):
    # ... existing fields ...
    discount_percentage = models.IntegerField(default=0)  # New field
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Creating a New Django App

```bash
python manage.py startapp reviews

# Then add 'reviews' to INSTALLED_APPS in settings.py
```

### 3. Accessing the Django Shell

```bash
python manage.py shell
```

Example commands:
```python
from products.models import Product, Category

# Get all products
products = Product.objects.all()

# Get specific product
product = Product.objects.get(slug='wireless-bluetooth-headphones')

# Create new category
category = Category.objects.create(
    name='Electronics',
    slug='electronics',
    description='Electronic devices'
)

# Create new product
product = Product.objects.create(
    name='Test Product',
    description='Test description',
    category=category,
    price=99.99,
    stock=10,
    slug='test-product',
    status='active'
)

# Filter products
active_products = Product.objects.filter(status='active')
expensive_products = Product.objects.filter(price__gte=100)

# Update product
product.price = 89.99
product.save()

# Delete product
product.delete()

# Count products
count = Product.objects.count()
```

### 4. Creating Test Data Manually

```python
# In Django shell
from django.contrib.auth.models import User
from products.models import Category, Product

# Create user
user = User.objects.create_user(username='testuser', password='testpass123')

# Create category
cat = Category.objects.create(name='Gadgets', slug='gadgets')

# Create product
product = Product.objects.create(
    name='Smart Watch',
    description='Advanced wearable device',
    category=cat,
    price=199.99,
    stock=25,
    slug='smart-watch',
    status='active'
)
```

### 5. Dumping and Loading Data

```bash
# Export data
python manage.py dumpdata > backup.json

# Import data
python manage.py loaddata backup.json

# Export specific app
python manage.py dumpdata products > products_backup.json
```

### 6. Running Management Commands

```bash
# Our custom populate_data command
python manage.py populate_data

# Built-in Django commands
python manage.py createsuperuser
python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic
python manage.py flush  # Clear database (dangerous!)
```

---

## API Testing

### Using cURL

```bash
# List products
curl http://localhost:8000/api/v1/products/

# Get specific product
curl http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/

# Search
curl "http://localhost:8000/api/v1/products/search/?q=phone"

# Create product (requires authentication)
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token" \
  -d '{
    "name": "New Product",
    "description": "Description",
    "price": "99.99",
    "stock": 50,
    "slug": "new-product"
  }'

# Add review
curl -X POST http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/add_review/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token" \
  -d '{
    "rating": 5,
    "comment": "Great product!"
  }'
```

### Using Python Requests

```python
import requests

# Setup
BASE_URL = 'http://localhost:8000/api/v1/'
HEADERS = {'Authorization': 'Token your_token_here'}

# Get all products
response = requests.get(f'{BASE_URL}products/')
products = response.json()
print(products)

# Get specific product
response = requests.get(f'{BASE_URL}products/wireless-bluetooth-headphones/')
product = response.json()
print(product)

# Search
response = requests.get(f'{BASE_URL}products/search/?q=phone')
results = response.json()
print(results)

# Add review
review_data = {
    'rating': 5,
    'comment': 'Excellent quality!'
}
response = requests.post(
    f'{BASE_URL}products/wireless-bluetooth-headphones/add_review/',
    json=review_data,
    headers=HEADERS
)
print(response.json())

# Create product
product_data = {
    'name': 'New Product',
    'description': 'Description here',
    'category': 1,
    'price': '99.99',
    'stock': 50,
    'slug': 'new-product'
}
response = requests.post(
    f'{BASE_URL}products/',
    json=product_data,
    headers=HEADERS
)
print(response.json())
```

---

## Database Queries

### Advanced Django ORM

```python
from django.db.models import Q, Count, Avg
from products.models import Product

# Complex queries
products = Product.objects.filter(
    Q(price__gte=100) | Q(stock__lt=5),
    status='active'
)

# Count reviews per product
products = Product.objects.annotate(
    review_count=Count('reviews')
).order_by('-review_count')

# Average rating
products = Product.objects.annotate(
    avg_rating=Avg('reviews__rating')
)

# Get products in category
products = Product.objects.select_related('category').filter(
    category__slug='electronics'
)

# Distinct results
categories = Product.objects.values('category').distinct()

# Raw SQL (if needed)
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM products_product WHERE price > %s", [100])
```

---

## Adding Features

### 1. Add Authentication Tokens

```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

Use in API:
```bash
curl -H "Authorization: Token YOUR_TOKEN_KEY" \
  http://localhost:8000/api/v1/products/
```

### 2. Create Custom Admin Actions

```python
# In app/admin.py
def mark_active(modeladmin, request, queryset):
    queryset.update(status='active')
mark_active.short_description = "Mark selected as active"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [mark_active]
```

### 3. Add Filtering to API

In views.py, use DRF filters:
```bash
pip install django-filter
```

```python
from django_filters import rest_framework as filters
from rest_framework import viewsets
from products.models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['category', 'status', 'price']
```

### 4. Add Search to API

```python
from rest_framework import filters

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
```

---

## Debugging

### Debug Toolbar

```bash
pip install django-debug-toolbar
```

Add to INSTALLED_APPS and MIDDLEWARE in settings.py.

### Print Statements

```python
# In views
print("Debug info:", variable_name)

# In models
print(f"Creating product: {self.name}")
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Django Shell Debugging

```bash
python manage.py shell
```

```python
from products.models import Product
product = Product.objects.first()
print(product.__dict__)  # See all fields
```

---

## Performance Tips

1. **Use select_related() for ForeignKey**
   ```python
   products = Product.objects.select_related('category')
   ```

2. **Use prefetch_related() for reverse FK**
   ```python
   products = Product.objects.prefetch_related('reviews')
   ```

3. **Index frequently queried fields**
   ```python
   class Meta:
       indexes = [
           models.Index(fields=['slug']),
           models.Index(fields=['status']),
       ]
   ```

4. **Use bulk operations**
   ```python
   Product.objects.bulk_create([product1, product2])
   ```

5. **Cache querysets**
   ```python
   products = list(Product.objects.all())  # Caches in memory
   ```

---

## Git Workflow

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Django e-commerce project"

# Create branch for feature
git checkout -b feature/add-wishlist

# Make changes
git add products/models.py
git commit -m "Add wishlist functionality"

# Merge back to main
git checkout main
git merge feature/add-wishlist
```

---

## Deployment Preparation

1. **Set DEBUG=False in .env**
2. **Update ALLOWED_HOSTS** with your domain
3. **Change SECRET_KEY** to a new secure value
4. **Setup environment variables**
5. **Configure production database**
6. **Collect static files**: `python manage.py collectstatic`
7. **Setup HTTPS/SSL**
8. **Configure email backend**
9. **Setup logging and monitoring**

---

## Useful Django Commands Reference

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Start dev server |
| `python manage.py shell` | Interactive Python shell |
| `python manage.py makemigrations` | Create migrations |
| `python manage.py migrate` | Apply migrations |
| `python manage.py test` | Run tests |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py dumpdata` | Export data |
| `python manage.py loaddata` | Import data |
| `python manage.py flush` | Clear database |
| `python manage.py check` | Check configuration |
| `python manage.py collectstatic` | Collect static files |
| `python manage.py dbshell` | Database shell |
| `python manage.py populate_data` | Load sample data |

---

## Useful Links

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- DRF Serializers: https://www.django-rest-framework.org/api-guide/serializers/
- PostgreSQL: https://www.postgresql.org/docs/

---

## Notes & Tips

- Always create migrations after model changes
- Use `.select_related()` to reduce database queries
- Test API endpoints regularly during development
- Keep `requirements.txt` updated
- Use `.gitignore` to avoid committing sensitive files
- Document your API endpoints
- Write tests for critical functionality
- Use environment variables for configuration

---

Happy Coding! 🚀
