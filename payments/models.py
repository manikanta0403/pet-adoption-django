from django.db import models
from django.core.validators import MinValueValidator
from orders.models import Order
from users.models import User


class Payment(models.Model):
    """Payment model for order payments"""
    
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='razorpay')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='INR')
    
    # Razorpay details
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, null=True)
    
    # Refund details
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_id = models.CharField(max_length=100, blank=True, null=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['razorpay_payment_id']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment for Order #{self.order.order_number} - {self.get_status_display()}"
    
    def generate_transaction_id(self):
        """Generate unique transaction ID"""
        import random
        import string
        while True:
            txn_id = f"TXN{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}"
            if not Payment.objects.filter(transaction_id=txn_id).exists():
                return txn_id
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
