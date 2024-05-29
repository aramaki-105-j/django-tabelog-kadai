from django.shortcuts import redirect, render
from tabelog.models import Like
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy



class LikeCreateView(UserPassesTestMixin, CreateView):
    model = Like
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')
    

    def post(self, request, *args, **kwargs):
        Like.objects.create(
            store_id = kwargs['store_id'],
            user_id = request.user.id,
        )
        
        return redirect('store_detail', kwargs['store_id'])


class LikeCancelView(UserPassesTestMixin, DeleteView):
    template_name = 'store/booking_cancel.html'
    model = Like
    success_url = reverse_lazy('home')
        
    def test_func(self):
        booking = Booking.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_paid and booking.user_id == self.request.user.id

    def handle_no_permission(self):
        return redirect('home')

