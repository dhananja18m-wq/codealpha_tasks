from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'discount', 'stock', 'rating', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'discount')
    ordering = ('-created_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('full_name', 'email', 'phone', 'id')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
