from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None, #'/method/account.getInfo',
                              urlencode(OrderedDict(fields=','.join(
                                  # ('bdate', 'sex', 'about', 'user_ids', 'lang', 'country', 'city')),
                                  ('bdate', 'sex', 'about', 'user_ids', 'lang', 'country', 'city')),

                                  access_token=response['access_token'],
                                  v='5.103')), None))
        resp = requests.get(api_url)
        print(resp)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        print('ответ от VK API: ')
        print(resp.json())
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about'] and not user.shopuserprofile.aboutMe:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data['lang']:
            lang_choice = {0: 'ru', 1: 'uk', 2: 'be', 3: 'en', 4: 'es', 5: 'fi', 6: 'de', 7: 'it'}
            user.shopuserprofile.language = lang_choice[data['lang']]

        if data['country']:
            user.shopuserprofile.country = data['country']['title']


        if data['city']:
            user.shopuserprofile.city = data['city']['title']

        if data['user_ids']:
            user.shopuserprofile.link = 'https://vk.com/id'+data['user_ids']


        user.save()
