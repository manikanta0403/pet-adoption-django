from django.urls import path
from . import views

app_name = 'accessories'

urlpatterns = [
    path('', views.accessory_list, name='accessory_list'),
    path('<slug:slug>/', views.accessory_detail, name='accessory_detail'),
    path('<int:accessory_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/<int:cart_id>/update/', views.update_cart, name='update_cart'),
    path('cart/<int:cart_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
]

