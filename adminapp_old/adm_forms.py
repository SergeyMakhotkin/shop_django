from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authapp.models import ShopUser
from django.forms import forms
from django.forms.widgets import HiddenInput


class AdmEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = HiddenInput()


class AdmUserCreateForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = 'username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'avatar', 'age'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


