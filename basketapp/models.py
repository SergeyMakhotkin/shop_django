from django.db import models
from django.conf import settings
from mainapp.models import Product


class BasketSlot(models.Model):
    class Meta:
        verbose_name = 'Слот корзины'
        verbose_name_plural = 'Слоты корзины'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    created = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='время последнего изменения', auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.product.name)

    def get_cost(self):
        return self.quantity * self.product.price

    cost = property(get_cost)

    @staticmethod
    def get_items(user):
        return BasketSlot.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_item(pk):
        return BasketSlot.objects.filter(pk=pk).first()
