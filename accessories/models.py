from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Category(models.Model):
    """Product category model"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Accessory(models.Model):
    """Pet accessory/product model"""
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='accessories')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='accessory_images/', blank=True, null=True)
    additional_images = models.JSONField(default=list, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., 10x5x3 cm")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]
        verbose_name_plural = 'Accessories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Ensure additional_images is always a list
        if self.additional_images is None:
            self.additional_images = []
        elif not isinstance(self.additional_images, list):
            self.additional_images = []
        super().save(*args, **kwargs)
    
    @property
    def in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return 'Out of Stock'
        elif self.stock_quantity < 10:
            return 'Low Stock'
        return 'In Stock'


class Cart(models.Model):
    """Shopping cart model"""
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cart_items')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'accessory']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.accessory.name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.accessory.price * self.quantity
