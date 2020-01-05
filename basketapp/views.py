from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, reverse, HttpResponse
from .models import BasketSlot
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F

@login_required
def basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.select_related('product', 'product__category').all()

    return render(request, 'basket.html', {'basket_items': basket})


@login_required
def add(request, product_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=product_pk)
    old_basket_slot = BasketSlot.objects.filter(user=request.user, product=product).first()

    if old_basket_slot:
        # # 1. классический вариант обновления значения атрибута
        # old_basket_slot.quantity += 1
        # old_basket_slot.save()

        # 2. вариант с использованием F-объектов
        old_basket_slot.quantity = F('quantity') + 1
    else:
        new_basket_slot = BasketSlot(user=request.user, product=product)
        new_basket_slot.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove(request, product_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[product_pk]))

    product = get_object_or_404(Product, pk=product_pk)
    basket_slot = BasketSlot.objects.filter(user=request.user, product=product).first()

    if basket_slot:
        if basket_slot.quantity == 1:
            basket_slot.delete()
        else:
            # basket_slot.quantity -= 1
            # basket_slot.save()
            basket_slot.quantity = F('quantity') - 1

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_slot(request, slot_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse("basket"))

    basket_slot = BasketSlot.objects.filter(user=request.user, id=slot_pk).first()

    if basket_slot:
        basket_slot.delete()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit(request, pk):
    print(pk)
    print(request.GET.get('quantity'))
    basket_slot = get_object_or_404(BasketSlot, pk=pk)
    quantity = int(request.GET.get('quantity'))
    if quantity > 0:
        basket_slot.quantity = quantity
        basket_slot.save()
    else:
        basket_slot.delete()
    basket_items = BasketSlot.objects.filter(user=request.user)
    context = {'basket_items': basket_items,}
    result = render_to_string('includes/inc_basket_list.html', context)

    return JsonResponse({'result': result})
