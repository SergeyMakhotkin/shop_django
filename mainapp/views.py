from django.shortcuts import render
from mainapp.models import ProductCategory, Product


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


def products(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'catalog.html', content)


def contacts(request):
    return render(request, 'contacts.html')


def product_1(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'product_1420.html', content)


def product_2(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'product_4310.html', content)


def product_3(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'product_6420.html', content)
