from django.urls import path
from . import views

urlpatterns = [
    path('create_factus/', views.create_factura, name='create_factura'),
]
