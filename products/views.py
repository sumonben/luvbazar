from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='active')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=True, methods=['post'])
    def add_review(self, request, slug=None):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            products = self.queryset.filter(
                name__icontains=query
            ) | self.queryset.filter(
                description__icontains=query
            )
        else:
            products = self.queryset.all()

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = self.queryset.filter(rating__gte=4).order_by('-rating')[:10]
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return Review.objects.filter(product__slug=product_slug)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs.get('product_slug'))
        serializer.save(product=product, user=self.request.user)

# Template views for frontend
def index(request):
    """Homepage view"""
    categories = Category.objects.all()[:5]
    featured_products = Product.objects.filter(status='active', rating__gte=4).order_by('-rating')[:12]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context)


def products_list(request):
    """Products listing page with filters"""
    products = Product.objects.filter(status='active')
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['-created_at', 'price', '-price', '-rating']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    
    context = {
        'products': products_page,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, status='active')
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(
        status='active',
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'products/detail.html', context)


def category_detail(request, slug):
    """Category detail page with all products in that category"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(status='active', category=category)
    categories = Category.objects.all()
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['-created_at', 'price', '-price', '-rating']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products_page,
        'categories': categories,
    }
    return render(request, 'products/list.html', context)


def about(request):
    """About page"""
    return render(request, 'about.html')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        from django.contrib import messages as django_messages
        django_messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return render(request, 'contact.html')
    
    return render(request, 'contact.html')


@require_http_methods(["POST"])
def add_review(request, slug):
    """Add a review to a product"""
    from django.contrib.auth.decorators import login_required
    from django.http import JsonResponse
    
    product = get_object_or_404(Product, slug=slug, status='active')
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '')
    
    # Ensure rating is between 1 and 5
    rating = max(1, min(5, rating))
    
    # Create review
    review = Review.objects.create(
        product=product,
        user=request.user,
        rating=rating,
        comment=comment
    )
    
    from django.contrib import messages
    messages.success(request, 'Thank you for your review!')
    
    return redirect('product-detail', slug=slug)