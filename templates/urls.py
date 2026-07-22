"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from products.views import index, products_list, product_detail, category_detail, about, contact, add_review
from products.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
from users.views import (
    register, login_view, logout_view, profile, profile_update,
    change_password, password_reset, orders_list, order_detail,send_otp_sms, verify_otp_code
)
from cart.views import (
    cart_view, add_to_cart, remove_from_cart, update_cart_item,
    clear_cart, checkout, order_confirmation, cart_count, get_address_by_phone
)

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    
    # Frontend pages
    path('', index, name='home'),
    path('products/', products_list, name='products-list'),
    path('products/<slug:slug>/', product_detail, name='product-detail'),
    path('products/<slug:slug>/review/', add_review, name='add-review'),
    path('category/<slug:slug>/', category_detail, name='category'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
    # Authentication
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile, name='profile'),
    path('auth/profile/update/', profile_update, name='profile-update'),
    path('auth/change-password/', change_password, name='change-password'),
    path('auth/password-reset/', password_reset, name='password-reset'),
    path('auth/send-otp/', send_otp_sms, name='send-otp'),
    path('auth/verify-otp/', verify_otp_code, name='verify-otp'),
    # Shopping Cart
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update-cart-item'),
    path('cart/clear/', clear_cart, name='clear-cart'),
    path('cart/count/', cart_count, name='cart-count'),
    path('api/address-by-phone/', get_address_by_phone, name='address-by-phone'),
    
    # Checkout & Orders
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders_list, name='orders-list'),
    path('orders/<int:order_id>/', order_detail, name='order-detail'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order-confirmation'),
    
    # Payments
    path('payments/', include('payments.urls')),
    
    # Region API
    path('', include('region.urls')),
    
    # API
    # path('api/v1/', include('rest_framework.urls')),
    # path('api/v1/products/', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)