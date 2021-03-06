"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import main, products, contacts, product_1, product_2, product_3
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import debug_toolbar
import social_django

urlpatterns = [
    path('', main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contacts/', contacts, name='contacts'),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('basket/', include('basketapp.urls', namespace='basket')),
    path('order/', include('ordersapp.urls', namespace='orders')),

    path('admin/', include('adminapp.urls', namespace='admin')),
    # path('admin_custom/', include('adminapp.urls', namespace='admin_custom')),
    # path('admin/', admin.site.urls),  # стандартная админка django

    path('__debug__/', include(debug_toolbar.urls)),
    path('', include("social_django.urls", namespace='social'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
