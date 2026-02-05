from pathlib import Path

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.db import transaction


class Command(BaseCommand):
    help = "Clear DB and load shop data from fixtures (categories.json, products.json)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fixtures-dir",
            type=str,
            default="catalog/fixtures",
            help="Path to directory with fixtures (default: catalog/fixtures)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fixtures_dir = Path(options["fixtures_dir"])

        categories_path = fixtures_dir / "categories.json"
        products_path = fixtures_dir / "products.json"

        if not categories_path.exists():
            self.stderr.write(self.style.ERROR(f"Fixture not found: {categories_path}"))
            return

        if not products_path.exists():
            self.stderr.write(self.style.ERROR(f"Fixture not found: {products_path}"))
            return

        # Берём модели через apps.get_model, чтобы избежать циклических импортов
        Category = apps.get_model("catalog", "Category")
        Product = apps.get_model("catalog", "Product")

        self.stdout.write("Step 1/4: deleting Products...")
        Product.objects.all().delete()

        self.stdout.write("Step 2/4: deleting Categories...")
        Category.objects.all().delete()

        self.stdout.write("Step 3/4: loading categories fixture...")
        call_command("loaddata", str(categories_path), verbosity=1)

        self.stdout.write("Step 4/4: loading products fixture...")
        call_command("loaddata", str(products_path), verbosity=1)

        self.stdout.write(self.style.SUCCESS("Done! Shop data loaded successfully."))
