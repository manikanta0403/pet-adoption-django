from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Pet, AdoptionRequest
from .forms import AdoptionRequestForm


def home(request):
    """Home page with featured pets"""
    # Get featured pets - try to get different types
    all_available = Pet.objects.filter(status='available')
    featured_pets = all_available.order_by('?')[:6]  # Random selection for variety
    recent_pets = all_available.order_by('-created_at')[:6]
    
    context = {
        'featured_pets': featured_pets,
        'recent_pets': recent_pets,
    }
    return render(request, 'pets/home.html', context)


def pet_list(request):
    """List all available pets with search and filter"""
    pets = Pet.objects.filter(status='available')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by pet type
    pet_type = request.GET.get('pet_type', '')
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        pets = pets.filter(location__icontains=location)
    
    # Pagination
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'pet_type': pet_type,
        'location': location,
        'pet_types': Pet.PET_TYPES,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    """Pet detail view"""
    pet = get_object_or_404(Pet, pk=pk)
    has_requested = False
    
    if request.user.is_authenticated:
        has_requested = AdoptionRequest.objects.filter(user=request.user, pet=pet).exists()
    
    context = {
        'pet': pet,
        'has_requested': has_requested,
    }
    return render(request, 'pets/pet_detail.html', context)


@login_required
def request_adoption(request, pk):
    """Request adoption for a pet"""
    pet = get_object_or_404(Pet, pk=pk)
    
    # Check if already requested
    if AdoptionRequest.objects.filter(user=request.user, pet=pet).exists():
        messages.warning(request, 'You have already requested adoption for this pet.')
        return redirect('pet_detail', pk=pk)
    
    # Check if pet is available
    if pet.status != 'available':
        messages.error(request, 'This pet is not available for adoption.')
        return redirect('pet_detail', pk=pk)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.pet = pet
            adoption_request.save()
            pet.status = 'pending'
            pet.save()
            messages.success(request, 'Your adoption request has been submitted successfully!')
            return redirect('pet_detail', pk=pk)
    else:
        form = AdoptionRequestForm()
    
    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'pets/request_adoption.html', context)


@login_required
def my_adoptions(request):
    """View user's adoption requests"""
    adoption_requests = AdoptionRequest.objects.filter(user=request.user).order_by('-requested_at')
    return render(request, 'pets/my_adoptions.html', {'adoption_requests': adoption_requests})
