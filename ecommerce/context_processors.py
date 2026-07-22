from django.core.cache import cache
from products.models import SiteSetting, Category, Product


def site_info(request):
    site_settings = cache.get('site_settings')
    if site_settings is None:
        site_settings = SiteSetting.objects.first()
        cache.set('site_settings', site_settings, 3600)  # cache 1 hour

    categories = cache.get('all_categories')
    if categories is None:
        categories = list(Category.objects.only('id', 'name', 'slug', 'image', 'serial').order_by('serial', 'name'))
        cache.set('all_categories', categories, 600)  # cache 10 minutes

    return {
        'settings': site_settings,
        'categories': categories,
    }

