# Project File Structure

## Directory Tree

```
ecommerz/
│
├── 📁 .venv/                          # Virtual environment (do not commit)
│   └── Scripts/                       # Python executable and scripts
│
├── 📁 ecommerce/                      # Main project configuration
│   ├── __init__.py
│   ├── settings.py                    # ⭐ Main Django settings
│   ├── urls.py                        # ⭐ URL routing configuration
│   ├── asgi.py                        # ASGI config (for async)
│   ├── wsgi.py                        # WSGI config (for production)
│   └── settings_common.py             # Common settings (reusable)
│
├── 📁 products/                       # Product Catalog App ⭐
│   ├── migrations/                    # Database migrations
│   │   └── 0001_initial.py           # Initial migration
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py      # ⭐ Generate sample data
│   ├── __init__.py
│   ├── admin.py                       # Admin interface configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # ⭐ Category, Product, Review models
│   ├── serializers.py                 # ⭐ DRF serializers for API
│   ├── views.py                       # ⭐ API viewsets
│   ├── urls.py                        # ⭐ URL routing for products
│   └── tests.py                       # Unit tests
│
├── 📁 orders/                         # Order Management App ⭐
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py                       # Admin interface
│   ├── apps.py
│   ├── models.py                      # ⭐ Order, OrderItem models
│   ├── views.py                       # API views
│   └── tests.py
│
├── 📁 cart/                           # Shopping Cart App
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py                       # Admin interface
│   ├── apps.py
│   ├── models.py                      # ⭐ Cart, CartItem models
│   ├── views.py                       # API views
│   └── tests.py
│
├── 📁 payments/                       # Payment Processing App
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py                       # Admin interface
│   ├── apps.py
│   ├── models.py                      # ⭐ Payment model
│   ├── views.py                       # API views
│   └── tests.py
│
├── 📁 users/                          # User Management App
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                       # Admin interface
│   ├── apps.py
│   ├── models.py                      # Ready for custom user models
│   ├── views.py                       # API views
│   └── tests.py
│
├── 📁 static/                         # Static Files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
│
├── 📁 media/                          # User-uploaded files
│   └── products/                      # Product images
│
├── 📁 templates/                      # HTML Templates
│   └── base.html                      # Base template (ready for use)
│
├── 🔵 db.sqlite3                      # SQLite Database (auto-generated)
│
├── 🔵 manage.py                       # ⭐ Django management script
│
├── 📄 requirements.txt                # ⭐ Python dependencies
├── 📄 .env.example                    # Environment variables template
├── 📄 .gitignore                      # Git ignore file
│
├── 📄 README.md                       # ⭐ Project documentation
├── 📄 QUICKSTART.md                   # ⭐ Getting started guide
├── 📄 DEVELOPMENT_NOTES.md            # ⭐ Development tips & tricks
├── 📄 API_EXAMPLES.md                 # ⭐ API usage examples
├── 📄 PROJECT_SUMMARY.md              # ⭐ Project overview
│
├── 📄 Dockerfile                      # Docker configuration
└── 📄 docker-compose.yml              # Docker Compose configuration
```

## File Descriptions

### 🌟 Essential Files (Start Here)

| File | Purpose |
|------|---------|
| `manage.py` | Django management command interface |
| `requirements.txt` | All Python package dependencies |
| `README.md` | Complete project documentation |
| `QUICKSTART.md` | Quick setup and usage guide |
| `PROJECT_SUMMARY.md` | Project overview and architecture |

### Configuration Files

| File | Purpose |
|------|---------|
| `ecommerce/settings.py` | Main Django configuration |
| `ecommerce/urls.py` | URL routing for entire project |
| `.env.example` | Template for environment variables |
| `.gitignore` | Git ignore patterns |
| `Dockerfile` | Docker container configuration |
| `docker-compose.yml` | Multi-container Docker setup |

### App Files Structure

Each app follows this pattern:
```
app_name/
├── migrations/              # Database schema changes
├── management/commands/     # Custom management commands
├── models.py               # Database models (⭐ Start here for each app)
├── views.py                # API views/viewsets (⭐ API logic)
├── serializers.py          # DRF serializers (products app only)
├── urls.py                 # URL routing (products app only)
├── admin.py                # Admin panel configuration
├── tests.py                # Unit tests
└── apps.py                 # App configuration
```

### Database

- **SQLite** (default): `db.sqlite3` - Auto-created after migrations
- **PostgreSQL** (production): Configure in settings.py

## Key Files to Edit

When developing, you'll typically work with:

1. **Models** - `products/models.py`, `orders/models.py`, etc.
2. **Serializers** - `products/serializers.py` (for API)
3. **Views** - `products/views.py` (for API endpoints)
4. **URLs** - `ecommerce/urls.py`, `products/urls.py`
5. **Settings** - `ecommerce/settings.py`

## Common File Operations

### Add a New Field to a Model
```python
# Edit products/models.py → Product model
# Then run:
python manage.py makemigrations
python manage.py migrate
```

### Register Model in Admin
```python
# Edit app/admin.py
from .models import YourModel
@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2']
```

### Create API Endpoint
```python
# Edit products/serializers.py
# Edit products/views.py
# Edit products/urls.py
```

## Important Notes

⚠️ **Never commit to version control:**
- `.venv/` directory
- `db.sqlite3` file
- `.env` file (with secrets)
- `__pycache__/` directories
- `.pyc` files

✅ **Always commit:**
- Model changes (migrations)
- Views and logic
- Configuration templates (.env.example)
- Documentation
- Test files

## Quick Reference

### To find...
- Database models → Look in `*/models.py`
- API endpoints → Look in `*/views.py` and `*/urls.py`
- Admin panel setup → Look in `*/admin.py`
- Configuration → Look in `ecommerce/settings.py`
- Dependencies → Look in `requirements.txt`
- Documentation → Look in `README.md`, `QUICKSTART.md`

### To add...
- New model → Edit `app/models.py`, then migrate
- New API endpoint → Edit `app/serializers.py`, `app/views.py`, `app/urls.py`
- New field → Edit model, then `makemigrations` and `migrate`
- New app → Run `python manage.py startapp app_name`

---

**Marked with ⭐ are the files you'll edit most frequently during development.**
