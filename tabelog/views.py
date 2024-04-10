from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import MyPasswordChangeForm
from django.views import generic
from .forms import LoginForm

class TopView(TemplateView):
    template_name = "home.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'

class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'home.html'

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('tabelog:password_change_done')
    template_name = 'registration/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'


