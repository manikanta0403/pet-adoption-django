"""
Script to add 50 pet accessories to the database
"""
import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption_project.settings')
django.setup()

from accessories.models import Category, Accessory

# Accessories data - 50 items across different categories
ACCESSORIES_DATA = [
    # Food & Treats (15 items)
    {'name': 'Premium Dog Food - Chicken & Rice', 'category': 'Food & Treats', 'description': 'High-quality dry dog food made with real chicken and brown rice. Rich in protein and essential nutrients. 5kg pack.', 'price': 1200.00, 'stock': 50, 'brand': 'PetCare Pro', 'image_url': 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=800'},
    {'name': 'Grain-Free Cat Food - Salmon', 'category': 'Food & Treats', 'description': 'Premium grain-free cat food with fresh salmon. Perfect for cats with sensitive stomachs. 3kg pack.', 'price': 1500.00, 'stock': 45, 'brand': 'Natural Pet', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog Treats - Training Bites', 'category': 'Food & Treats', 'description': 'Small, soft training treats perfect for reward-based training. Made with natural ingredients. 500g pack.', 'price': 450.00, 'stock': 80, 'brand': 'TrainRight', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Treats - Tuna Flavor', 'category': 'Food & Treats', 'description': 'Irresistible tuna-flavored treats that cats love. Great for bonding and training. 200g pack.', 'price': 350.00, 'stock': 75, 'brand': 'Kitty Delight', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Bird Seed Mix - Premium Blend', 'category': 'Food & Treats', 'description': 'Nutritious seed mix for all types of birds. Contains sunflower seeds, millet, and more. 1kg pack.', 'price': 300.00, 'stock': 60, 'brand': 'Avian Nutrition', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Rabbit Pellets - Complete Nutrition', 'category': 'Food & Treats', 'description': 'Complete nutrition pellets for rabbits. Balanced diet with all essential vitamins and minerals. 2kg pack.', 'price': 400.00, 'stock': 55, 'brand': 'Bunny Care', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Fish Food Flakes - Tropical', 'category': 'Food & Treats', 'description': 'Premium tropical fish food flakes. Suitable for all tropical fish. Enhances color and vitality. 200g pack.', 'price': 250.00, 'stock': 100, 'brand': 'AquaLife', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Puppy Food - Lamb & Vegetables', 'category': 'Food & Treats', 'description': 'Specially formulated for puppies. Rich in DHA for brain development. Easy to digest. 4kg pack.', 'price': 1800.00, 'stock': 40, 'brand': 'Puppy Prime', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Kitten Food - Chicken & Milk', 'category': 'Food & Treats', 'description': 'Complete nutrition for kittens. High protein content for healthy growth. Contains milk proteins. 2kg pack.', 'price': 1300.00, 'stock': 42, 'brand': 'Kitten Care', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog Dental Chews', 'category': 'Food & Treats', 'description': 'Promotes healthy teeth and gums. Reduces tartar and bad breath. Long-lasting chew treat. Pack of 10.', 'price': 550.00, 'stock': 65, 'brand': 'DentalCare', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Freeze-Dried Dog Treats', 'category': 'Food & Treats', 'description': 'Single-ingredient freeze-dried treats. 100% natural chicken. No preservatives. 100g pack.', 'price': 650.00, 'stock': 58, 'brand': 'Natural Treats', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Wet Food - Chicken & Liver', 'category': 'Food & Treats', 'description': 'Delicious wet food with real chicken and liver. High moisture content. Pack of 12 cans (400g each).', 'price': 750.00, 'stock': 70, 'brand': 'Kitty Gourmet', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Hamster Food Mix', 'category': 'Food & Treats', 'description': 'Complete nutrition mix for hamsters. Contains seeds, grains, and dried fruits. 500g pack.', 'price': 280.00, 'stock': 85, 'brand': 'Hamster Happy', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Bird Treat Sticks', 'category': 'Food & Treats', 'description': 'Honey-coated seed sticks for birds. Great for mental stimulation. Pack of 5 sticks.', 'price': 200.00, 'stock': 90, 'brand': 'Bird Treats Co', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Senior Dog Food - Joint Care', 'category': 'Food & Treats', 'description': 'Specialized food for senior dogs with joint support. Contains glucosamine and chondroitin. 5kg pack.', 'price': 2000.00, 'stock': 35, 'brand': 'Senior Care', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    
    # Toys (15 items)
    {'name': 'Interactive Dog Puzzle Toy', 'category': 'Toys', 'description': 'Mental stimulation puzzle toy for dogs. Hide treats inside for hours of fun. Durable plastic construction.', 'price': 850.00, 'stock': 40, 'brand': 'PuzzlePlay', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Cat Scratching Post - 3 Levels', 'category': 'Toys', 'description': 'Multi-level scratching post with hanging toys. Saves furniture from scratches. Sisal rope wrapped. 120cm height.', 'price': 2500.00, 'stock': 30, 'brand': 'CatTree Pro', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Dog Tennis Ball - Pack of 3', 'category': 'Toys', 'description': 'Standard size tennis balls for fetch. Bright yellow for visibility. Non-abrasive surface. Pack of 3.', 'price': 200.00, 'stock': 150, 'brand': 'Fetch Master', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Catnip Mouse Toys - Set of 5', 'category': 'Toys', 'description': 'Catnip-filled mouse toys that cats love. Colorful fabric design. Great for play and exercise. Set of 5.', 'price': 450.00, 'stock': 80, 'brand': 'Kitty Play', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Kong Classic Dog Toy', 'category': 'Toys', 'description': 'Durable rubber toy that bounces unpredictably. Can be stuffed with treats. Perfect for chewing. Red color.', 'price': 750.00, 'stock': 55, 'brand': 'Kong', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Feather Wand Cat Toy', 'category': 'Toys', 'description': 'Interactive wand toy with colorful feathers. Great for bonding with your cat. Extendable handle.', 'price': 350.00, 'stock': 70, 'brand': 'Feather Fun', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Dog Rope Tug Toy', 'category': 'Toys', 'description': 'Braided rope toy for tug-of-war. Helps clean teeth naturally. 30cm length. Safe for all sizes.', 'price': 380.00, 'stock': 60, 'brand': 'TugMaster', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Bird Mirror Toy', 'category': 'Toys', 'description': 'Safe mirror toy for birds. Provides entertainment and companionship. Easy to attach to cage. 10cm diameter.', 'price': 250.00, 'stock': 95, 'brand': 'Avian Play', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Rabbit Chew Toys - Wood Set', 'category': 'Toys', 'description': 'Natural wood chew toys for rabbits. Promotes dental health. Set of 3 different shapes. 100% safe.', 'price': 320.00, 'stock': 75, 'brand': 'Bunny Chews', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Dog Frisbee - Flying Disc', 'category': 'Toys', 'description': 'Professional-grade flying disc for dogs. Soft and flexible. Floats on water. 23cm diameter.', 'price': 450.00, 'stock': 50, 'brand': 'FlyHigh', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Laser Pointer for Cats', 'category': 'Toys', 'description': 'Red laser pointer for interactive play with cats. Promotes exercise and mental stimulation. Battery included.', 'price': 280.00, 'stock': 85, 'brand': 'Laser Play', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Plush Dog Toy - Squeaky', 'category': 'Toys', 'description': 'Soft plush toy with squeaker inside. Machine washable. Perfect for cuddling and play. 25cm size.', 'price': 550.00, 'stock': 65, 'brand': 'Plush Pets', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Hamster Exercise Wheel', 'category': 'Toys', 'description': 'Silent exercise wheel for hamsters. Prevents boredom and promotes health. Easy to clean. 20cm diameter.', 'price': 420.00, 'stock': 88, 'brand': 'Hamster Fitness', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Dog Pull Rope - Tug of War', 'category': 'Toys', 'description': 'Heavy-duty rope toy for tug games. Reinforced ends. Suitable for medium to large dogs. 45cm length.', 'price': 480.00, 'stock': 58, 'brand': 'Strong Rope', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    {'name': 'Bird Swing - Natural Wood', 'category': 'Toys', 'description': 'Natural wood swing for bird cages. Provides exercise and entertainment. Easy to install. 15cm width.', 'price': 180.00, 'stock': 100, 'brand': 'Avian Comfort', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800'},
    
    # Grooming (10 items)
    {'name': 'Dog Grooming Brush - Slicker', 'category': 'Grooming', 'description': 'Professional slicker brush for dogs. Removes tangles and loose fur. Gentle on skin. Medium size.', 'price': 450.00, 'stock': 60, 'brand': 'Groom Pro', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Grooming Glove', 'category': 'Grooming', 'description': 'Massage grooming glove for cats. Removes loose hair while petting. Washable and comfortable.', 'price': 380.00, 'stock': 75, 'brand': 'GloveGroom', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Pet Shampoo - Oatmeal', 'category': 'Grooming', 'description': 'Gentle oatmeal shampoo for dogs and cats. Soothes sensitive skin. pH balanced. 500ml bottle.', 'price': 550.00, 'stock': 70, 'brand': 'Gentle Care', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog Nail Clipper - Professional', 'category': 'Grooming', 'description': 'Professional nail clipper with safety guard. Suitable for all dog sizes. Stainless steel blades.', 'price': 350.00, 'stock': 80, 'brand': 'ClipSafe', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Pet Hair Remover - Lint Roller', 'category': 'Grooming', 'description': 'Reusable lint roller for pet hair removal from clothes and furniture. Washable sticky sheets.', 'price': 250.00, 'stock': 90, 'brand': 'Hair Away', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog Toothbrush & Toothpaste Set', 'category': 'Grooming', 'description': 'Complete dental care set for dogs. Includes brush and chicken-flavored toothpaste. Promotes oral health.', 'price': 420.00, 'stock': 65, 'brand': 'Dental Care', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Deshedding Tool', 'category': 'Grooming', 'description': 'Professional deshedding tool for cats. Reduces shedding by up to 90%. Stainless steel blades.', 'price': 680.00, 'stock': 55, 'brand': 'DeShed Pro', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Pet Wipes - Hypoallergenic', 'category': 'Grooming', 'description': 'Gentle cleaning wipes for pets. Hypoallergenic and alcohol-free. Pack of 100 wipes.', 'price': 380.00, 'stock': 85, 'brand': 'CleanWipes', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog Grooming Scissors - Curved', 'category': 'Grooming', 'description': 'Professional curved grooming scissors. Sharp stainless steel. Perfect for trimming around face and paws.', 'price': 850.00, 'stock': 45, 'brand': 'GroomMaster', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Pet Hair Dryer', 'category': 'Grooming', 'description': 'Low-noise pet hair dryer. Adjustable temperature and speed. Perfect for post-bath drying. 1600W power.', 'price': 3500.00, 'stock': 25, 'brand': 'DryPro', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    
    # Accessories & Care (10 items)
    {'name': 'Dog Leash - Retractable', 'category': 'Accessories', 'description': 'Heavy-duty retractable leash for dogs. Extends up to 5 meters. One-button brake system. Suitable for medium dogs.', 'price': 650.00, 'stock': 50, 'brand': 'FlexiLeash', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Collar - Breakaway', 'category': 'Accessories', 'description': 'Safe breakaway collar for cats. Releases if caught. Includes bell and ID tag. Adjustable sizing.', 'price': 280.00, 'stock': 95, 'brand': 'SafeCollar', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Dog Bowl - Stainless Steel Set', 'category': 'Accessories', 'description': 'Durable stainless steel bowls for food and water. Non-slip base. Easy to clean. Set of 2 bowls (1L each).', 'price': 550.00, 'stock': 70, 'brand': 'SteelBowl', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Pet Bed - Orthopedic', 'category': 'Accessories', 'description': 'Comfortable orthopedic pet bed. Supports joints and provides comfort. Washable cover. Medium size (70cm).', 'price': 2500.00, 'stock': 35, 'brand': 'Comfort Bed', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Cat Litter Box - Covered', 'category': 'Accessories', 'description': 'Privacy-covered litter box for cats. Includes filter to reduce odors. Easy to clean. Large size.', 'price': 1800.00, 'stock': 40, 'brand': 'LitterPro', 'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800'},
    {'name': 'Dog Harness - No Pull', 'category': 'Accessories', 'description': 'No-pull harness for dogs. Reduces pulling during walks. Padded chest and belly straps. Adjustable sizing.', 'price': 850.00, 'stock': 55, 'brand': 'WalkEasy', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Bird Cage - Large', 'category': 'Accessories', 'description': 'Spacious bird cage with perches and toys. Includes food and water dishes. 60cm x 40cm x 50cm.', 'price': 4500.00, 'stock': 20, 'brand': 'Avian Home', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Pet Carrier - Airline Approved', 'category': 'Accessories', 'description': 'Airline-approved pet carrier. Ventilated sides and top. Secure latches. Suitable for small dogs and cats.', 'price': 2200.00, 'stock': 30, 'brand': 'TravelSafe', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Dog ID Tag - Engraved', 'category': 'Accessories', 'description': 'Durable stainless steel ID tag. Can be engraved with pet name and contact info. Hangs from collar.', 'price': 200.00, 'stock': 120, 'brand': 'ID Tag Pro', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
    {'name': 'Pet First Aid Kit', 'category': 'Accessories', 'description': 'Comprehensive first aid kit for pets. Includes bandages, antiseptic, tweezers, and more. Essential for emergencies.', 'price': 1200.00, 'stock': 45, 'brand': 'Pet First Aid', 'image_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800'},
]

def download_image(url, product_name):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content)
    except Exception as e:
        print(f"  [WARNING] Could not download image for {product_name}")
    return None

def add_accessories():
    """Add all accessories to the database"""
    print("=" * 60)
    print("Adding 50 Pet Accessories to Database")
    print("=" * 60)
    print()
    
    # Create categories first
    categories = {}
    for item in ACCESSORIES_DATA:
        cat_name = item['category']
        if cat_name not in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = category
            if created:
                print(f"Created category: {cat_name}")
    
    print()
    added_count = 0
    skipped_count = 0
    
    for item in ACCESSORIES_DATA:
        name = item['name']
        
        # Check if accessory already exists
        if Accessory.objects.filter(name=name).exists():
            print(f"  [SKIP] Skipping {name} - already exists")
            skipped_count += 1
            continue
        
        try:
            category = categories[item['category']]
            
            # Create accessory
            accessory = Accessory.objects.create(
                name=name,
                category=category,
                description=item['description'],
                price=item['price'],
                stock_quantity=item['stock'],
                brand=item.get('brand', ''),
                is_featured=False,
                is_active=True
            )
            
            # Download and add image
            print(f"  Adding {name[:40]}...", end=' ')
            image_file = download_image(item.get('image_url', ''), name)
            
            if image_file:
                filename = f"{name.lower().replace(' ', '_').replace('-', '_')[:50]}.jpg"
                accessory.image.save(filename, image_file, save=True)
                print("[OK - with image]")
            else:
                print("[OK - no image]")
            
            added_count += 1
            
        except Exception as e:
            print(f"  [ERROR] Error adding {name}: {str(e)}")
            skipped_count += 1
    
    print()
    print("=" * 60)
    print(f"[SUCCESS] Added: {added_count} accessories")
    print(f"[INFO] Skipped: {skipped_count} accessories")
    print("=" * 60)
    print("\nAccessories added successfully!")
    print(f"Visit http://localhost:8000/accessories/ to see all accessories")

if __name__ == "__main__":
    add_accessories()

