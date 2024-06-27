import requests
from myproject import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView
from tabelog.models import CustomUser, Store, Category, Company
from tabelog.forms import StoreCreateForm
from django.db.models import Q

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

class StoreEditView(UserPassesTestMixin, UpdateView):
    template_name = 'store_admin/store_edit_form.html'
    model = Store
    form = StoreCreateForm()
    fields = ['name', 'address', 'tel', 'description', 'category', 'image']
    success_url = reverse_lazy('home')
        
    def test_func(self):
        store = Store.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

class StoreDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'store_admin/store_delete_form.html'
    model = Store
    success_url = reverse_lazy('home')
        
    def test_func(self):
        store = Store.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

class UserListView(UserPassesTestMixin, ListView):
    template_name = 'store_admin/user_list.html'
    model = CustomUser
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        active_count = queryset.filter(is_active=True).count()
        paid_count = queryset.filter(is_paid=True).count()

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            queryset = queryset.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(address__icontains=q) | Q(email__icontains=q)
                )
        return queryset
   
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['seach_text'] = self.request.GET.get('q', '')
        ctx['active_count'] = self.get_queryset().filter(is_active=True).count()
        ctx['paid_count'] = self.get_queryset().filter(is_paid=True).count()
        ctx['unpaid_active_count'] = ctx['active_count'] - ctx['paid_count']
        ctx['total_paid_amount'] = ctx['paid_count'] * 300
        return ctx

class CategoryCreateView(UserPassesTestMixin, CreateView):
    template_name = 'store_admin/category_create_form.html'
    model = Category
    fields = ['name']
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')
    
    def post(self, request, *args, **kwargs):
        Category.objects.create(
            name = request.POST['name'],
        )
        return redirect('home')

class CategoryListView(UserPassesTestMixin, ListView):
    template_name = 'store_admin/category_list.html'
    model = Category
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            queryset = queryset.filter(
                Q(name__icontains=q)
                )
        return queryset
   
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seach_text"] = self.request.GET.get('q', '')
        return ctx

class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'store_admin/category_delete_form.html'
    model = Category
    success_url = reverse_lazy('home')
        
    def test_func(self):
        category = Category.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

class CategoryEditView(UserPassesTestMixin, UpdateView):
    template_name = 'store_admin/category_edit_form.html'
    model = Category
    fields = ['name']
    success_url = reverse_lazy('home')
        
    def test_func(self):
        category = Category.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

class CompanyInfoView(ListView):
    template_name = 'store_admin/company_information.html'
    model = Company
    fields = ['name', 'address', 'tel']

class CompanyInfoUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'store_admin/company_information_update.html'
    model = Company
    fields = ['name', 'address', 'tel']
    success_url = reverse_lazy('home')
        
    def test_func(self):
        company = Company.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')
    