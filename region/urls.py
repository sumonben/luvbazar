from django.urls import path
from . import views

app_name = 'region'

urlpatterns = [
    path('api/divisions/', views.get_divisions, name='api-divisions'),
    path('api/districts/', views.get_districts, name='api-districts'),
    path('api/upazillas/', views.get_upazillas, name='api-upazillas'),
    path('api/unions/', views.get_unions, name='api-unions'),
]
