"""
Script to add pet data to the database.
Run this script to add pets with their details.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption_project.settings')
django.setup()

from pets.models import Pet
from users.models import User

def add_pet(name, pet_type, breed, age, gender, description, location, adoption_fee, 
            vaccination_status=False, is_spayed_neutered=False, weight=None, status='available', image_path=None):
    """Add a pet to the database"""
    
    # Get or create admin user for created_by
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create a superuser first.")
        return None
    
    pet = Pet.objects.create(
        name=name,
        pet_type=pet_type,
        breed=breed,
        age=age,
        gender=gender,
        description=description,
        location=location,
        adoption_fee=adoption_fee,
        vaccination_status=vaccination_status,
        is_spayed_neutered=is_spayed_neutered,
        weight=weight,
        status=status,
        created_by=admin_user
    )
    
    # Add image if provided
    if image_path and os.path.exists(image_path):
        from django.core.files import File
        with open(image_path, 'rb') as f:
            pet.image.save(os.path.basename(image_path), File(f), save=True)
    
    print(f"✓ Added pet: {pet.name} (ID: {pet.id})")
    return pet

if __name__ == "__main__":
    print("=" * 50)
    print("Pet Data Addition Script")
    print("=" * 50)
    print("\nInstructions:")
    print("1. Prepare pet images in the 'media/pet_images/' folder")
    print("2. Use this script or manually add pets via admin panel")
    print("3. Or provide pet details below to add programmatically\n")
    
    # Example: Add the existing "Leo" pet if not exists
    if not Pet.objects.filter(name="Leo").exists():
        print("\nAdding example pet: Leo")
        add_pet(
            name="Leo",
            pet_type="dog",
            breed="Labrador",
            age=1,
            gender="male",
            description="Friendly and playful dog looking for a loving home. Leo is very energetic and loves to play fetch.",
            location="Kovvur",
            adoption_fee=5666.27,
            vaccination_status=True,
            is_spayed_neutered=False,
            weight=5,
            status="available"
        )
    else:
        print("Pet 'Leo' already exists.")
    
    print("\n" + "=" * 50)
    print("To add more pets:")
    print("1. Use Django admin: http://localhost:8000/admin/pets/pet/add/")
    print("2. Or modify this script and add more pets programmatically")
    print("=" * 50)

