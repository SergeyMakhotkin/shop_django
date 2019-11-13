from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
# from django.contrib.auth.models import User  # Стандартная модель пользователя
from authapp.models import ShopUser

import json, os

JSON_PATH = os.path.join('mainapp', 'json')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()  # Удаляет существующие записи
        for category in categories:
            new_category = ProductCategory(**category)  # распаковка словорей в нужный формат
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            if "image" in product:
                product_image_path = os.path.join('products_images', product["image"])
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            if ("image" in product):
                product["image"] = product_image_path
            else:
                product["image"] = os.path.join('products_images', "nophoto.jpg")
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        ShopUser.objects.all().delete()
        ShopUser.objects.create_superuser('admin', 'admin@geekshop.local', '12345678', age=27)
