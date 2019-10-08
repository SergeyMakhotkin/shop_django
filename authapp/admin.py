from django.contrib import admin

# Register your models here.

from authapp.models import ShopUser
from basketapp.models import BasketSlot

admin.site.register(ShopUser)

class BasketSlotInline(admin.TabularInline):
    model = BasketSlot
    extra = 0

class ShopUserBasketView(ShopUser):
    class Meta:
        verbose_name = 'Пользователь с корзиной'
        verbose_name_plural = 'пользователи с корзиной'
        proxy = True


@admin.register(ShopUserBasketView)
class ShopUserBasketView(admin.ModelAdmin):
    fields = 'username',
    list_display = 'username', 'get_basket_quantity', 'get_basket_cost'
    readonly_fields = 'username',
    inlines = BasketSlotInline,
    # list_display = 'name', 'category', 'is_hot'
    # list_filter = 'is_hot',
    # search_fields = 'name',
    # readonly_fields = 'quantity',

    def get_queryset(self, request):
        return ShopUser.objects.filter(basket__quantity__gt=0).distinct()

    def get_basket_quantity(self, instance):
        basket = instance.basket.all()
        # basket = BasketSlot.objects.filter(user=instance)
        total_quantity = sum(list(map(lambda basket_slot: basket_slot.quantity, basket)))
        return total_quantity

    get_basket_quantity.short_description = 'Количество товаров в корзине'

    # def get_total_cost(self, instance):


    def get_basket_cost(self, instance):
        basket = BasketSlot.objects.select_related('product').filter(user=instance)
        return sum(list(map(lambda basket_slot: basket_slot.cost, basket)))

    get_basket_cost.short_description = 'Общая стоимость'
