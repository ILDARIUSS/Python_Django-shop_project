import json
import os
from datetime import datetime, timezone
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Category, Product  # noqa


BASE_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = BASE_DIR / "catalog" / "fixtures"
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)


def iso(dt: datetime) -> str:
    """Безопасная ISO-строка для фикстур."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    # Django нормально ест и "+00:00", но "Z" тоже ок
    return dt.isoformat().replace("+00:00", "Z")


def dump_categories() -> None:
    data = []
    for obj in Category.objects.all().order_by("id"):
        data.append(
            {
                "model": "catalog.category",
                "pk": obj.pk,
                "fields": {
                    "name": obj.name,
                    "description": obj.description,
                },
            }
        )

    path = FIXTURES_DIR / "categories.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✔ categories.json written in UTF-8")


def dump_products() -> None:
    data = []
    now = datetime.now(timezone.utc)

    for obj in Product.objects.all().order_by("id"):
        created = getattr(obj, "created_at", None) or now
        updated = getattr(obj, "updated_at", None) or created or now

        data.append(
            {
                "model": "catalog.product",
                "pk": obj.pk,
                "fields": {
                    "name": obj.name,
                    "description": obj.description,
                    "price": str(obj.price),
                    "category": obj.category_id,
                    "image": obj.image.name if obj.image else "",
                    "created_at": iso(created),
                    "updated_at": iso(updated),
                },
            }
        )

    path = FIXTURES_DIR / "products.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✔ products.json written in UTF-8")


dump_categories()
dump_products()
