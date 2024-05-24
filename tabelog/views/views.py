from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from allauth.account import views
from django.views import View
from django.views.decorators.http import require_POST
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http.response import HttpResponse
from tabelog.models import Store, Booking, Review
from tabelog.forms import ProfileForm, StoreForm, ReviewForm
from allauth.account import views
from tabelog.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'account/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'email': user_data.email,
                'telephone_number': user_data.telephone_number,
                'post_code': user_data.post_code,
                'address': user_data.address,
            }
        )

        return render(request, 'account/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.email = form.cleaned_data['email']
            user_data.telephone_number = form.cleaned_data['telephone_number']
            user_data.post_code = form.cleaned_data['post_code']
            user_data.address = form.cleaned_data['address']
            
            user_data.save()
            return redirect('profile')

        return render(request, 'registration/profile.html', {
            'form': form
        })

class CreateCheckoutView(TemplateView):
    template_name = "subscription/create_checkout_session.html"

class SubscriptionCancelView(TemplateView):
   template_name = "subscription/checkout_cancel.html"

class StoreView(View):
    def get(self, request, *args, **kwargs):
        store_data = Store.objects.all()

        return render(request, 'home.html', {
            'store_data': store_data,
        })

class StoreDetailView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])

        return render(request, 'store/store.html', {
            'store_data': store_data,
        })
        
class ReviewList(ListView):
    template_name = 'store/review_list.html'
    model = Review


class ReviewCreateView(UserPassesTestMixin, CreateView):
    template_name = 'store/review_form.html'
    model = Review
    fields = ['comment', 'score']
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')
    
    def post(self, request, *args, **kwargs):
        Review.objects.create(
            store = kwargs['store_id'],
            user=request.user.id,
            comment=request.POST['comment'],
            score=request.POST['score'],
        )
        return render(request, 'home.html')
   