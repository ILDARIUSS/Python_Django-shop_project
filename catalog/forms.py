from django import forms
from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_WORDS
from .models import Product


def _contains_forbidden_words(value: str) -> bool:
    """Проверяет, содержит ли строка запрещенные слова (без учета регистра)."""
    if not value:
        return False
    lower_value = value.lower()
    return any(word in lower_value for word in FORBIDDEN_WORDS)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "category",
            "price",
            "image",
            "stock",
            "is_available",
            "is_published",  # ✅ добавили для ДЗ-28
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Общие bootstrap-классы
        for field_name, field in self.fields.items():
            # Чекбоксы оформляем отдельно
            if field_name in ("is_available", "is_published"):
                field.widget.attrs.update({"class": "form-check-input"})
                continue

            # Остальные поля — input/select/file/textarea
            field.widget.attrs.update({"class": "form-control"})

        # UX плейсхолдеры
        self.fields["name"].widget.attrs.update({"placeholder": "Название товара"})
        self.fields["description"].widget.attrs.update({"placeholder": "Описание товара"})

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if _contains_forbidden_words(name):
            raise ValidationError("Название содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        if _contains_forbidden_words(description):
            raise ValidationError("Описание содержит запрещенные слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            return price
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price