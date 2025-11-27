from django import forms
from .models import AdoptionRequest


class AdoptionRequestForm(forms.ModelForm):
    """Form for adoption request"""
    
    class Meta:
        model = AdoptionRequest
        fields = ('message', 'contact_preference')
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us why you want to adopt this pet...'
            }),
            'contact_preference': forms.Select(attrs={'class': 'form-control'}),
        }

