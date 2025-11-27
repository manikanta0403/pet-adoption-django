from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Category, Accessory, Cart


def accessory_list(request):
    """List all accessories with search and filter"""
    accessories = Accessory.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        accessories = accessories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        accessories = accessories.filter(category__slug=category_slug)
    
    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        accessories = accessories.filter(price__gte=Decimal(min_price))
    if max_price:
        accessories = accessories.filter(price__lte=Decimal(max_price))
    
    # Sort
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        accessories = accessories.order_by('price')
    elif sort_by == 'price_high':
        accessories = accessories.order_by('-price')
    elif sort_by == 'name':
        accessories = accessories.order_by('name')
    else:
        accessories = accessories.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(accessories, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'accessories/accessory_list.html', context)


def accessory_detail(request, slug):
    """Accessory detail view"""
    accessory = get_object_or_404(Accessory, slug=slug, is_active=True)
    in_cart = False
    cart_quantity = 0
    
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(user=request.user, accessory=accessory)
            in_cart = True
            cart_quantity = cart_item.quantity
        except Cart.DoesNotExist:
            pass
    
    context = {
        'accessory': accessory,
        'in_cart': in_cart,
        'cart_quantity': cart_quantity,
    }
    return render(request, 'accessories/accessory_detail.html', context)


@login_required
def add_to_cart(request, accessory_id):
    """Add accessory to cart"""
    accessory = get_object_or_404(Accessory, pk=accessory_id, is_active=True)
    
    if not accessory.in_stock:
        messages.error(request, 'This item is out of stock.')
        return redirect('accessory_detail', slug=accessory.slug)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > accessory.stock_quantity:
        messages.error(request, f'Only {accessory.stock_quantity} items available in stock.')
        return redirect('accessory_detail', slug=accessory.slug)
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        accessory=accessory,
        defaults={'quantity': quantity}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > accessory.stock_quantity:
            messages.error(request, f'Cannot add more. Only {accessory.stock_quantity} items available in stock.')
            return redirect('view_cart')
        cart_item.quantity = new_quantity
        cart_item.save()
    
    messages.success(request, f'{accessory.name} added to cart!')
    return redirect('view_cart')


@login_required
def view_cart(request):
    """View shopping cart"""
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'accessories/cart.html', context)


@login_required
def update_cart(request, cart_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > cart_item.accessory.stock_quantity:
            messages.error(request, f'Only {cart_item.accessory.stock_quantity} items available in stock.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
    
    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')
