# API Usage Examples

## Base URL
```
http://localhost:8000/api/v1/
```

## Products

### List All Products
```bash
curl http://localhost:8000/api/v1/products/
```

**Response:**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Wireless Bluetooth Headphones",
      "price": "79.99",
      "stock": 45,
      "image": "/media/products/2024/01/01/headphones.jpg",
      "slug": "wireless-bluetooth-headphones",
      "rating": "4.5",
      "category": {
        "id": 1,
        "name": "Electronics",
        "description": "...",
        "slug": "electronics"
      },
      "review_count": 5,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Product Details
```bash
curl http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/
```

**Response:**
```json
{
  "id": 1,
  "name": "Wireless Bluetooth Headphones",
  "description": "High-quality wireless headphones with noise cancellation...",
  "price": "79.99",
  "stock": 45,
  "image": "/media/products/2024/01/01/headphones.jpg",
  "slug": "wireless-bluetooth-headphones",
  "status": "active",
  "rating": "4.5",
  "category": {
    "id": 1,
    "name": "Electronics",
    "description": "...",
    "slug": "electronics"
  },
  "reviews": [
    {
      "id": 1,
      "user": "john_doe",
      "rating": 5,
      "comment": "Great product! Works perfectly.",
      "created_at": "2024-01-14T15:20:00Z"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Search Products
```bash
curl "http://localhost:8000/api/v1/products/search/?q=headphones"
```

### Get Featured Products
```bash
curl http://localhost:8000/api/v1/products/featured/
```

### Add Product Review
```bash
curl -X POST http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/add_review/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{
    "rating": 5,
    "comment": "Excellent quality and fast shipping!"
  }'
```

**Response:**
```json
{
  "id": 2,
  "user": "john_doe",
  "rating": 5,
  "comment": "Excellent quality and fast shipping!",
  "created_at": "2024-01-15T16:45:00Z"
}
```

### Create Product (Admin Only)
```bash
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token admin_token" \
  -d '{
    "name": "New Product",
    "description": "Product description...",
    "category": 1,
    "price": "99.99",
    "stock": 50,
    "slug": "new-product",
    "status": "active"
  }'
```

### Update Product (Admin Only)
```bash
curl -X PUT http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token admin_token" \
  -d '{
    "price": "89.99",
    "stock": 40
  }'
```

### Delete Product (Admin Only)
```bash
curl -X DELETE http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/ \
  -H "Authorization: Token admin_token"
```

## Categories

### List All Categories
```bash
curl http://localhost:8000/api/v1/products/categories/
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices and gadgets",
      "slug": "electronics"
    }
  ]
}
```

### Get Category Details
```bash
curl http://localhost:8000/api/v1/products/categories/electronics/
```

## Authentication

### Get Token (Setup Required)
First, create a token for your user in Django shell:
```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

### Using Token in Requests
```bash
curl -H "Authorization: Token your_token_key" \
  http://localhost:8000/api/v1/products/
```

## Pagination

By default, 10 items per page. To get a specific page:

```bash
curl "http://localhost:8000/api/v1/products/?page=2"
```

## Filtering

Filter by category:
```bash
curl "http://localhost:8000/api/v1/products/?category=electronics"
```

## Common Status Codes

- `200 OK` - Successful GET, PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Missing authentication token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Responses

```json
{
  "detail": "Not found."
}
```

```json
{
  "field_name": ["This field may not be blank."]
}
```

## Testing with Python Requests

```python
import requests

# Get all products
response = requests.get('http://localhost:8000/api/v1/products/')
products = response.json()

# Get specific product
product = requests.get('http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/')
print(product.json())

# Search products
results = requests.get('http://localhost:8000/api/v1/products/search/?q=phone')
print(results.json())

# Add review (authenticated)
headers = {'Authorization': 'Token your_token_here'}
review_data = {
    'rating': 5,
    'comment': 'Great product!'
}
response = requests.post(
    'http://localhost:8000/api/v1/products/wireless-bluetooth-headphones/add_review/',
    json=review_data,
    headers=headers
)
print(response.json())
```

## Testing with cURL and JQ

Install jq for pretty JSON output:
```bash
# macOS
brew install jq

# Ubuntu
sudo apt-get install jq

# Windows (with chocolatey)
choco install jq
```

Then use:
```bash
curl http://localhost:8000/api/v1/products/ | jq '.'
```
