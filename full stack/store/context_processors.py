from .cart import get_cart_details


def cart_context(request):
    """Context processor making cart total count available across all templates."""
    try:
        cart_info = get_cart_details(request)
        return {
            'cart_count': cart_info['total_count'],
            'cart_grand_total': cart_info['grand_total'],
        }
    except Exception:
        return {
            'cart_count': 0,
            'cart_grand_total': 0,
        }
