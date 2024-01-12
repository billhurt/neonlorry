import random
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def latest_products(request):
    latest_products = Product.products.all().order_by('-created')[:3]
    return render(request, 'store/index.html', {'latest_products': latest_products})


def all_products(request):
    products = Product.products.all()
    return render(request, 'store/shop.html', {'products': products})


def product_detail(request, slug):
    # Get single product, a list of random products and pass the amount of a particular product that is available
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    products = list(Product.products.all())
    n = len(products)
    random_products = random.sample(products, n)
    template_vars = {
        'product': product,
        'random_products': random_products,
    }
    # Slug is equal to 'slug' in Product model, and 'in_stock' is true in Product model too
    return render(request, 'store/detail.html', template_vars)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # select one item in the 'Category' database where the slug is equal to the category_slug passed by the url
    products = Product.objects.filter(category=category)
    # 'products' will equal all products with a category equal to the category_slug
    return render(request, 'store/category.html', {'category': category, 'products': products})
