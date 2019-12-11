from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.views.generic.edit import UpdateView
from .models import ShopUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST.get('next')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('main'))
    next = request.GET.get('next')

    content = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print("Сообщение для активации пользователя отправлено на почту")
                return HttpResponseRedirect(reverse('auth:login'))
            # auth.login(request, user)
            # return HttpResponseRedirect(reverse('main'))
            else:
                print("Ошибка отправки сообщения!")
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)

class EditView(UpdateView):
    model = ShopUser
    template_name = 'authapp/register.html'
    fields = 'username', 'email', 'avatar'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        context['submit_label'] = 'Применить'
        return context

@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form =ShopUserEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'authapp/edit.html', content)



def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    print(f'from: {settings.EMAIL_HOST_USER}, to: {user.email}')
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        context = {"email": email}
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'user {user} is activated')
            user.is_active = True
            user.save()
            # backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'authapp/verification_ok.html', context)
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification_error.html', context)
    except Exception as e:
        print(f'error activation user: {e.args}')

    return HttpResponseRedirect(reverse('main'))


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)




