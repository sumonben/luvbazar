from django.conf import settings
from products.models import  SiteSetting,Category, Product

def site_info(request):
        settings=SiteSetting.objects.first()
        categories=Category.objects.all()
        context={}
        context={
                'settings':settings,
                'categories': categories,
            }
        return context          
                
