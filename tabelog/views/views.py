from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from allauth.account import views
from django.views import View, generic
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http.response import HttpResponse
from tabelog.models import Store, Booking, Review, Category, Like
from tabelog.forms import ProfileForm, StoreForm, ReviewForm
from allauth.account import views
from tabelog.models import CustomUser
from django.db.models import Avg, FloatField, Value
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Coalesce, Round



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

class StoreView(ListView):
    model = Store
    template_name = "home.html"


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.annotate(
            average_score=Coalesce(Round(Avg("review__score"), 1), Value(0, output_field=FloatField()))
        ).order_by('-average_score')

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(address__icontains=q) | Q(tel__icontains=q) | Q(description__icontains=q)
            )
        if self.request.GET.get('category'):
            category_id = self.request.GET.get('category')
            queryset = queryset.filter(category__id=category_id)

        if self.request.GET.get('order_by'):
            order = self.request.GET.get('order_by')
            queryset = queryset.order_by(order)

        return queryset
   
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seach_text"] = self.request.GET.get('q', '')
        ctx["categorys"] = Category.objects.all()
        ctx['current_order'] = self.request.GET.get('order_by', '-average_score')
        ctx['average_scores'] = self.get_queryset().values('id', 'average_score')
        return ctx
        

class StoreDetailView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        reviews = Review.objects.filter(store_id=store_data.id)
        average = reviews.aggregate(Avg("score"))['score__avg']or 0
        average = round(average,2)
        review_count = Review.objects.filter(store_id=store_data.id).count()
        is_like = Like.objects.filter(store_id=store_data.id, user_id=request.user.id).exists()

	        
        return render(request, 'store/store.html', {
            'store_data': store_data,
            'reviews': reviews,
            'average': average,
            'review_count': review_count,
            'is_like': is_like,
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
            store_id = kwargs['store_id'],
            user_id = request.user.id,
            comment = request.POST['comment'],
            score = request.POST['score'],
        )
        return redirect('home')
   
class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'store/review_delete.html'
    model = Review
    success_url = reverse_lazy('home')
        
    def test_func(self):
        review = Review.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_paid and review.user_id == self.request.user.id

    def handle_no_permission(self):
        return redirect('home')
    
class ReviewUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'store/review_form.html'
    model = Review
    fields = ['comment', 'score']
    success_url = reverse_lazy('home')
        
    def test_func(self):
        review = Review.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_paid and review.user_id == self.request.user.id

    def handle_no_permission(self):
        return redirect('home')
    
 

