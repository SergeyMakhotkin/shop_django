from django.urls import path

import authapp.views as authapp



app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    # path('edit/<int:pk>/', authapp.EditView.as_view(), name='edit'),
    path('edit/', authapp.edit, name='edit'),

]