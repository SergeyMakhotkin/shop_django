from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    help = "Скрипт создаёт записи в таблице для связанной модели ShopUserProfile " \
           "из данных таблицы основной модели ShopUser"

    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            users_profile = ShopUserProfile.objects.create(user=user)
            users_profile.save()
