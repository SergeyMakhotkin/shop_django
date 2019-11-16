from django.urls import path

from mainapp.views import products, product_1, product_2, product_3, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product/<int:pk>/', product, name='product'),
    # path('product/2/', product_2, name='product_4310'),
    # path('product/3/', product_3, name='product_6420'),

]
