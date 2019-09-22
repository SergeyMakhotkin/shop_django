from django.urls import path

from mainapp.views import products, product_1, product_2, product_3

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    # path('product/1/', product_1, name='product_1420'),
    # path('product/2/', product_2, name='product_4310'),
    # path('product/3/', product_3, name='product_6420'),

]