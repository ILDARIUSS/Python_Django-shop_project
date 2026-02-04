from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Категория")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # ✅ поле для изображения (MEDIA)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
