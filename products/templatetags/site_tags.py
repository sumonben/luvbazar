from django import template
from products.models import SiteSetting

register = template.Library()

@register.simple_tag
def get_site_settings():
    return SiteSetting.objects.first()