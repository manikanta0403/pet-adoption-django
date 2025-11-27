from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/adopt/', views.request_adoption, name='request_adoption'),
    path('my-adoptions/', views.my_adoptions, name='my_adoptions'),
]

