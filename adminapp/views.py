from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory
# from .forms import ProductAdminForm

app_name = 'adminapp'

# class IsSuperUserView(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Список продуктов. Админка'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            queryset = queryset.filter(category=category_pk)
        return queryset



class ProductDetailView(DetailView):
    model = Product
    template_name = 'adm_product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # context['title'] = Product.objects.get(pk=self.kwargs.get('pk')).name
        # context['title'] = '{}. Админка'.format(title)
        context['title'] = self.object.name
        return context

#
class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_update.html'
    success_url = reverse_lazy('admin_custom:product_read')
    fields = '__all__'


    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание нового продукта'
        context['button_label'] = 'Создать'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:product_read', kwargs={'pk': self.object.pk})
#

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    success_url = reverse_lazy('admin_custom:products')
    fields = '__all__'
    # form_class = ProductAdminForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        title = Product.objects.get(pk=self.kwargs.get('pk')).name
        context['title'] = 'Изменение {}. Админка'.format(title)
        context['button_label'] = 'Применить'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:product_read', kwargs={'pk': self.kwargs.get('pk')})
#
# class ProductDeleteView(IsSuperUserView, DeleteView):
#     model = Product
#     template_name = 'adminapp/product_delete.html'
#     success_url = reverse_lazy('admin_custom:products')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductDeleteView, self).get_context_data(**kwargs)
#         title = Product.objects.get(pk=self.kwargs.get('pk')).name
#         context['title'] = 'Удаление {}. Админка'.format(title)
#         return context
#
#
