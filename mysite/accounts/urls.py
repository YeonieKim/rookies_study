# accounts/urls.py
from django.urls import path
from . import views

app_name= 'accounts'

urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("login_method1/", views.login_method1, name="login_method1"),
    path("login_method2/", views.login_method2, name="login_method2"),
]