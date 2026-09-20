from decimal import Decimal
from .models import Product

CART_SESSION_ID = 'cart'


def get_cart(request):
    """Retrieve session cart or initialize if empty."""
    cart = request.session.get(CART_SESSION_ID)
    if not cart:
        cart = request.session[CART_SESSION_ID] = {}
    return cart


def cart_add_item(request, product_id, quantity=1, override_quantity=False):
    """Add a product or update its quantity in the session cart."""
    cart = get_cart(request)
    product = Product.objects.get(id=product_id)
    product_id_str = str(product_id)

    if product_id_str not in cart:
        cart[product_id_str] = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': 0,
            'image_url': product.get_image_url,
            'category': product.category,
            'max_stock': product.stock,
        }

    if override_quantity:
        cart[product_id_str]['quantity'] = min(quantity, product.stock)
    else:
        cart[product_id_str]['quantity'] = min(cart[product_id_str]['quantity'] + quantity, product.stock)

    if cart[product_id_str]['quantity'] <= 0:
        cart_remove_item(request, product_id)
    else:
        request.session.modified = True


def cart_remove_item(request, product_id):
    """Remove product item from session cart."""
    cart = get_cart(request)
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session.modified = True


def cart_clear(request):
    """Clear session cart."""
    if CART_SESSION_ID in request.session:
        del request.session[CART_SESSION_ID]
        request.session.modified = True


def get_cart_details(request):
    """
    Returns calculated cart items list, subtotal, shipping fee, total, and item count.
    Shipping fee = $0 if subtotal >= 49 or subtotal == 0 else $4.99.
    """
    cart = get_cart(request)
    items = []
    subtotal = Decimal('0.00')
    total_count = 0

    for pid, item_data in cart.items():
        qty = item_data['quantity']
        price = Decimal(item_data['price'])
        item_total = price * qty
        subtotal += item_total
        total_count += qty

        items.append({
            'id': item_data['id'],
            'name': item_data['name'],
            'price': price,
            'quantity': qty,
            'item_total': item_total,
            'image_url': item_data['image_url'],
            'category': item_data['category'],
            'max_stock': item_data.get('max_stock', 99),
        })

    shipping_fee = Decimal('0.00') if (subtotal >= Decimal('49.00') or subtotal == Decimal('0.00')) else Decimal('4.99')
    grand_total = subtotal + shipping_fee

    return {
        'items': items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
        'total_count': total_count,
        'free_shipping_eligible': subtotal >= Decimal('49.00'),
        'away_from_free_shipping': max(Decimal('0.00'), Decimal('49.00') - subtotal),
    }
