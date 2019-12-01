from django import forms
from ordersapp.models import Order, OrderItem

class OrderForm(forms.ModelForm):  # используется форма, поля которой создаются
                                    # на базе существующей модели
                                    # если использовать forms.Form то все поля нужно будет создавать вручную
   class Meta:
       model = Order
       exclude = ('user',)  # поля, которые исключаем из форм. кортеж

   def __init__(self, *args, **kwargs):
       super(OrderForm, self).__init__(*args, **kwargs)
       for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'