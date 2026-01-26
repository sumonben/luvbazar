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
    tax_total = round(cart_total_float * 0.08, 2)  # 8% tax
    order_total = round(cart_total_float + tax_total, 2)
    
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
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart',
            'cart_count': cart.items.count(),
        })
    
    return redirect('cart')


@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    if cart_item.cart == cart:
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{product_name} removed from cart')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Item removed from cart',
            'cart_count': cart.items.count(),
        })
    
    return redirect('cart')


@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    if cart_item.cart == cart:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated')
        else:
            cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_price = sum(item.get_total_price() for item in cart.items.all())
        return JsonResponse({
            'status': 'success',
            'total_price': total_price,
        })
    
    return redirect('cart')


@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared')
    return redirect('cart')


@login_required(login_url='login')
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
        street_address = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        # Create order
        from orders.models import Order, OrderItem
        from django.utils import timezone
        import uuid
        
        # Generate order number
        order_number = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        
        # Calculate totals
        subtotal = float(total_price)
        shipping_cost = 0  # Free shipping
        tax = round(subtotal * 0.08, 2)  # 8% tax
        total = subtotal + shipping_cost + tax
        
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            street_address=street_address,
            apartment=apartment,
            shipping_city=city,
            shipping_state=state,
            shipping_zip=zip_code,
            shipping_country=country,
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


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    from orders.models import Order
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
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
