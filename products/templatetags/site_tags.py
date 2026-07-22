from django import template
from django.core.cache import cache
from products.models import SiteSetting

register = template.Library()


@register.simple_tag
def get_site_settings():
    site_settings = cache.get('site_settings')
    if site_settings is None:
        site_settings = SiteSetting.objects.first()
        cache.set('site_settings', site_settings, 3600)
    return site_settings


@register.filter
def subtract(value, arg):
    return value - arg
