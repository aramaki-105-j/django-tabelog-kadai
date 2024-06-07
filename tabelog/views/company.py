import requests
from myproject import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from tabelog.models import CustomUser


class CompanyAdminView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get(self, request):
        
        return render(request, 'company/company_admin.html')

    def post(self, request):
        email = self.request.user.email   
        custom_user = CustomUser.objects.get(email=email)
        custom_user.is_staff = True 
        custom_user.save()

        return redirect('home')