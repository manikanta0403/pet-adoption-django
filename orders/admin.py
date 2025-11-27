from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem"""
    model = OrderItem
    readonly_fields = ('accessory', 'quantity', 'price_at_purchase', 'subtotal')
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model"""
    
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'shipping_name', 'tracking_number')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'shipped_at', 'delivered_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Shipping Address', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address', 
                      'shipping_city', 'shipping_state', 'shipping_zip_code')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('tracking_number', 'shipped_at', 'delivered_at')
        }),
        ('Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'cancel_orders']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f"{queryset.count()} orders marked as processing.")
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='shipped', shipped_at=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def cancel_orders(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} orders cancelled.")
    cancel_orders.short_description = "Cancel selected orders"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderItem model"""
    
    list_display = ('order', 'accessory', 'quantity', 'price_at_purchase', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__order_number', 'accessory__name')
    readonly_fields = ('order', 'accessory', 'quantity', 'price_at_purchase', 'subtotal')
