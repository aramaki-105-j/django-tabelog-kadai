import requests
from myproject import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from tabelog.models import CustomUser, Store
from tabelog.forms import StoreCreateForm


class StoreAdminView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get(self, request):
        
        return render(request, 'store_admin/store_admin.html')

    def post(self, request):
        email = self.request.user.email   
        custom_user = CustomUser.objects.get(email=email)
        custom_user.is_staff = True 
        custom_user.save()

        return redirect('home')


class StoreCreateView(UserPassesTestMixin, CreateView):
    template_name = 'store_admin/storecreate_form.html'
    model = Store
    form = StoreCreateForm()
    fields = ['name', 'address', 'tel', 'description', 'category', 'image']
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')
    
    def post(self, request, *args, **kwargs):
        form = StoreCreateForm(request.POST)
        if form.is_valid():
           store = Store()
           store.name = form.cleaned_data['name']
           store.address = form.cleaned_data['address']
           store.tel = form.cleaned_data['tel']
           store.description = form.cleaned_data['description']
           store.category = form.cleaned_data['category']
           if request.FILES:
               store.image = request.FILES.get('image')
           store.save()

           return redirect('home')

        return render(request, 'store_admin/storecreate_form.html', {'form': form})