from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views import View
import addresses
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Register(View) :
    def get(self, request, *args, **kwargs) :
        print(kwargs)
        form = RegisterForm()
        return render(request, addresses.register_template, {"form" : form})
    
    def post(self, request, *args, **kwargs) :
        print(**kwargs)
        form = RegisterForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            form.save()
            return redirect(addresses.land_url)
        
        return render(request, addresses.register_template, {"form" : form})


class Login(LoginView) :
    template_name = addresses.login_template


@method_decorator(login_required, name="dispatch")
class Profile(View) :
    template_name = addresses.profile_template
    def get(self, request) :
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class PasswordChange(PasswordChangeView) :
    template_name = addresses.password_change_template


@method_decorator(login_required, name="dispatch")
class PasswordChangeDone(PasswordChangeDoneView) :
    template_name = addresses.password_change_done_template


@method_decorator(login_required, name="dispatch")
class Logout(LogoutView) :
    template_name = addresses.land_template