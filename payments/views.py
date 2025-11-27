import razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from orders.models import Order
from .models import Payment


# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def initiate_payment(request, order_id):
    """Initiate payment for an order"""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Check if payment already exists
    if hasattr(order, 'payment'):
        payment = order.payment
        if payment.status == 'success':
            messages.info(request, 'This order has already been paid.')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_amount,
            status='pending'
        )
    
    # Create Razorpay order
    if not payment.razorpay_order_id:
        try:
            razorpay_order = client.order.create({
                'amount': int(order.total_amount * 100),  # Convert to paise
                'currency': 'INR',
                'receipt': order.order_number,
            })
            payment.razorpay_order_id = razorpay_order['id']
            payment.save()
        except Exception as e:
            messages.error(request, f'Error creating payment: {str(e)}')
            return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': int(order.total_amount * 100),
    }
    return render(request, 'payments/payment.html', context)


@csrf_exempt
def payment_success(request):
    """Handle successful payment callback"""
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                messages.error(request, 'Payment verification failed.')
                return redirect('orders:order_list')
            
            # Update payment
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'success'
            payment.payment_status = 'paid'
            payment.payment_date = timezone.now()
            payment.save()
            
            # Update order payment status
            order = payment.order
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
            messages.success(request, 'Payment successful! Your order has been confirmed.')
            return redirect('orders:order_detail', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
            return redirect('orders:order_list')
    
    return redirect('orders:order_list')


@csrf_exempt
def payment_failed(request):
    """Handle failed payment callback"""
    if request.method == 'POST':
        try:
            razorpay_order_id = request.POST.get('razorpay_order_id')
            error_description = request.POST.get('error[description]', 'Payment failed')
            
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.status = 'failed'
            payment.failure_reason = error_description
            payment.save()
            
            messages.error(request, f'Payment failed: {error_description}')
        except Exception as e:
            messages.error(request, 'Error processing payment failure.')
    
    return redirect('orders:order_list')


@login_required
def payment_history(request):
    """View payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/payment_history.html', {'payments': payments})
