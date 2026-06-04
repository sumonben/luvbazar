from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import PhoneNumberRegistrationForm, PhoneNumberLoginForm
from orders.models import Order
from cart.views import migrate_session_cart_to_user


def register(request):
    """User registration view using phone number"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = PhoneNumberRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Capture old session ID before login (because login() creates a new session)
                old_session_id = request.session.session_key
                
                phone = form.cleaned_data['phone']
                email = form.cleaned_data.get('email', '')
                password1 = form.cleaned_data['password1']
                first_name = form.cleaned_data.get('first_name', '')
                
                # Create user with phone as username (for Django's auth system)
                user = User.objects.create_user(
                    username=phone,
                    email=email if email else '',
                    password=password1,
                    first_name=first_name
                )
                
                # Create user profile with phone
                UserProfile.objects.create(user=user, phone=phone)
                
                # Login the user with explicit backend
                user.backend = 'users.backends.PhoneNumberBackend'
                login(request, user)
                
                # Migrate cart from session to user after successful registration
                # Pass the OLD session ID that we captured before login
                migrate_session_cart_to_user(request, user, old_session_key=old_session_id)
                
                messages.success(request, 'Account created successfully!')
                return redirect('home')
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return render(request, 'auth/register.html', {'form': form})
        else:
            return render(request, 'auth/register.html', {'form': form})
    else:
        form = PhoneNumberRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view using phone number"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = PhoneNumberLoginForm(request.POST)
        if form.is_valid():
            # Capture old session ID before login (because login() creates a new session)
            old_session_id = request.session.session_key
            
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Authenticate using phone number (as username)
            user = authenticate(request, username=phone, password=password)
            
            if user is not None:
                # Set the backend explicitly for login
                user.backend = 'users.backends.PhoneNumberBackend'
                login(request, user)
                
                # Migrate cart from session to user after successful login
                # Pass the OLD session ID that we captured before login
                migrate_session_cart_to_user(request, user, old_session_key=old_session_id)
                
                if not remember_me:
                    request.session.set_expiry(0)
                    
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid phone number or password.')
                return render(request, 'auth/login.html', {'form': form})
        else:
            return render(request, 'auth/login.html', {'form': form})
    else:
        form = PhoneNumberLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    """User profile view"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'profile': profile,
        'orders': orders,
    }
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_update(request):
    """Update user profile"""
    if request.method == 'POST':
        try:
            existing_user = User.objects.get(username=request.POST.get('phone', ''))
            if existing_user:
                messages.error(request, 'Phone number is already in use by another account.')
                return redirect('profile')
        except User.DoesNotExist:
            existing_user = None

        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        bio = request.POST.get('bio', '')
        
        user = request.user
        user.first_name = first_name
        user.email = email
        user.username = phone  # Update username to match phone number
        user.save()
        
        profile = user.userprofile
        profile.phone = phone
        profile.bio = bio
        profile.save()
        
        messages.success(request, 'Phone number is updated to match the phone number. Please use your phone number for future logins.')
        return redirect('profile')
    return redirect('profile')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        old_session_id = request.session.session_key
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        user = request.user
        
        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('profile')
        
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('profile')
        
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('profile')
        
        user.set_password(new_password1)
        user.save()
        user.backend = 'users.backends.PhoneNumberBackend'
        login(request, user)
        migrate_session_cart_to_user(request, user, old_session_key=old_session_id)
        messages.success(request, 'Password changed successfully!')
        return redirect('profile')
    
    return redirect('profile')


def password_reset(request):
    """Password reset request"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            messages.success(
                request,
                'If this email is registered, you will receive password reset instructions.'
            )
        except User.DoesNotExist:
            messages.success(
                request,
                'If this email is registered, you will receive password reset instructions.'
            )
        
        return render(request, 'auth/password_reset.html')
    
    return render(request, 'auth/password_reset.html')


@login_required(login_url='login')
def orders_list(request):
    """Display user orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/orders_list.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)
