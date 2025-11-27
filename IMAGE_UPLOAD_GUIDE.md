# Image Upload Guide

## How to Add Pet Images

### Method 1: Via Admin Panel (Recommended)

1. **Prepare your images:**
   - Image formats: JPG, PNG, GIF, WebP
   - Recommended size: 800x600 pixels or larger
   - File size: Keep under 5MB for best performance

2. **Upload through Admin:**
   - Go to: http://localhost:8000/admin/pets/pet/add/
   - Fill in all pet details
   - In the "Image" field, click "Choose File" and select your pet image
   - Click "Save"

3. **Or Edit Existing Pet:**
   - Go to: http://localhost:8000/admin/pets/pet/
   - Click on the pet you want to edit
   - Scroll to "Images" section
   - Click "Choose File" next to "Image"
   - Select your image
   - Click "Save"

### Method 2: Direct File Upload

1. **Copy image files to media folder:**
   ```
   pet-adoption-django/
   └── media/
       └── pet_images/
           ├── leo.jpg
           ├── max.jpg
           └── ...
   ```

2. **Then add/edit pet via admin:**
   - The image files will be accessible once uploaded through admin panel

### Method 3: Programmatic Addition

Use the `add_pet_data.py` script:

```python
from add_pet_data import add_pet

add_pet(
    name="Max",
    pet_type="dog",
    breed="Golden Retriever",
    age=2,
    gender="male",
    description="Very friendly and well-trained dog.",
    location="Mumbai",
    adoption_fee=5000.00,
    vaccination_status=True,
    is_spayed_neutered=True,
    weight=25.5,
    image_path="path/to/image.jpg"  # Optional
)
```

## Image Storage

- **Development:** Images are stored in `media/pet_images/` folder
- **Production:** Configure AWS S3 or similar cloud storage

## Troubleshooting

### Images not showing?
1. Check that `MEDIA_URL` and `MEDIA_ROOT` are set correctly in `settings.py`
2. Ensure the Django development server is running
3. Clear browser cache
4. Check file permissions on the media folder

### Upload fails?
1. Check file size (should be under 5MB)
2. Verify file format (JPG, PNG, GIF, WebP)
3. Check Django logs for error messages
4. Ensure `media/pet_images/` folder exists and is writable

## Current Pet Image Status

The "Leo" pet was added without an image. To add an image:

1. Take a photo of the pet or find a stock image
2. Save it as `leo.jpg` or `leo.png`
3. Go to admin panel → Pets → Leo → Edit
4. Upload the image in the "Image" field
5. Save

The image will then display on the homepage and pet detail pages!

