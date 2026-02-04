from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.select_related("category").all()
    return render(request, "catalog/home.html", {"products": products})


def contacts(request):
    return render(request, "catalog/contacts.html")
