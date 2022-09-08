from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'authenticate'

urlpatterns = [
    path('register/', views.Register.as_view(), name="user_register"),
    path('login/', views.Login.as_view(), name="user_login"),
    path('profile/', views.Profile.as_view(), name="user_profile"),
    path('logout/', views.Logout.as_view(), name="user_logout"),
    path('password-change/', views.PasswordChange.as_view(success_url=reverse_lazy("authenticate:user_password_change_done")), name="user_password_change"),
    path('password_change_done', views.PasswordChangeDone.as_view(), name="user_password_change_done")
]
