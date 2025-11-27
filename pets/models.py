from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Pet(models.Model):
    """Pet model for adoption listings"""
    
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('fish', 'Fish'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending Adoption'),
        ('adopted', 'Adopted'),
    ]
    
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    description = models.TextField()
    vaccination_status = models.BooleanField(default=False)
    is_spayed_neutered = models.BooleanField(default=False)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    additional_images = models.JSONField(default=list, blank=True, null=True, help_text="List of additional image URLs")
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pets_created')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pet_type', 'status']),
            models.Index(fields=['location']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure additional_images is always a list
        if self.additional_images is None:
            self.additional_images = []
        elif not isinstance(self.additional_images, list):
            self.additional_images = []
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.get_pet_type_display()}"
    
    @property
    def is_available(self):
        return self.status == 'available'
    
    @property
    def get_additional_images(self):
        """Return additional_images as a list, defaulting to empty list"""
        return self.additional_images if self.additional_images is not None else []


class AdoptionRequest(models.Model):
    """Model for pet adoption requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(help_text="Why do you want to adopt this pet?")
    contact_preference = models.CharField(max_length=50, default='email')
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='adoptions_reviewed')
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-requested_at']
        unique_together = ['user', 'pet']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.pet.name} ({self.get_status_display()})"
