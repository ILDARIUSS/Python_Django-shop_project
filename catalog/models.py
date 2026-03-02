from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    # ✅ домашка 28: владелец + публикация
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Владелец",
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]

    def __str__(self) -> str:
        return self.name