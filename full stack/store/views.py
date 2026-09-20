from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden

from .models import Product, Order, OrderItem, CATEGORY_CHOICES
from .cart import (
    get_cart_details, cart_add_item, cart_remove_item,
    cart_clear, get_cart
)


def home(request):
    """Phase 1 homepage with dynamic featured products."""
    featured_products = Product.objects.all()[:8]
    context = {
        'page_title': 'ShopEase – Discover Products You\'ll Love',
        'featured_products': featured_products,
    }
    return render(request, 'store/home.html', context)



def product_list(request):
    """
    Phase 2: Products page view.
    Supports search (q), category filtering (category), and sorting (sort).
    """
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'default').strip()

    products = Product.objects.all()

    # Search filter
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Category filter
    if category and category.lower() != 'all':
        products = products.filter(category__iexact=category)

    # Sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')

    categories = ['All'] + [choice[0] for choice in CATEGORY_CHOICES]

    context = {
        'page_title': 'Shop Products – ShopEase',
        'products': products,
        'categories': categories,
        'current_category': category if category else 'All',
        'search_query': q,
        'current_sort': sort,
        'total_count': products.count(),
    }
    return render(request, 'store/products.html', context)


def product_detail(request, pk):
    """
    Phase 3: Complete dynamic Product Details view (/products/<id>/).
    Handles non-existing products gracefully with a custom 404 template.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        context = {
            'page_title': 'Product Not Found – ShopEase',
            'requested_id': pk,
        }
        return render(request, 'store/product_not_found.html', context, status=404)

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    review_count = int(float(product.rating) * 26) + (product.id * 5)
    savings = (product.original_price - product.price) if (product.original_price and product.original_price > product.price) else 0

    context = {
        'page_title': f'{product.name} – ShopEase',
        'product': product,
        'related_products': related_products,
        'review_count': review_count,
        'savings': savings,
    }
    return render(request, 'store/product_detail.html', context)


# ============================================================
# CART VIEWS
# ============================================================

def cart_detail(request):
    """Render Shopping Cart page."""
    cart_info = get_cart_details(request)
    context = {
        'page_title': 'Shopping Cart – ShopEase',
        'cart': cart_info,
    }
    return render(request, 'store/cart.html', context)


def cart_add(request, product_id):
    """Add product to cart via POST or GET."""
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_detail', pk=product_id)

    qty = int(request.POST.get('quantity', request.GET.get('quantity', 1)))
    cart_add_item(request, product_id, quantity=qty)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_info = get_cart_details(request)
        return JsonResponse({
            'status': 'success',
            'message': f'Added {qty}x {product.name} to cart!',
            'cart_count': cart_info['total_count'],
            'cart_total': str(cart_info['grand_total']),
        })

    messages.success(request, f"Added {product.name} to your shopping cart.")
    return redirect('cart_detail')


def cart_update(request, product_id):
    """Update item quantity in cart."""
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))

    if qty > product.stock:
        qty = product.stock
        messages.warning(request, f"Quantity adjusted to available stock ({product.stock} units).")

    cart_add_item(request, product_id, quantity=qty, override_quantity=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_info = get_cart_details(request)
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_info['total_count'],
            'cart_total': str(cart_info['grand_total']),
            'subtotal': str(cart_info['subtotal']),
            'shipping_fee': str(cart_info['shipping_fee']),
        })

    return redirect('cart_detail')


def cart_remove(request, product_id):
    """Remove product from cart."""
    product = Product.objects.filter(id=product_id).first()
    cart_remove_item(request, product_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_info = get_cart_details(request)
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_info['total_count'],
            'cart_total': str(cart_info['grand_total']),
        })

    if product:
        messages.info(request, f"Removed {product.name} from your cart.")
    return redirect('cart_detail')


# ============================================================
# USER AUTHENTICATION VIEWS
# ============================================================

def register_view(request):
    """User Registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation checks
        if not username or not email or not password:
            messages.error(request, "All required fields must be filled.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match. Please check and try again.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email address already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to ShopEase, {user.username}! Your account has been created.")

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')

    context = {
        'page_title': 'Create an Account – ShopEase',
        'next': request.GET.get('next', ''),
    }
    return render(request, 'store/register.html', context)


def login_view(request):
    """User Login."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_post = request.POST.get('next', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            target = next_post or next_url or 'home'
            if target and target.startswith('/'):
                return redirect(target)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    context = {
        'page_title': 'Sign In – ShopEase',
        'next': next_url,
    }
    return render(request, 'store/login.html', context)


def logout_view(request):
    """User Logout."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


# ============================================================
# CHECKOUT & ORDER VIEWS
# ============================================================

@login_required(login_url='login')
def checkout(request):
    """Checkout Page & Place Order Workflow."""
    cart_info = get_cart_details(request)

    if not cart_info['items']:
        messages.warning(request, "Your cart is currently empty. Please add products before checking out.")
        return redirect('products')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')

        if not (full_name and email and phone and address and city and state and pincode):
            messages.error(request, "Please fill in all shipping details.")
        else:
            # Re-verify stock before placing order
            for item in cart_info['items']:
                try:
                    product = Product.objects.get(id=item['id'])
                    if product.stock < item['quantity']:
                        messages.error(request, f"Stock changed! Only {product.stock} units of {product.name} left.")
                        return redirect('cart_detail')
                except Product.DoesNotExist:
                    messages.error(request, f"Product {item['name']} is no longer available.")
                    return redirect('cart_detail')

            # Create Order
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                total_amount=cart_info['grand_total'],
                shipping_fee=cart_info['shipping_fee'],
                payment_method=payment_method,
                status='Confirmed'
            )

            # Create OrderItems & Reduce Stock
            for item in cart_info['items']:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                # Decrement stock
                product.stock = max(0, product.stock - item['quantity'])
                product.save()

            # Clear session cart
            cart_clear(request)

            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_confirmation', order_id=order.id)

    context = {
        'page_title': 'Checkout – ShopEase',
        'cart': cart_info,
        'user': request.user,
    }
    return render(request, 'store/checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order Confirmation Page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'page_title': f'Order #{order.id} Confirmed – ShopEase',
        'order': order,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required(login_url='login')
def my_orders(request):
    """My Orders Page — Lists logged in user's orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'page_title': 'My Orders – ShopEase',
        'orders': orders,
    }
    return render(request, 'store/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Individual Order Detail Page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'page_title': f'Order #{order.id} Details – ShopEase',
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)
