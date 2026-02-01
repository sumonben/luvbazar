from .models import Cart

def cart_count(request):
    """Context processor to make cart_item_count available in all templates"""
    count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.filter(session_id=session_id).first()
        else:
            cart = None
    
    if cart:
        count = cart.get_item_count()
        print(f"Cart item count: {count}")
    return {'cart_item_count': count}