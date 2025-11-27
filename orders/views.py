from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from accessories.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """Checkout view"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('accessories:accessory_list')
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.accessory.stock_quantity:
            messages.error(request, f'{item.accessory.name} has insufficient stock.')
            return redirect('accessories:view_cart')
    
    subtotal = sum(item.total_price for item in cart_items)
    shipping_cost = Decimal('100.00')  # Fixed shipping cost
    tax = subtotal * Decimal('0.18')  # 18% GST
    total_amount = subtotal + shipping_cost + tax
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = Order.objects.create(
                        user=request.user,
                        shipping_name=form.cleaned_data['shipping_name'],
                        shipping_phone=form.cleaned_data['shipping_phone'],
                        shipping_address=form.cleaned_data['shipping_address'],
                        shipping_city=form.cleaned_data['shipping_city'],
                        shipping_state=form.cleaned_data['shipping_state'],
                        shipping_zip_code=form.cleaned_data['shipping_zip_code'],
                        subtotal=subtotal,
                        shipping_cost=shipping_cost,
                        tax=tax,
                        total_amount=total_amount,
                    )
                    
                    # Create order items and update stock
                    for cart_item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            accessory=cart_item.accessory,
                            quantity=cart_item.quantity,
                            price_at_purchase=cart_item.accessory.price,
                            subtotal=cart_item.total_price,
                        )
                        # Update stock
                        cart_item.accessory.stock_quantity -= cart_item.quantity
                        cart_item.accessory.save()
                    
                    # Clear cart
                    cart_items.delete()
                    
                    messages.success(request, 'Order placed successfully!')
                    return redirect('orders:order_detail', order_id=order.id)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # Pre-fill form with user data
        initial_data = {
            'shipping_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'shipping_phone': request.user.phone_number,
            'shipping_address': request.user.address,
            'shipping_city': request.user.city,
            'shipping_state': request.user.state,
            'shipping_zip_code': request.user.zip_code,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total_amount': total_amount,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    """View user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """View order detail"""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
