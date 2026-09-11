def get_mock_products():
    """Returns a list of mock product dictionaries for UI testing."""
    products = [
        {
            "name": "Classic White Sneakers",
            "price": 59.99,
            "category": "Shoes",
            "similarity": 96.5,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
        },
        {
            "name": "Brown Leather Handbag",
            "price": 89.99,
            "category": "Bags",
            "similarity": 91.2,
            "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"
        },
        {
            "name": "Denim Jacket",
            "price": 74.50,
            "category": "Jackets",
            "similarity": 88.7,
            "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
        },
        {
            "name": "Silver Analog Watch",
            "price": 129.00,
            "category": "Watches",
            "similarity": 85.3,
            "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"
        },
        {
            "name": "Black Running Shoes",
            "price": 64.99,
            "category": "Shoes",
            "similarity": 82.9,
            "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400"
        }
    ]
    return products