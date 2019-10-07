from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from .adm_forms import AdmEditForm, AdmUserCreateForm

app_name = 'adminapp'


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(IsSuperUserView, ListView):
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


class ProductDetailView(IsSuperUserView, DetailView):
    model = Product
    template_name = 'adm_product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # context['title'] = Product.objects.get(pk=self.kwargs.get('pk')).name
        # context['title'] = '{}. Админка'.format(title)
        context['title'] = self.object.name
        return context


#
class ProductCreateView(IsSuperUserView, CreateView):
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

class ProductUpdateView(IsSuperUserView, UpdateView):
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


class ProductDeleteView(IsSuperUserView, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('admin_custom:products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        title = Product.objects.get(pk=self.kwargs.get('pk')).name
        context['title'] = 'Удаление {}. Админка'.format(title)
        return context


class UsersListView(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'Список зарегистрированных пользователей'
        return context

class UserDetailView(IsSuperUserView, DetailView):
    model = ShopUser
    template_name = 'adm_user_overview.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        title = ShopUser.objects.get(pk=self.kwargs.get('pk')).username
        context['title'] = 'Детали пользователя {}'.format(title)
        return context



class UserUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'adm_user_edit.html'
    success_url = reverse_lazy('admin_custom:user_read')
    # fields = '__all__'
    form_class = AdmEditForm


    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        title = ShopUser.objects.get(pk=self.kwargs.get('pk')).username
        context['title'] = 'Редактирование пользователя {}'.format(title)
        context['button_label'] = 'Применить'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:user_read', kwargs={'pk': self.kwargs.get('pk')})


class UserCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'adm_user_edit.html'
    success_url = reverse_lazy('admin_custom:user_read')
    form_class = AdmUserCreateForm

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание нового пользователя'
        context['button_label'] = 'Создать'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:user_read', kwargs={'pk': self.object.pk})


class UserDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'user_delete.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        title = ShopUser.objects.get(pk=self.kwargs.get('pk')).username
        context['title'] = 'Удаление пользователя {}'.format(title)
        return context


class CategoriesListView(IsSuperUserView, ListView):
    model = ProductCategory
    template_name = 'categories_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['title'] = 'Список категорий товаров'
        return context

class CategoriesDetailView(IsSuperUserView, DeleteView):
    model = ProductCategory
    template_name = 'adm_product_category_overview.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesDetailView, self).get_context_data(**kwargs)
        title = ProductCategory.objects.get(pk=self.kwargs.get('pk')).name
        context['title'] = 'Информация о категории "{}"'.format(title)
        return context

class CategoryUpdateView(IsSuperUserView, UpdateView):
    model = ProductCategory
    template_name = 'adm_product_category_edit.html'
    success_url = reverse_lazy('admin_custom:category_read')
    fields = '__all__'


    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        title = ProductCategory.objects.get(pk=self.kwargs.get('pk')).name
        context['title'] = 'Редактирование категории "{}"'.format(title)
        context['button_label'] = 'Применить'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:category_read', kwargs={'pk': self.kwargs.get('pk')})


class CategoryDeleteView(IsSuperUserView, DeleteView):
    model = ProductCategory
    template_name = 'adm_product_category_delete.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        title = ProductCategory.objects.get(pk=self.kwargs.get('pk')).name
        context['title'] = 'Удаление категории "{}"'.format(title)
        return context


class CategoryCreateView(IsSuperUserView,  CreateView):
    model = ProductCategory
    template_name = 'adm_product_category_edit.html'
    success_url = reverse_lazy('admin_custom:category_read')
    # form_class = AdmUserCreateForm
    fields = '__all__'


    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание новой категории товаров'
        context['button_label'] = 'Создать'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:category_read', kwargs={'pk': self.object.pk})