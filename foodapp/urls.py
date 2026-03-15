from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
]