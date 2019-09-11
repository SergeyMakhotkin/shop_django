from django.shortcuts import render


# Create your views here.

def main(request):
    context = {'username': 'SERGEY'}
    links_menu = [
        {'href': 'product_1420', 'name': 'ABB Tropos 1420'},
        {'href': 'product_4310', 'name': 'ABB Tropos 4310'},
        {'href': 'product_6420', 'name': 'ABB Tropos 6420'}
    ]
    return render(request, 'index.html', context, links_menu)


def products(request):
    return render(request, 'catalog.html')


def contacts(request):
    return render(request, 'contacts.html')


def product_1(request):
    return render(request, 'product_1420.html')


def product_2(request):
    return render(request, 'product_4310.html')


def product_3(request):
    return render(request, 'product_6420.html')
