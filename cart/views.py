from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Get or create cart for user/session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart


def cart_view(request):
    """Display shopping cart"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    cart_total = sum(item.get_total_price() for item in cart_items) or 0
    total_items = sum(item.quantity for item in cart_items)
    cart_total_float = float(cart_total)
    tax_total = 0  # No tax
    order_total = round(cart_total_float + 20, 2)  # Add 20 TK shipping
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': f'{cart_total_float:.2f}',
        'tax_total': f'{tax_total:.2f}',
        'order_total': f'{order_total:.2f}',
        'total_items': total_items,
    }
    return render(request, 'cart/cart.html', context)


@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Handle removal if quantity becomes zero or negative
    if cart_item.quantity <= 0:
        cart_item.delete()
        msg = f'{product.name} removed from cart' if not created else 'Invalid quantity'
        message_tag = 'error' if 'Invalid' in msg else 'info'
        current_qty = 0
    else:
        msg = f'{product.name} added to cart!'
        message_tag = 'success'
        current_qty = cart_item.quantity
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        if 'Invalid' in msg:
            messages.error(request, msg)
        else:
            messages.success(request, msg)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': msg,
            'message_tag': message_tag,
            'cart_count': cart.get_item_count(),
            'item_quantity': current_qty,
        })
    
    return redirect('cart')


@require_http_methods(["GET", "POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    print(cart_item)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product_name} removed from cart',
            'message_tag': 'warning',
            'cart_count': cart.get_item_count(),
        })
    
    return redirect('cart')


@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    msg = 'Cart updated'
    message_tag = 'success'
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated')
    else:
        cart_item.delete()
        msg = 'Item removed from cart'
        message_tag = 'info'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_price = sum(item.get_total_price() for item in cart.items.all())
        return JsonResponse({
            'status': 'success',
            'message': msg,
            'message_tag': message_tag,
            'total_price': total_price,
            'cart_count': cart.get_item_count(),
        })
    
    return redirect('cart')


@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared')
    return redirect('cart')


def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart')
    
    total_price = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Process checkout
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        shipping_address = request.POST.get('shipping_address')
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        upazila_id = request.POST.get('upazila')
        union_id = request.POST.get('union')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        # Create order
        from orders.models import Order, OrderItem
        from django.utils import timezone
        import uuid
        
        # Generate order number
        order_number = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        
        # Calculate totals
        subtotal = float(total_price)
        shipping_cost = 20  # 20 TK shipping
        tax = 0  # No tax
        total = subtotal + shipping_cost + tax
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            shipping_address=shipping_address,
            division_id=division_id,
            district_id=district_id,
            upazilla_id=upazila_id,
            union_id=union_id,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            status='processing',
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                total=cart_item.get_total_price(),
            )
        
        # DON'T clear cart here - let payment success handler do it
        # This prevents "cart is empty" errors if redirect fails
        
        # Handle payment method
        if payment_method == 'sslcommerz':
            # Redirect to SSL Commerz payment initiation
            return redirect('payments:ssl-initiate', order_id=order.id)
        else:
            # For other payment methods, clear cart and show confirmation
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order-confirmation', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': f'{float(total_price):.2f}',
    }
    return render(request, 'checkout/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation page"""
    from orders.models import Order
    
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)
        if order.user:
            return redirect('login')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/confirmation.html', context)


@require_http_methods(["GET"])
def cart_count(request):
    """Get cart item count"""
    cart = get_or_create_cart(request)
    from django.db.models import Sum
    count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'count': count})
    
    return JsonResponse({'count': count})


def order_page(request):
    """
    Unified order page for both products and room bookings
    Supports full order process including room selection, date picking, and payment
    """
    from products.models import Room
    from orders.models import Order, OrderItem
    from django.utils import timezone
    from datetime import datetime, timedelta
    import uuid
    
    # Get available rooms
    rooms = Room.objects.filter(status='available')
    
    # Get cart items (for product orders)
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    # Initialize order type
    order_type = request.GET.get('type', 'product')  # 'product' or 'room'
    
    if request.method == 'POST':
        # Get common fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        # Generate order number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Handle room booking
        if order_type == 'room':
            room_id = request.POST.get('room_id')
            check_in = request.POST.get('check_in_date')
            check_out = request.POST.get('check_out_date')
            guests = request.POST.get('number_of_guests', 1)
            special_requests = request.POST.get('special_requests', '')
            
            if not all([room_id, check_in, check_out]):
                messages.error(request, 'Please fill in all required room booking fields')
                return redirect('order-page')
            
            try:
                room = Room.objects.get(id=room_id, status='available')
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                # Validate dates
                if check_in_date < timezone.now().date():
                    messages.error(request, 'Check-in date cannot be in the past')
                    return redirect('order-page')
                
                if check_out_date <= check_in_date:
                    messages.error(request, 'Check-out date must be after check-in date')
                    return redirect('order-page')
                
                # Calculate nights and total
                nights = (check_out_date - check_in_date).days
                subtotal = float(room.price_per_night) * nights
                tax = round(subtotal * 0.08, 2)
                total = subtotal + tax
                
                # Create room booking order
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    order_number=order_number,
                    order_type='room',
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    number_of_guests=int(guests),
                    special_requests=special_requests,
                    subtotal=subtotal,
                    shipping_cost=0,
                    tax=tax,
                    total=total,
                    status='pending',
                )
                
                # Create order item for room
                OrderItem.objects.create(
                    order=order,
                    room=room,
                    quantity=nights,  # Number of nights
                    price=room.price_per_night,
                    total=subtotal,
                )
                
                messages.success(request, f'Room booking created successfully! Order: {order_number}')
                
                # Handle payment
                if payment_method == 'sslcommerz':
                    return redirect('payments:ssl-initiate', order_id=order.id)
                else:
                    return redirect('order-confirmation', order_id=order.id)
                    
            except Room.DoesNotExist:
                messages.error(request, 'Selected room is not available')
                return redirect('order-page')
            except ValueError as e:
                messages.error(request, f'Invalid date format: {str(e)}')
                return redirect('order-page')
        
        # Handle product order
        else:
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('cart')
            
            shipping_address = request.POST.get('shipping_address')
            
            
            # Calculate totals
            subtotal = float(sum(item.get_total_price() for item in cart_items))
            shipping_cost = 0  # Free shipping
            tax = round(subtotal * 0.08, 2)
            total = subtotal + shipping_cost + tax
            
            # Create product order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                order_number=order_number,
                order_type='product',
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                shipping_address=shipping_address,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax=tax,
                total=total,
                status='processing',
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    total=cart_item.get_total_price(),
                )
            
            messages.success(request, f'Order placed successfully! Order: {order_number}')
            
            # Handle payment
            if payment_method == 'sslcommerz':
                return redirect('payments:ssl-initiate', order_id=order.id)
            else:
                # Clear cart for other payment methods
                cart.items.all().delete()
                return redirect('order-confirmation', order_id=order.id)
    
    # GET request - display order page
    total_price = sum(item.get_total_price() for item in cart_items) if cart_items.exists() else 0
    
    context = {
        'rooms': rooms,
        'cart': cart,
        'cart_items': cart_items,
        'total_price': f'{float(total_price):.2f}',
        'order_type': order_type,
        'today': timezone.now().date(),
        'min_checkout': (timezone.now() + timedelta(days=1)).date(),
    }
    return render(request, 'cart/order_page.html', context)

