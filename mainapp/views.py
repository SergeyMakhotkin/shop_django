from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from basketapp.models import BasketSlot
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# настройка низкоуровневого кэширования
# начало настройки LOW_CACHE

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


# def get_categories():
#     if settings.LOW_CACHE:
#         key = 'categories'
#         categories = cache.get(key)
#         if categories is None:
#             categories = get_object_or_404(ProductCategory.objects.all())
#             cache.set(key, categories)
#         return categories
#     else:
#         return get_object_or_404(ProductCategory.objects.all())


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.all()
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.all()


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            # products = Product.objects.all().select_related('category')
            products = Product.objects.all()
            cache.set(key, products)
        return products
    else:
        return Product.objects.all()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.all().order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.all().order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk).order_by('price')


# конец настройки LOW_CACHE

def main(request):
    # links_menu = [
    #     {'href': 'product_1', 'name': 'ABB Tropos 1420'},
    #     {'href': 'product_2', 'name': 'ABB Tropos 4310'},
    #     {'href': 'product_3', 'name': 'ABB Tropos 6420'}
    # ]
    username = "Гость" if request.user.is_anonymous else request.user.username
    # context = {'links_menu': get_links_menu(), 'products': get_products(), 'username': username}
    context = {'products': get_products(), 'username': username}
    return render(request, 'index.html', context)


@cache_page(3600)
def products(request, pk=None):
    var_products = get_products()
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.select_related('product').all()
        # basket = BasketSlot.objects.filter(user=request.user)
    if pk is not None:
        if pk > 0:
            category = get_category(pk)
            var_products = get_products().filter(category=category)

        content = {'products': var_products, 'categories': get_categories()}
        return render(request, 'catalog.html', content)
    else:
        content = {'hot_product': get_products().filter(is_hot=True).first(),
                   'categories': get_categories()}
        return render(request, 'hot_product.html', content)


# def get_basket(user):
#     if user.is_authenticated:
#         return basket.objects.filter(user=user)
#     else:
#         return []

@cache_page(3600)
def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk),
        # 'basket': request.user.basket.all(),
    }

    return render(request, 'product.html', content)


@cache_page(3600)
def contacts(request):
    return render(request, 'contacts.html')


@cache_page(3600)
def product_1(request):
    content = {'products': get_products(), 'categories': get_categories()}
    return render(request, 'product_1420.html', content)


@cache_page(3600)
def product_2(request):
    content = {'products': get_products(), 'categories': get_categories()}
    return render(request, 'product_4310.html', content)


@cache_page(3600)
def product_3(request):
    content = {'products': get_products(), 'categories': get_categories()}
    return render(request, 'product_6420.html', content)
