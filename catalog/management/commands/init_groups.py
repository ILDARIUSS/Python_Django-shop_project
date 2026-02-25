from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product


class Command(BaseCommand):
    help = "Создает группу модераторов товаров и назначает права (ДЗ-28)"

    def handle(self, *args, **options):
        group_name = "Модератор продуктов"
        group, _ = Group.objects.get_or_create(name=group_name)

        ct = ContentType.objects.get_for_model(Product)

        perm_delete = Permission.objects.get(codename="delete_product", content_type=ct)
        perm_unpublish = Permission.objects.get(codename="can_unpublish_product", content_type=ct)

        group.permissions.add(perm_delete, perm_unpublish)

        self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' создана, права назначены."))