"""
Script to create 3 sample order histories with payments
"""
import os
import django
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption_project.settings')
django.setup()

from users.models import User
from accessories.models import Accessory
from orders.models import Order, OrderItem
from payments.models import Payment

def create_order_history():
    """Create 3 sample orders with complete history"""
    print("=" * 60)
    print("Creating 3 Sample Order Histories")
    print("=" * 60)
    print()
    
    # Get admin user or create a test user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found.")
        return
    
    # Get some accessories
    accessories = Accessory.objects.filter(is_active=True, stock_quantity__gt=0)[:10]
    if accessories.count() < 3:
        print("Error: Not enough accessories in database. Please add accessories first.")
        return
    
    orders_data = [
        {
            'items': [
                {'accessory': accessories[0], 'quantity': 2},
                {'accessory': accessories[1], 'quantity': 1},
                {'accessory': accessories[2], 'quantity': 3},
            ],
            'shipping': {
                'name': 'John Doe',
                'phone': '+919876543210',
                'address': '123 Main Street, Apartment 4B',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'zip_code': '400001',
            },
            'status': 'delivered',
            'payment_status': 'paid',
            'created_days_ago': 15,
        },
        {
            'items': [
                {'accessory': accessories[3], 'quantity': 1},
                {'accessory': accessories[4], 'quantity': 2},
            ],
            'shipping': {
                'name': 'Jane Smith',
                'phone': '+919123456789',
                'address': '456 Park Avenue',
                'city': 'Delhi',
                'state': 'Delhi',
                'zip_code': '110001',
            },
            'status': 'shipped',
            'payment_status': 'paid',
            'created_days_ago': 5,
        },
        {
            'items': [
                {'accessory': accessories[5], 'quantity': 1},
                {'accessory': accessories[6], 'quantity': 1},
                {'accessory': accessories[7], 'quantity': 1},
            ],
            'shipping': {
                'name': 'Robert Johnson',
                'phone': '+919988776655',
                'address': '789 Oak Street',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'zip_code': '560001',
            },
            'status': 'processing',
            'payment_status': 'paid',
            'created_days_ago': 2,
        },
    ]
    
    created_orders = []
    
    for idx, order_data in enumerate(orders_data, 1):
        print(f"\nCreating Order #{idx}...")
        print("-" * 60)
        
        # Calculate totals
        subtotal = Decimal('0.00')
        for item_data in order_data['items']:
            item_total = item_data['accessory'].price * item_data['quantity']
            subtotal += item_total
        
        shipping_cost = Decimal('100.00')
        tax = subtotal * Decimal('0.18')  # 18% GST
        total_amount = subtotal + shipping_cost + tax
        
        # Create order
        created_date = timezone.now() - timedelta(days=order_data['created_days_ago'])
        
        order = Order.objects.create(
            user=admin_user,
            shipping_name=order_data['shipping']['name'],
            shipping_phone=order_data['shipping']['phone'],
            shipping_address=order_data['shipping']['address'],
            shipping_city=order_data['shipping']['city'],
            shipping_state=order_data['shipping']['state'],
            shipping_zip_code=order_data['shipping']['zip_code'],
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total_amount=total_amount,
            status=order_data['status'],
            payment_status=order_data['payment_status'],
            created_at=created_date,
        )
        
        print(f"  Order Number: {order.order_number}")
        print(f"  Total Amount: Rs.{total_amount}")
        print(f"  Status: {order.get_status_display()}")
        
        # Create order items
        for item_data in order_data['items']:
            accessory = item_data['accessory']
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                accessory=accessory,
                quantity=quantity,
                price_at_purchase=accessory.price,
                subtotal=accessory.price * quantity,
            )
            
            # Update stock (don't actually reduce, just for demo)
            # accessory.stock_quantity -= quantity
            # accessory.save()
            
            print(f"  - {accessory.name} x{quantity} = Rs.{accessory.price * quantity}")
        
        # Create payment
        payment_date = created_date + timedelta(hours=1)
        
        payment = Payment.objects.create(
            order=order,
            user=admin_user,
            payment_method='razorpay',
            status='success',
            amount=total_amount,
            currency='INR',
            razorpay_order_id=f'order_test_{order.order_number}',
            razorpay_payment_id=f'pay_test_{order.order_number}',
            razorpay_signature=f'sig_test_{order.order_number}',
            transaction_id=f'TXN{order.order_number}',
            payment_date=payment_date,
            created_at=created_date,
        )
        
        print(f"  Payment: Rs.{total_amount} - {payment.get_status_display()}")
        
        created_orders.append(order)
    
    print()
    print("=" * 60)
    print(f"[SUCCESS] Created {len(created_orders)} orders with payments")
    print("=" * 60)
    print("\nOrder History:")
    for order in created_orders:
        print(f"  - Order #{order.order_number}: Rs.{order.total_amount} ({order.get_status_display()})")
    print(f"\nVisit http://localhost:8000/orders/ to see order history")

if __name__ == "__main__":
    create_order_history()

