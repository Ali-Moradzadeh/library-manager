from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views import View
import addresses
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class Register(View) :
    form_class = RegisterForm
    register_template = addresses.register_template
    redirect_url = addresses.land_url
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated :
            return redirect(addresses.land_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs) :
        form = self.form_class()
        return render(request, self.register_template, {"form" : form})
    
    def post(self, request, *args, **kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            form.save()
            return redirect(self.redirect_url)
        return render(request, self.register_template, {"form" : form})


class Login(LoginView) :
    template_name = addresses.login_template
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated :
            if "next" in kwargs :
                return redirect(kwargs["next"])
            else :
                return redirect(addresses.land_url)
        return super().dispatch(request, *args, **kwargs)


class Profile(LoginRequiredMixin, View) :
    template_name = addresses.profile_template
    def get(self, request) :
        return render(request, self.template_name)


class PasswordChange(LoginRequiredMixin, PasswordChangeView) :
    template_name = addresses.password_change_template


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView) :
    template_name = addresses.password_change_done_template


class Logout(LoginRequiredMixin, LogoutView) :
    template_name = addresses.land_template