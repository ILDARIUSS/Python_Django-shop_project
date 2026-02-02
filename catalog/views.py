from django.shortcuts import render
from .models import Product


def home(request):
    # Достаём товары из БД
    # select_related('category') ускоряет доступ к product.category.name
    products = Product.objects.select_related("category").all()

    context = {
        "products": products,
    }
    return render(request, "catalog/home.html", context)


def contacts(request):
    # Как и раньше: пока просто отдаём статическую страницу контактов
    return render(request, "catalog/contacts.html")
