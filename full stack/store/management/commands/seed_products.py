from django.core.management.base import BaseCommand
from store.models import Product, Order, OrderItem

# 37 Unique, Distinct Products across 8 Categories
SAMPLE_PRODUCTS = [
    # --- ELECTRONICS (1 to 6) ---
    {
        "name": "Wireless Pro Headphones",
        "category": "Electronics",
        "price": 89.99,
        "original_price": 119.99,
        "discount": 25,
        "rating": 4.8,
        "stock": 18,
        "description": "High-fidelity active noise-cancelling wireless headphones with 40h battery life, deep bass tuning, and ultra-soft memory foam earcups.",
        "image_url": "images/product_headphones.jpg"
    },
    {
        "name": "SmartFit Pro Watch",
        "category": "Electronics",
        "price": 149.99,
        "original_price": 179.99,
        "discount": 16,
        "rating": 4.9,
        "stock": 12,
        "description": "Advanced smartwatch featuring AMOLED display, heart rate monitor, SpO2 sensor, GPS tracking, and 7-day battery life.",
        "image_url": "images/product_smartwatch.jpg"
    },
    {
        "name": "NexPhone Ultra 5G",
        "category": "Electronics",
        "price": 699.99,
        "original_price": 849.99,
        "discount": 18,
        "rating": 4.8,
        "stock": 8,
        "description": "Flagship smartphone featuring 6.7-inch 120Hz OLED display, triple 108MP camera array, and 5G connectivity.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "VortexClick Wireless Mouse",
        "category": "Electronics",
        "price": 42.49,
        "original_price": 49.99,
        "discount": 15,
        "rating": 4.9,
        "stock": 25,
        "description": "Ergonomic wireless mouse with 26,000 DPI optical sensor, ultra-lightweight design, and customizable macro buttons.",
        "image_url": "images/banner_electronics.jpg"
    },
    {
        "name": "Noise Cancelling Earbuds",
        "category": "Electronics",
        "price": 79.99,
        "original_price": 99.99,
        "discount": 20,
        "rating": 4.6,
        "stock": 15,
        "description": "True wireless earbuds with hybrid ANC, IPX5 water resistance, and crystal-clear call quality.",
        "image_url": "images/product_headphones.jpg"
    },
    {
        "name": "Smart LED Desk Lamp",
        "category": "Electronics",
        "price": 34.99,
        "original_price": 44.99,
        "discount": 22,
        "rating": 4.5,
        "stock": 4,
        "description": "Dimmable LED desk lamp with wireless smartphone charging pad, multiple color temperatures, and touch controls.",
        "image_url": "images/banner_electronics.jpg"
    },

    # --- FASHION (7 to 11) ---
    {
        "name": "Silk Summer Floral Dress",
        "category": "Fashion",
        "price": 59.99,
        "original_price": 89.99,
        "discount": 33,
        "rating": 4.7,
        "stock": 14,
        "description": "Breathable silk-blend midi dress featuring vibrant summer floral print and comfortable waist sash.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Classic Vintage Denim Jacket",
        "category": "Fashion",
        "price": 74.99,
        "original_price": 99.99,
        "discount": 25,
        "rating": 4.6,
        "stock": 20,
        "description": "Timeless vintage wash denim jacket made from 100% organic cotton denim with durable metal hardware.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Premium Cotton Fleece Hoodie",
        "category": "Fashion",
        "price": 49.99,
        "original_price": 64.99,
        "discount": 23,
        "rating": 4.8,
        "stock": 15,
        "description": "Ultra-soft heavyweight fleece pullover hoodie with double-lined hood and kangaroo pouch pocket.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Tailored Slim Fit Suit Blazer",
        "category": "Fashion",
        "price": 119.99,
        "original_price": 159.99,
        "discount": 25,
        "rating": 4.9,
        "stock": 9,
        "description": "Elegant wool-blend formal blazer with notch lapel, interior chest pockets, and refined modern silhouette.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Stretch Cotton Chino Pants",
        "category": "Fashion",
        "price": 44.99,
        "original_price": 59.99,
        "discount": 25,
        "rating": 4.5,
        "stock": 16,
        "description": "Stretch cotton twill chinos designed for everyday comfort with wrinkle-resistant finish and classic fit.",
        "image_url": "images/banner_fashion.jpg"
    },

    # --- FOOTWEAR (12 to 16) ---
    {
        "name": "Urban Stride Running Sneakers",
        "category": "Footwear",
        "price": 69.99,
        "original_price": 99.99,
        "discount": 30,
        "rating": 4.7,
        "stock": 22,
        "description": "Lightweight athletic sneakers featuring breathable mesh upper, responsive cushioning, and durable rubber outsole.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Air Cushion Trail Runners",
        "category": "Footwear",
        "price": 89.99,
        "original_price": 119.99,
        "discount": 25,
        "rating": 4.9,
        "stock": 10,
        "description": "Rugged all-terrain running shoes with waterproof membrane, high-traction lugs, and air cushion impact absorption.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Casual Canvas Slip-Ons",
        "category": "Footwear",
        "price": 39.99,
        "original_price": 49.99,
        "discount": 20,
        "rating": 4.4,
        "stock": 3,
        "description": "Everyday slip-on canvas shoes with padded collar, vulcanized rubber sole, and cushioned footbed.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Handcrafted Leather Chelsea Boots",
        "category": "Footwear",
        "price": 129.99,
        "original_price": 169.99,
        "discount": 23,
        "rating": 4.8,
        "stock": 7,
        "description": "Handcrafted full-grain leather Chelsea boots with elastic side gussets, pull tabs, and anti-slip rubber soles.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Outdoor Adventure Sandals",
        "category": "Footwear",
        "price": 34.99,
        "original_price": 44.99,
        "discount": 22,
        "rating": 4.5,
        "stock": 14,
        "description": "Adjustable strap outdoor adventure sandals with arch support, EVA footbed, and quick-drying webbing.",
        "image_url": "images/banner_summer.jpg"
    },

    # --- HOME & DECOR (17 to 21) ---
    {
        "name": "Handcrafted Terracotta Ceramic Vase",
        "category": "Home & Decor",
        "price": 29.99,
        "original_price": 39.99,
        "discount": 25,
        "rating": 4.8,
        "stock": 16,
        "description": "Artisan terracotta ceramic vase with matte textured glaze finish, ideal for dried flowers or standalone accent decor.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "Minimalist LED Floor Lamp",
        "category": "Home & Decor",
        "price": 89.99,
        "original_price": 119.99,
        "discount": 25,
        "rating": 4.7,
        "stock": 9,
        "description": "Sleek architectural standing lamp with remote control, stepless dimming, and energy-efficient LED technology.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "Luxury Velvet Throw Pillow Pair",
        "category": "Home & Decor",
        "price": 34.99,
        "original_price": 44.99,
        "discount": 22,
        "rating": 4.6,
        "stock": 15,
        "description": "Set of 2 ultra-soft velvet cushion covers with invisible zipper closures and plush microfiber inserts.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "Aromatherapy Essential Oil Diffuser",
        "category": "Home & Decor",
        "price": 39.99,
        "original_price": 49.99,
        "discount": 20,
        "rating": 4.9,
        "stock": 12,
        "description": "Ultrasonic cool mist diffuser with 500ml capacity, 7 ambient LED light colors, and automatic shut-off feature.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "Macrame Woven Wall Tapestry",
        "category": "Home & Decor",
        "price": 24.99,
        "original_price": 32.99,
        "discount": 24,
        "rating": 4.7,
        "stock": 18,
        "description": "Handmade macrame wall hanging crafted from 100% natural cotton cord mounted on a natural wooden dowel.",
        "image_url": "images/hero_products.jpg"
    },

    # --- BEAUTY (22 to 25) ---
    {
        "name": "Organic Glow Hydrating Serum",
        "category": "Beauty",
        "price": 39.99,
        "original_price": 49.99,
        "discount": 20,
        "rating": 4.9,
        "stock": 30,
        "description": "Nourishing facial serum infused with Hyaluronic Acid, Vitamin C, and Niacinamide for radiantly hydrated skin.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Botanical Day Cream & Cleanser Set",
        "category": "Beauty",
        "price": 29.99,
        "original_price": 39.99,
        "discount": 25,
        "rating": 4.7,
        "stock": 25,
        "description": "Gentle plant-based facial cleanser and moisturizing day cream set for all skin types.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Rosewater Hydrating Facial Mist",
        "category": "Beauty",
        "price": 19.99,
        "original_price": 24.99,
        "discount": 20,
        "rating": 4.6,
        "stock": 20,
        "description": "Refreshing natural Damask rosewater hydrating spray to tone skin and lock in moisture throughout the day.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Velvet Matte Lipstick Trio",
        "category": "Beauty",
        "price": 32.99,
        "original_price": 42.99,
        "discount": 23,
        "rating": 4.8,
        "stock": 15,
        "description": "Long-wearing non-drying matte lipstick set in nude, classic red, and berry plum shades.",
        "image_url": "images/banner_fashion.jpg"
    },

    # --- ACCESSORIES (26 to 29) ---
    {
        "name": "Explorer Pro Travel Backpack",
        "category": "Accessories",
        "price": 54.99,
        "original_price": 79.99,
        "discount": 31,
        "rating": 4.6,
        "stock": 14,
        "description": "Water-resistant commuter backpack with padded 15.6-inch laptop compartment, hidden anti-theft pocket, and USB port.",
        "image_url": "images/hero_products.jpg"
    },
    {
        "name": "Full-Grain Leather Slim Bifold Wallet",
        "category": "Accessories",
        "price": 29.99,
        "original_price": 39.99,
        "discount": 25,
        "rating": 4.8,
        "stock": 25,
        "description": "Hand-stitched RFID-blocking bifold wallet crafted from full-grain Italian leather with quick-access card slots.",
        "image_url": "images/banner_fashion.jpg"
    },
    {
        "name": "Polarized UV400 Aviator Sunglasses",
        "category": "Accessories",
        "price": 45.00,
        "original_price": 60.00,
        "discount": 25,
        "rating": 4.5,
        "stock": 18,
        "description": "Classic metal frame aviator sunglasses featuring 100% UV400 protection polarized lenses and comfortable nose pads.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Stainless Steel Mesh Watch",
        "category": "Accessories",
        "price": 79.99,
        "original_price": 99.99,
        "discount": 20,
        "rating": 4.8,
        "stock": 11,
        "description": "Sleek analog quartz timepiece with scratch-resistant sapphire crystal glass and mesh steel band.",
        "image_url": "images/product_smartwatch.jpg"
    },

    # --- GROCERIES (30 to 32) ---
    {
        "name": "Artisanal Dark Roast Coffee (1kg)",
        "category": "Groceries",
        "price": 24.99,
        "original_price": 29.99,
        "discount": 17,
        "rating": 4.9,
        "stock": 35,
        "description": "Single-origin Arabica dark roast whole coffee beans roasted fresh in small batches with notes of chocolate and caramel.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Cold-Pressed Extra Virgin Olive Oil",
        "category": "Groceries",
        "price": 18.99,
        "original_price": 22.99,
        "discount": 17,
        "rating": 4.8,
        "stock": 28,
        "description": "First cold-pressed unrefined extra virgin olive oil harvested from Mediterranean olive groves.",
        "image_url": "images/banner_summer.jpg"
    },
    {
        "name": "Raw Wildflower Honey Jar (500g)",
        "category": "Groceries",
        "price": 14.99,
        "original_price": 18.99,
        "discount": 21,
        "rating": 4.9,
        "stock": 22,
        "description": "100% pure unfiltered raw honey rich in natural enzymes and antioxidants harvested from local apiaries.",
        "image_url": "images/banner_summer.jpg"
    },

    # --- GAMING (33 to 35) ---
    {
        "name": "RGB Mechanical Gaming Keyboard",
        "category": "Gaming",
        "price": 89.99,
        "original_price": 119.99,
        "discount": 25,
        "rating": 4.9,
        "stock": 12,
        "description": "Full-size mechanical keyboard with hot-swappable tactile switches, per-key RGB backlighting, and aluminum top frame.",
        "image_url": "images/banner_electronics.jpg"
    },
    {
        "name": "7.1 Surround Gaming Headset",
        "category": "Gaming",
        "price": 69.99,
        "original_price": 89.99,
        "discount": 22,
        "rating": 4.7,
        "stock": 16,
        "description": "7.1 virtual surround sound headset with noise-canceling detachable microphone and breathable cooling-gel ear pads.",
        "image_url": "images/product_headphones.jpg"
    },
    {
        "name": "Ergonomic High-Back Gaming Chair",
        "category": "Gaming",
        "price": 199.99,
        "original_price": 249.99,
        "discount": 20,
        "rating": 4.8,
        "stock": 5,
        "description": "Heavy-duty gaming chair with lumbar support pillow, 135-degree recline function, 4D armrests, and PU leather finish.",
        "image_url": "images/banner_electronics.jpg"
    }
]


class Command(BaseCommand):
    help = "Seed database with clean, non-duplicate sample products for ShopEase"

    def handle(self, *args, **options):
        # Clear existing products to prevent duplicates
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared existing products database to rebuild clean product list..."))

        created_count = 0
        for item in SAMPLE_PRODUCTS:
            product = Product.objects.create(
                name=item["name"],
                category=item["category"],
                price=item["price"],
                original_price=item["original_price"],
                discount=item["discount"],
                rating=item["rating"],
                stock=item["stock"],
                description=item["description"],
                image_url=item["image_url"]
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} clean, unique products across 8 categories!"))
