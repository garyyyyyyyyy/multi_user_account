from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='login-or-register-page'),
    path('index', views.index, name='index-page'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
    path('create-user', views.create_user, name='create-user'),
    path('', views.home),
]