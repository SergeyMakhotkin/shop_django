from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from basketapp.models import BasketSlot




# Create your views here.

def main(request):
    #context = {'username': 'SERGEY'}
    #links_menu = [
    links_menu = [
        {'href': 'product_1420', 'name': 'ABB Tropos 1420'},
        {'href': 'product_4310', 'name': 'ABB Tropos 4310'},
        {'href': 'product_6420', 'name': 'ABB Tropos 6420'}
    ]
    username = "Гость" if request.user.is_anonymous else request.user.username
    context = {'links_menu': links_menu, 'username': username, 'products': Product.objects.all()}
    return render(request, 'index.html', context)


def products(request, pk=None):
    var_products = Product.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.all()
        # basket = BasketSlot.objects.filter(user=request.user)
    if pk is not None:
        if pk > 0:
            category = get_object_or_404(ProductCategory, pk=pk)
            var_products = var_products.filter(category=category)

        content = {'products': var_products, 'categories': ProductCategory.objects.all(), 'basket': basket}
        return render(request, 'catalog.html', content)
    else:
        content = {'hot_product': Product.objects.filter(is_hot=True).first(),
                   'categories': ProductCategory.objects.all(),
                   'basket': basket}
        return render(request, 'hot_product.html', content)

def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'product.html', content)


def contacts(request):
    return render(request, 'contacts.html')


def product_1(request):
    content = {'products': Product.objects.all(), 'categories': ProductCategory.objects.all()}
    return render(request, 'product_1420.html', content)


def product_2(request):
    content = {'products': Product.objects.all(), 'categories': ProductCategory.objects.all()}
    return render(request, 'product_4310.html', content)


def product_3(request):
    content = {'products': Product.objects.all(), 'categories': ProductCategory.objects.all()}
    return render(request, 'product_6420.html', content)
