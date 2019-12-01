from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':

        api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None, urlencode(
            OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'country', 'city', 'domain',)),
                        access_token=response['access_token'], v='5.92')), None))

        # api_url_2 = urlunparse(('https', 'api.vk.com', '/method/account.getInfo', None, urlencode(
        #     OrderedDict(fields=','.join(('lang')),
        #                 access_token=response['access_token'], v='5.92')), None))


        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        print('ответ от VK API: ', resp.json())


        # resp_2 = requests.get(api_url_2)
        # if resp_2.status_code != 200:
        #     return
        #
        # data_2 = resp_2.json()['response'][0]
        # print('ответ от VK API: ', resp_2.json())

        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about'] and not user.shopuserprofile.aboutMe:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year

            user.age = age
            # так не работает
            # if age:
            #     print(age)
            #     ShopUser.objects.filter(id=user.shopuserprofile.user_id).update(age=age)

            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')



        # if data['lang']:
        #     print('значение lang: ', data['lang'])
        #     lang_choice = {0: 'ru', 1: 'uk', 2: 'be', 3: 'en', 4: 'es', 5: 'fi', 6: 'de', 7: 'it'}
        #     user.shopuserprofile.language = lang_choice[data['lang']]

        if data['country']:
            user.shopuserprofile.country = data['country']['title']



        if data['city']:
            user.shopuserprofile.city = data['city']['title']

        if data['domain']:
            user.shopuserprofile.link = 'https://vk.com/'+data['domain']


        user.save()
