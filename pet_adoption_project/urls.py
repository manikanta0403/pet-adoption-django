"""
URL configuration for pet_adoption_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pets.urls')),
    path('users/', include('users.urls')),
    path('accessories/', include('accessories.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Pet Adoption & Accessories Admin"
admin.site.site_title = "Pet Adoption Admin"
admin.site.index_title = "Welcome to Pet Adoption Management"
