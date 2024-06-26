from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime, make_aware
from django.views.generic import View
from tabelog.models import Store, Booking
from tabelog.forms import BookingForm
from django.views.generic import View, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class BookingView(UserPassesTestMixin, CreateView):
    template_name = 'store/booking.html'
    model = Booking
    form_class = BookingForm

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.store_id = self.kwargs['store_id']
        self.object.user = self.request.user
        self.object.start = datetime.combine(
            form.cleaned_data['start_date'], 
            form.cleaned_data['start_time']
        )
        self.object.save()
        return redirect('thanks')

    def post(self, request, *args, **kwargs):
        self.object = None 
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BookingCancelView(UserPassesTestMixin, DeleteView):
    template_name = 'store/booking_cancel.html'
    model = Booking
    success_url = reverse_lazy('home')
        
    def test_func(self):
        booking = Booking.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_paid and booking.user_id == self.request.user.id

    def handle_no_permission(self):
        return redirect('home')

class BookingListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')

    def get(self, request, *args, **kwargs):
        booking_data = Booking.objects.filter(user_id=request.user.id)

        return render(request, 'store/booking_list.html', {
            'booking_data': booking_data,
        })

    

class ThanksView(TemplateView):
    template_name = 'store/thanks.html'

