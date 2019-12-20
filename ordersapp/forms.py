from django import forms
from ordersapp.models import Order, OrderItem, Product

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
    price = forms.CharField(label='цена', required=False)   # добавляем статическое поле в форму для отображения цены
                        # текстовое поле, т.к. не должно редактироваться, проходить валидацию и сохраняться в базе
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # self.fields['product'].queryset = Product.get_items()
            self.fields['product'].queryset = Product.get_items().select_related()

