from django.urls import path

from mainapp.views import products, product_1, product_2, product_3, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product/<int:pk>/', product, name='product'),
    path('product/abb_1420/', product_1, name='product_1420'),
    path('product/abb_4310/', product_2, name='product_4310'),
    path('product/abb_6420/', product_3, name='product_6420'),

]
