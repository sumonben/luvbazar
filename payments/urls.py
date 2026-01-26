from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # SSL Commerz payment URLs
    path('ssl-commerz/initiate/<int:order_id>/', views.initiate_ssl_payment, name='ssl-initiate'),
    path('ssl-commerz/success/', views.ssl_payment_success, name='ssl-success'),
    path('ssl-commerz/fail/', views.ssl_payment_fail, name='ssl-fail'),
    path('ssl-commerz/cancel/', views.ssl_payment_cancel, name='ssl-cancel'),
    path('ssl-commerz/ipn/', views.ssl_payment_ipn, name='ssl-ipn'),
    
    # Payment status
    path('status/<int:order_id>/', views.payment_status, name='status'),
]
