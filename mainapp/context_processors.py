from basketapp.models import BasketSlot

def basket(request):
#    print(f'context processor basket works')
   basket = []

   if request.user.is_authenticated:
       basket = BasketSlot.objects.filter(user=request.user)


   return {
       'basket': basket,
   }


def user_data(request):
    print(f'context processor user_data works')
    if request.user.is_authenticated:
        username = request.user
        return {
            'username': username,
        }
