from django.contrib import admin
from .models import Category, Accessory, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    """Admin configuration for Accessory model"""
    
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Product Details', {
            'fields': ('brand', 'weight', 'dimensions')
        }),
        ('Images', {
            'fields': ('image', 'additional_images')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_not_featured', 'activate_products', 'deactivate_products']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} products marked as featured.")
    mark_as_featured.short_description = "Mark selected products as featured"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} products unmarked as featured.")
    mark_as_not_featured.short_description = "Unmark selected products as featured"
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} products activated.")
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} products deactivated.")
    deactivate_products.short_description = "Deactivate selected products"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart model"""
    
    list_display = ('user', 'accessory', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__email', 'accessory__name')
    readonly_fields = ('added_at', 'updated_at')
