from django.contrib import admin
from .models import Pet, AdoptionRequest


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Admin configuration for Pet model"""
    
    list_display = ('name', 'pet_type', 'breed', 'age', 'gender', 'status', 'location', 'adoption_fee', 'created_at')
    list_filter = ('pet_type', 'gender', 'status', 'vaccination_status', 'is_spayed_neutered', 'created_at')
    search_fields = ('name', 'breed', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'age', 'gender', 'weight')
        }),
        ('Health Information', {
            'fields': ('vaccination_status', 'is_spayed_neutered')
        }),
        ('Details', {
            'fields': ('description', 'location', 'adoption_fee', 'status')
        }),
        ('Images', {
            'fields': ('image', 'additional_images')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    """Admin configuration for AdoptionRequest model"""
    
    list_display = ('user', 'pet', 'status', 'requested_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'requested_at', 'reviewed_at')
    search_fields = ('user__email', 'user__username', 'pet__name', 'message')
    readonly_fields = ('requested_at',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'pet', 'status', 'message', 'contact_preference')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('requested_at',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', reviewed_by=request.user, reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} adoption requests approved.")
    approve_requests.short_description = "Approve selected adoption requests"
    
    def reject_requests(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='rejected', reviewed_by=request.user, reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} adoption requests rejected.")
    reject_requests.short_description = "Reject selected adoption requests"
