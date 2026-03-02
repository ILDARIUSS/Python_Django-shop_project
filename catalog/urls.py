from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),

    # список товаров
    path("catalog/", views.product_list, name="product_list"),

    # детальная карточка товара (кеш страницы)
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # товары конкретной категории
    path("catalog/category/<int:pk>/", views.category_products, name="category_products"),
]
