"""
Script to add sample pets to the database
Adds 10 pets of each type with realistic details
"""
import os
import django
import requests
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption_project.settings')
django.setup()

from pets.models import Pet
from users.models import User

# Sample pet data - 10 of each type
PET_DATA = {
    'dog': [
        {'name': 'Max', 'breed': 'Golden Retriever', 'age': 2, 'gender': 'male', 'weight': 28.5, 
         'description': 'Friendly and energetic Golden Retriever. Loves playing fetch and going on walks. Great with kids and other pets. House-trained and well-behaved.', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 8000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=800'},
        {'name': 'Bella', 'breed': 'Labrador', 'age': 1, 'gender': 'female', 'weight': 25.0,
         'description': 'Playful and affectionate Labrador. Very intelligent and easy to train. Enjoys swimming and outdoor activities.', 
         'location': 'Delhi, NCR', 'adoption_fee': 7500.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800'},
        {'name': 'Charlie', 'breed': 'German Shepherd', 'age': 3, 'gender': 'male', 'weight': 35.0,
         'description': 'Loyal and protective German Shepherd. Excellent guard dog. Requires an active family who can provide regular exercise and training.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 10000.00, 'vaccination_status': True, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1589941029190-1c1b1e9c2c2b?w=800'},
        {'name': 'Luna', 'breed': 'Siberian Husky', 'age': 2, 'gender': 'female', 'weight': 22.0,
         'description': 'Beautiful blue-eyed Husky with a friendly personality. Loves cold weather and long walks. Very social and good with children.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 12000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1517849845537-4d257902454a?w=800'},
        {'name': 'Rocky', 'breed': 'Bulldog', 'age': 4, 'gender': 'male', 'weight': 23.0,
         'description': 'Gentle and calm Bulldog. Perfect for apartment living. Low maintenance and loves cuddling. Gets along well with everyone.', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 15000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1517849845537-4d257902454a?w=800'},
        {'name': 'Daisy', 'breed': 'Beagle', 'age': 1, 'gender': 'female', 'weight': 12.0,
         'description': 'Curious and friendly Beagle. Great sense of smell and loves exploring. Perfect for active families who enjoy outdoor activities.', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 7000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1534361960057-19889c938e8c?w=800'},
        {'name': 'Buddy', 'breed': 'Poodle', 'age': 2, 'gender': 'male', 'weight': 15.0,
         'description': 'Intelligent and hypoallergenic Poodle. Great for families with allergies. Easy to train and very obedient.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 9000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1616190174712-18e4e6dcc4b3?w=800'},
        {'name': 'Molly', 'breed': 'Shih Tzu', 'age': 3, 'gender': 'female', 'weight': 7.0,
         'description': 'Small and adorable Shih Tzu. Perfect lap dog. Very affectionate and loves being pampered. Great for seniors or small families.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 6000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=800'},
        {'name': 'Cooper', 'breed': 'Boxer', 'age': 2, 'gender': 'male', 'weight': 30.0,
         'description': 'Energetic and playful Boxer. Loves playing and requires regular exercise. Very loyal and protective of family.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 8500.00, 'vaccination_status': True, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1517849845537-4d257902454a?w=800'},
        {'name': 'Sadie', 'breed': 'Australian Shepherd', 'age': 1, 'gender': 'female', 'weight': 20.0,
         'description': 'Smart and active Australian Shepherd. Needs plenty of exercise and mental stimulation. Great for active owners who love hiking.', 
         'location': 'Surat, Gujarat', 'adoption_fee': 11000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=800'},
    ],
    'cat': [
        {'name': 'Whiskers', 'breed': 'Persian', 'age': 2, 'gender': 'male', 'weight': 4.5,
         'description': 'Beautiful long-haired Persian cat. Calm and gentle personality. Loves lounging around and being brushed.', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 5000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
        {'name': 'Luna', 'breed': 'Siamese', 'age': 1, 'gender': 'female', 'weight': 3.5,
         'description': 'Elegant Siamese cat with striking blue eyes. Very vocal and loves attention. Intelligent and playful.', 
         'location': 'Delhi, NCR', 'adoption_fee': 4500.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=800'},
        {'name': 'Shadow', 'breed': 'Maine Coon', 'age': 3, 'gender': 'male', 'weight': 8.0,
         'description': 'Large and majestic Maine Coon. Very friendly and dog-like personality. Great with children and other pets.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 7000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?w=800'},
        {'name': 'Bella', 'breed': 'British Shorthair', 'age': 2, 'gender': 'female', 'weight': 5.0,
         'description': 'Cute and round-faced British Shorthair. Calm and easygoing. Perfect indoor cat for any family.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 5500.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800'},
        {'name': 'Oscar', 'breed': 'Bengal', 'age': 2, 'gender': 'male', 'weight': 6.0,
         'description': 'Exotic-looking Bengal cat with wild patterns. Very active and playful. Needs lots of toys and attention.', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 8000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
        {'name': 'Mittens', 'breed': 'Ragdoll', 'age': 1, 'gender': 'female', 'weight': 5.5,
         'description': 'Fluffy Ragdoll cat. Very docile and loves being held. Gets along well with everyone including dogs.', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 6000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=800'},
        {'name': 'Simba', 'breed': 'Orange Tabby', 'age': 3, 'gender': 'male', 'weight': 4.5,
         'description': 'Friendly orange tabby cat. Very social and loves playing. Great mouser and family companion.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 3500.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?w=800'},
        {'name': 'Princess', 'breed': 'Turkish Angora', 'age': 2, 'gender': 'female', 'weight': 4.0,
         'description': 'Elegant Turkish Angora with silky white fur. Playful and affectionate. Loves climbing and exploring.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 5000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800'},
        {'name': 'Tiger', 'breed': 'Tabby', 'age': 4, 'gender': 'male', 'weight': 5.5,
         'description': 'Sweet tabby cat with beautiful stripes. Very calm and easygoing. Perfect for first-time cat owners.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 3000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
        {'name': 'Cleo', 'breed': 'Egyptian Mau', 'age': 1, 'gender': 'female', 'weight': 3.5,
         'description': 'Elegant Egyptian Mau with spotted coat. Very active and loves running. Fastest domestic cat breed!', 
         'location': 'Surat, Gujarat', 'adoption_fee': 6500.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=800'},
    ],
    'bird': [
        {'name': 'Rio', 'breed': 'Parrot', 'age': 3, 'gender': 'male', 'weight': 0.4,
         'description': 'Colorful and intelligent parrot. Can learn words and phrases. Very social and loves interaction.', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 15000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1535530992830-e3d9d8c45de3?w=800'},
        {'name': 'Kiwi', 'breed': 'Lovebird', 'age': 1, 'gender': 'female', 'weight': 0.05,
         'description': 'Small and affectionate lovebird. Very colorful and playful. Perfect for bird lovers.', 
         'location': 'Delhi, NCR', 'adoption_fee': 3000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'},
        {'name': 'Sunny', 'breed': 'Canary', 'age': 2, 'gender': 'male', 'weight': 0.02,
         'description': 'Beautiful yellow canary with melodious voice. Easy to care for and perfect for small spaces.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 2000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
        {'name': 'Pepper', 'breed': 'Cockatiel', 'age': 2, 'gender': 'female', 'weight': 0.1,
         'description': 'Friendly cockatiel that loves whistling. Can learn tunes and is very interactive.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 4000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1512531386531-89a1a8e14b8d?w=800'},
        {'name': 'Blue', 'breed': 'Budgerigar', 'age': 1, 'gender': 'male', 'weight': 0.03,
         'description': 'Cheerful blue budgie. Very playful and can learn to talk. Great starter bird for beginners.', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 1500.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
        {'name': 'Mango', 'breed': 'Sun Conure', 'age': 2, 'gender': 'male', 'weight': 0.12,
         'description': 'Vibrant orange and yellow sun conure. Very playful and loves attention. Makes great sounds!', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 12000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1535530992830-e3d9d8c45de3?w=800'},
        {'name': 'Zazu', 'breed': 'African Grey', 'age': 4, 'gender': 'male', 'weight': 0.5,
         'description': 'Highly intelligent African Grey parrot. Excellent at mimicking speech. Requires experienced owner.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 25000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'},
        {'name': 'Ruby', 'breed': 'Finch', 'age': 1, 'gender': 'female', 'weight': 0.01,
         'description': 'Tiny and adorable finch. Easy to care for and loves company. Perfect for small apartments.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 1000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
        {'name': 'Aurora', 'breed': 'Macaw', 'age': 5, 'gender': 'female', 'weight': 1.2,
         'description': 'Magnificent blue and gold macaw. Large and requires experienced owner. Very affectionate once bonded.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 35000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1512531386531-89a1a8e14b8d?w=800'},
        {'name': 'Tweety', 'breed': 'Canary', 'age': 1, 'gender': 'male', 'weight': 0.02,
         'description': 'Cheerful yellow canary with beautiful singing voice. Low maintenance and perfect pet bird.', 
         'location': 'Surat, Gujarat', 'adoption_fee': 1800.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'},
    ],
    'rabbit': [
        {'name': 'Bunny', 'breed': 'Holland Lop', 'age': 1, 'gender': 'male', 'weight': 1.5,
         'description': 'Adorable floppy-eared Holland Lop rabbit. Very gentle and loves being petted. Great with kids!', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 2500.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800'},
        {'name': 'Coco', 'breed': 'Rex Rabbit', 'age': 2, 'gender': 'female', 'weight': 3.0,
         'description': 'Beautiful Rex rabbit with velvety soft fur. Very calm and friendly. Perfect indoor pet.', 
         'location': 'Delhi, NCR', 'adoption_fee': 3000.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'},
        {'name': 'Snowball', 'breed': 'Angora', 'age': 1, 'gender': 'male', 'weight': 2.5,
         'description': 'Fluffy white Angora rabbit. Requires regular grooming. Very docile and loves attention.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 3500.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800'},
        {'name': 'Oreo', 'breed': 'Dutch Rabbit', 'age': 2, 'gender': 'female', 'weight': 2.0,
         'description': 'Cute black and white Dutch rabbit. Very playful and curious. Great for first-time rabbit owners.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 2800.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'},
        {'name': 'Thumper', 'breed': 'Flemish Giant', 'age': 2, 'gender': 'male', 'weight': 6.0,
         'description': 'Gentle giant rabbit. Very calm and friendly despite large size. Great with families.', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 4000.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800'},
        {'name': 'Luna', 'breed': 'Lionhead', 'age': 1, 'gender': 'female', 'weight': 1.8,
         'description': 'Cute Lionhead rabbit with fluffy mane. Very playful and energetic. Loves toys and treats.', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 3000.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'},
        {'name': 'Pepper', 'breed': 'Mini Lop', 'age': 2, 'gender': 'male', 'weight': 1.5,
         'description': 'Small and adorable Mini Lop. Very affectionate and loves cuddling. Perfect apartment pet.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 2500.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800'},
        {'name': 'Honey', 'breed': 'Californian', 'age': 1, 'gender': 'female', 'weight': 3.5,
         'description': 'Beautiful white Californian rabbit with dark points. Very gentle and easy to handle.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 3200.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'},
        {'name': 'Midnight', 'breed': 'Rex', 'age': 2, 'gender': 'male', 'weight': 3.0,
         'description': 'Sleek black Rex rabbit with unique velvety fur. Very calm and enjoys being petted.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 2800.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800'},
        {'name': 'Daisy', 'breed': 'Netherland Dwarf', 'age': 1, 'gender': 'female', 'weight': 1.0,
         'description': 'Tiny and cute Netherland Dwarf. Very active and playful. Perfect for small spaces.', 
         'location': 'Surat, Gujarat', 'adoption_fee': 3500.00, 'vaccination_status': False, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'},
    ],
    'fish': [
        {'name': 'Goldie', 'breed': 'Goldfish', 'age': 1, 'gender': 'unknown', 'weight': 0.1,
         'description': 'Beautiful golden goldfish. Easy to care for and perfect for beginners. Very hardy and long-lived.', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 500.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
        {'name': 'Nemo', 'breed': 'Clownfish', 'age': 1, 'gender': 'unknown', 'weight': 0.05,
         'description': 'Colorful orange and white clownfish. Requires saltwater aquarium. Very popular and active fish.', 
         'location': 'Delhi, NCR', 'adoption_fee': 1500.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1594736797933-d0e4a440365b?w=800'},
        {'name': 'Bubbles', 'breed': 'Guppy', 'age': 0, 'gender': 'unknown', 'weight': 0.01,
         'description': 'Colorful and active guppy. Easy to breed and care for. Perfect for community tanks.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 200.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c93a?w=800'},
        {'name': 'Angel', 'breed': 'Angelfish', 'age': 1, 'gender': 'unknown', 'weight': 0.2,
         'description': 'Elegant angelfish with distinctive triangular shape. Requires larger tank. Very peaceful and beautiful.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 800.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
        {'name': 'Tetra', 'breed': 'Neon Tetra', 'age': 0, 'gender': 'unknown', 'weight': 0.01,
         'description': 'Bright neon tetra with stunning colors. Schooling fish - best kept in groups. Very peaceful.', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 150.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1594736797933-d0e4a440365b?w=800'},
        {'name': 'Betta', 'breed': 'Betta Fish', 'age': 1, 'gender': 'male', 'weight': 0.02,
         'description': 'Beautiful betta fish with flowing fins. Can be kept alone. Very colorful and easy to care for.', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 300.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c93a?w=800'},
        {'name': 'Sword', 'breed': 'Swordtail', 'age': 1, 'gender': 'male', 'weight': 0.1,
         'description': 'Active swordtail fish with distinctive tail extension. Great for community tanks. Easy to breed.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 250.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
        {'name': 'Cichlid', 'breed': 'African Cichlid', 'age': 2, 'gender': 'unknown', 'weight': 0.3,
         'description': 'Colorful African cichlid. Requires specific water conditions. Very active and interesting behavior.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 1200.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1594736797933-d0e4a440365b?w=800'},
        {'name': 'Discus', 'breed': 'Discus Fish', 'age': 2, 'gender': 'unknown', 'weight': 0.4,
         'description': 'Beautiful discus fish with round body shape. Requires experienced keeper. Very peaceful and colorful.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 2000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c93a?w=800'},
        {'name': 'Koi', 'breed': 'Koi Carp', 'age': 3, 'gender': 'unknown', 'weight': 2.0,
         'description': 'Stunning koi carp with beautiful patterns. Requires large pond. Very long-lived and elegant.', 
         'location': 'Surat, Gujarat', 'adoption_fee': 3000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
    ],
    'other': [
        {'name': 'Spike', 'breed': 'Hedgehog', 'age': 1, 'gender': 'male', 'weight': 0.5,
         'description': 'Cute and prickly hedgehog. Very unique pet. Nocturnal and requires special care. Very adorable!', 
         'location': 'Mumbai, Maharashtra', 'adoption_fee': 5000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800'},
        {'name': 'Hammy', 'breed': 'Hamster', 'age': 0, 'gender': 'male', 'weight': 0.1,
         'description': 'Tiny and adorable hamster. Perfect for kids. Very active at night and loves running on wheel.', 
         'location': 'Delhi, NCR', 'adoption_fee': 800.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800'},
        {'name': 'Guinea', 'breed': 'Guinea Pig', 'age': 1, 'gender': 'female', 'weight': 0.8,
         'description': 'Friendly guinea pig. Very social and loves company. Perfect for children and first-time pet owners.', 
         'location': 'Bangalore, Karnataka', 'adoption_fee': 1500.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'},
        {'name': 'Tortoise', 'breed': 'Tortoise', 'age': 5, 'gender': 'male', 'weight': 3.0,
         'description': 'Gentle tortoise. Very long-lived and easy to care for. Requires outdoor space and proper habitat.', 
         'location': 'Pune, Maharashtra', 'adoption_fee': 4000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c93a?w=800'},
        {'name': 'Chinny', 'breed': 'Chinchilla', 'age': 2, 'gender': 'female', 'weight': 0.6,
         'description': 'Soft and fluffy chinchilla. Very active and playful. Requires dust baths. Very cute and unique!', 
         'location': 'Hyderabad, Telangana', 'adoption_fee': 6000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800'},
        {'name': 'Gerbil', 'breed': 'Gerbil', 'age': 0, 'gender': 'male', 'weight': 0.08,
         'description': 'Small and active gerbil. Very social and should be kept in pairs. Great for watching and interacting.', 
         'location': 'Chennai, Tamil Nadu', 'adoption_fee': 600.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800'},
        {'name': 'Ferret', 'breed': 'Ferret', 'age': 1, 'gender': 'male', 'weight': 1.5,
         'description': 'Playful and curious ferret. Very intelligent and active. Requires lots of interaction and playtime.', 
         'location': 'Kolkata, West Bengal', 'adoption_fee': 8000.00, 'vaccination_status': True, 'is_spayed_neutered': True,
         'image_url': 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800'},
        {'name': 'Lizard', 'breed': 'Bearded Dragon', 'age': 2, 'gender': 'male', 'weight': 0.5,
         'description': 'Docile bearded dragon lizard. Very friendly and easy to handle. Great reptile pet for beginners.', 
         'location': 'Ahmedabad, Gujarat', 'adoption_fee': 5000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800'},
        {'name': 'Snake', 'breed': 'Ball Python', 'age': 3, 'gender': 'female', 'weight': 2.0,
         'description': 'Gentle ball python. Very calm and easy to handle. Perfect for reptile enthusiasts. Very docile.', 
         'location': 'Jaipur, Rajasthan', 'adoption_fee': 7000.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800'},
        {'name': 'Ratty', 'breed': 'Rat', 'age': 1, 'gender': 'female', 'weight': 0.3,
         'description': 'Intelligent and friendly rat. Very social and trainable. Great pet for older children and adults.', 
         'location': 'Surat, Gujarat', 'adoption_fee': 400.00, 'vaccination_status': False, 'is_spayed_neutered': False,
         'image_url': 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800'},
    ],
}

def download_image(url, pet_name):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content)
    except Exception as e:
        print(f"  [WARNING] Could not download image for {pet_name}: {str(e)}")
    return None

def add_sample_pets():
    """Add all sample pets to the database"""
    # Get admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create a superuser first.")
        return
    
    total_pets = sum(len(pets) for pets in PET_DATA.values())
    print("=" * 60)
    print(f"Adding {total_pets} Sample Pets to Database")
    print("=" * 60)
    print()
    
    added_count = 0
    skipped_count = 0
    
    for pet_type, pets_list in PET_DATA.items():
        print(f"Adding {pet_type.upper()}S ({len(pets_list)} pets)...")
        print("-" * 60)
        
        for pet_data in pets_list:
            pet_name = pet_data['name']
            
            # Check if pet already exists
            if Pet.objects.filter(name=pet_name, pet_type=pet_type).exists():
                print(f"  [SKIP] Skipping {pet_name} - already exists")
                skipped_count += 1
                continue
            
            try:
                # Create pet
                pet = Pet.objects.create(
                    name=pet_name,
                    pet_type=pet_type,
                    breed=pet_data['breed'],
                    age=pet_data['age'],
                    gender=pet_data['gender'],
                    weight=pet_data.get('weight'),
                    description=pet_data['description'],
                    location=pet_data['location'],
                    adoption_fee=pet_data['adoption_fee'],
                    vaccination_status=pet_data['vaccination_status'],
                    is_spayed_neutered=pet_data['is_spayed_neutered'],
                    status='available',
                    created_by=admin_user
                )
                
                # Download and add image
                print(f"  Adding {pet_name}...", end=' ')
                image_file = download_image(pet_data['image_url'], pet_name)
                
                if image_file:
                    filename = f"{pet_name.lower().replace(' ', '_')}_{pet_type}.jpg"
                    pet.image.save(filename, image_file, save=True)
                    print("[OK - with image]")
                else:
                    print("[OK - no image]")
                
                added_count += 1
                
            except Exception as e:
                print(f"  [ERROR] Error adding {pet_name}: {str(e)}")
                skipped_count += 1
        
        print()
    
    print("=" * 60)
    print(f"[SUCCESS] Added: {added_count} pets")
    print(f"[INFO] Skipped: {skipped_count} pets")
    print("=" * 60)
    print("\nSample pets added successfully!")
    print(f"Visit http://localhost:8000/pets/ to see all pets")

if __name__ == "__main__":
    add_sample_pets()

