from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import BasketSlot
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.http import JsonResponse
from mainapp.models import Product




class OrderList(ListView):
    model = Order  # формируется на основе модели Order

    def get_queryset(self):  # переопределяем, т.к. по дефолту возвращает список всех товаров во всех заказах
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
    model = Order  # основан на модели Order, так как Order содержит в себе OrderItems
    fields = []
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        # extra=1 означает создать на одну (пустую) форму для OrderItem больше
        # inlineformset_factory  - функция-конструктор, формирующая класс
        # создаем formset для страницы
        if self.request.POST:  # После того, как пользователь нажмет на форме кнопку «Сохранить», создаем набор форм
            # заново на основе данных формы, переданных методом POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = BasketSlot.get_items(self.request.user)
            # basket_items = BasketSlot.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # транзакция в БД (запись в две таблицы одновременно)
            form.instance.user = self.request.user
            self.object = form.save()  # в таблице Order
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()  # в таблице OrderItem
            basket_items = BasketSlot.objects.filter(user=self.request.user)
            basket_items.delete()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
            # instance - указываем, какой заказ правим
        else:
            # data['orderitems'] = OrderFormSet(instance=self.object)
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:order_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:order_list'))


#  реализация изменения количества товаров в корзине с помощью сигналов (pre_save, pre_delete и приемник receiver)
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketSlot)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketSlot)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})

