from django.shortcuts import render


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")

        # Просто для проверки - вывод в консоль
        print(f"[CONTACT FORM] name={name} message={message}")

        context["success"] = True
        context["name"] = name

    return render(request, "catalog/contacts.html", context)
from django.shortcuts import render

# Create your views here.
