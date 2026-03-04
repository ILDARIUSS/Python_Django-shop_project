from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from .models import Category, Product
from .services import get_products_by_category

CACHE_TTL = 60  # секунд


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    return render(request, "catalog/contacts.html")


def product_list(request):
    """
    Список товаров (низкоуровневый кеш).
    """
    cache_key = "product_list"

    if getattr(settings, "CACHE_ENABLED", False):
        products = cache.get(cache_key)
        if products is None:
            qs = Product.objects.all().select_related("category").order_by("-id")

            if hasattr(Product, "is_published"):
                qs = qs.filter(is_published=True)
            if hasattr(Product, "is_available"):
                qs = qs.filter(is_available=True)

            products = list(qs)
            cache.set(cache_key, products, CACHE_TTL)
    else:
        qs = Product.objects.all().select_related("category").order_by("-id")
        if hasattr(Product, "is_published"):
            qs = qs.filter(is_published=True)
        if hasattr(Product, "is_available"):
            qs = qs.filter(is_available=True)
        products = qs

    return render(request, "catalog/product_list.html", {"products": products})


def _product_detail_impl(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


# Кеширование страницы товара
if getattr(settings, "CACHE_ENABLED", False):
    product_detail = cache_page(CACHE_TTL)(_product_detail_impl)
else:
    product_detail = _product_detail_impl


def category_products(request, pk: int):
    """
    Страница товаров по категории + сервисная функция + кеш по категории.
    """
    category = get_object_or_404(Category, pk=pk)
    cache_key = f"category_products:{pk}"

    if getattr(settings, "CACHE_ENABLED", False):
        products = cache.get(cache_key)
        if products is None:
            products = list(get_products_by_category(pk))
            cache.set(cache_key, products, CACHE_TTL)
    else:
        products = get_products_by_category(pk)

    return render(
        request,
        "catalog/category_products.html",
        {"category": category, "products": products},
    )