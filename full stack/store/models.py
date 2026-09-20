from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Footwear', 'Footwear'),
    ('Home & Decor', 'Home & Decor'),
    ('Beauty', 'Beauty'),
    ('Accessories', 'Accessories'),
    ('Groceries', 'Groceries'),
    ('Gaming', 'Gaming'),
]


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True, help_text="Path to static image or fallback URL")
    stock = models.IntegerField(default=10)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    discount = models.IntegerField(default=0, help_text="Discount percentage (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            if self.image_url.startswith('http://') or self.image_url.startswith('https://') or self.image_url.startswith('/'):
                return self.image_url
            return static(self.image_url)
        return static('images/product_headphones.jpg')

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def stock_status(self):
        if self.stock <= 0:
            return 'Out of Stock'
        elif self.stock <= 5:
            return f'Only {self.stock} left'
        return 'In Stock'


ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.status})"

    @property
    def subtotal(self):
        return self.total_amount - self.shipping_fee


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order #{self.order.id})"

    @property
    def get_total(self):
        return self.price * self.quantity
