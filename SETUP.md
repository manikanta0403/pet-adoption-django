# Setup Guide - Pet Adoption & Accessories Management System

## Quick Start Guide

### Step 1: Install Dependencies
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your configuration:
   - `SECRET_KEY`: Generate a new secret key or use the default
   - `DEBUG=True` for development
   - Add Razorpay keys if you want payment functionality

### Step 3: Setup Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### Step 4: Run Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your application!

## Creating Sample Data

### Option 1: Use Admin Panel
1. Login to admin panel: `http://localhost:8000/admin/`
2. Add pets, categories, and accessories manually

### Option 2: Use Django Shell
```bash
python manage.py shell
```

```python
from users.models import User
from pets.models import Pet
from accessories.models import Category, Accessory

# Create categories
category1 = Category.objects.create(name="Food & Treats", description="Pet food and treats")
category2 = Category.objects.create(name="Toys", description="Pet toys and accessories")
category3 = Category.objects.create(name="Grooming", description="Grooming supplies")

# Create accessories
Accessory.objects.create(
    name="Premium Dog Food",
    category=category1,
    description="High-quality dog food",
    price=1500.00,
    stock_quantity=50,
    is_active=True
)

# Create pets (you'll need a user first)
user = User.objects.first()
if user:
    Pet.objects.create(
        name="Buddy",
        pet_type="dog",
        breed="Golden Retriever",
        age=2,
        gender="male",
        description="Friendly and playful dog",
        vaccination_status=True,
        location="Mumbai",
        created_by=user
    )
```

## Admin Dashboard Access

1. Create superuser if you haven't:
   ```bash
   python manage.py createsuperuser
   ```

2. Login at: `http://localhost:8000/admin/`

3. Default admin features:
   - Manage all pets
   - Manage accessories and categories
   - View and manage orders
   - Manage adoption requests
   - View payments
   - Manage users

## Testing Payment Integration

### Test Mode Setup
1. Get Razorpay test keys from: https://razorpay.com/docs/payments/payments/test-card-details/
2. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=your_test_key_id
   RAZORPAY_KEY_SECRET=your_test_key_secret
   ```

### Test Cards
- Success: 4111 1111 1111 1111
- Failure: Any other card number

## Common Issues & Solutions

### Issue: Database locked
**Solution**: Make sure no other process is using the database. Restart the server.

### Issue: Static files not loading
**Solution**: 
```bash
python manage.py collectstatic --noinput
```

### Issue: Migration errors
**Solution**: 
```bash
python manage.py migrate --run-syncdb
```

### Issue: Module not found
**Solution**: Make sure virtual environment is activated and all packages are installed.

## Production Deployment

### Before deploying:
1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up proper static file serving
5. Configure media file storage (AWS S3 recommended)
6. Set up SSL/HTTPS
7. Use production Razorpay keys

### Heroku Deployment
```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Render Deployment
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy!

## Need Help?

- Check the main README.md
- Review Django documentation: https://docs.djangoproject.com/
- Check Razorpay documentation: https://razorpay.com/docs/

