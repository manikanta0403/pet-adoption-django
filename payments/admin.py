from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model"""
    
    list_display = ('order', 'user', 'payment_method', 'status', 'amount', 'payment_date', 'created_at')
    list_filter = ('payment_method', 'status', 'payment_date', 'created_at')
    search_fields = ('order__order_number', 'user__email', 'transaction_id', 'razorpay_payment_id')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at', 'payment_date', 'refund_date')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'user', 'payment_method', 'status')
        }),
        ('Amount Details', {
            'fields': ('amount', 'currency', 'refund_amount')
        }),
        ('Razorpay Details', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'payment_date', 'failure_reason')
        }),
        ('Refund Details', {
            'fields': ('refund_id', 'refund_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_success', 'mark_as_failed', 'process_refunds']
    
    def mark_as_success(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='success', payment_date=timezone.now())
        self.message_user(request, f"{queryset.count()} payments marked as success.")
    mark_as_success.short_description = "Mark selected payments as success"
    
    def mark_as_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f"{queryset.count()} payments marked as failed.")
    mark_as_failed.short_description = "Mark selected payments as failed"
    
    def process_refunds(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='refunded', refund_date=timezone.now())
        self.message_user(request, f"{queryset.count()} payments marked as refunded.")
    process_refunds.short_description = "Mark selected payments as refunded"
