from typing import Iterable

from django.db.models import QuerySet

from .models import Product


def get_products_by_category(category_id: int) -> QuerySet[Product]:
    """
    Возвращает список товаров в указанной категории.
    Здесь сосредоточена бизнес-логика получения товаров.
    """
    qs = Product.objects.filter(category_id=category_id)

    # Если у вас в модели есть флаги публикации/доступности — учитываем их.
    # Если какого-то поля нет — удалите соответствующую строку.
    if hasattr(Product, "is_published"):
        qs = qs.filter(is_published=True)
    if hasattr(Product, "is_available"):
        qs = qs.filter(is_available=True)

    return qs.select_related("category").order_by("name")
