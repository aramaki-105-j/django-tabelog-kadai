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




class CalendarView(View):
    def get(self, request, *args, **kwargs):
        today = date.today()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            # 週始め
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
        # 1週間
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        # 10時～20時
        for hour in range(10, 21):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
        booking_data = Booking.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False

        return render(request, 'store/calendar.html', {
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
        })

class BookingView(UserPassesTestMixin, CreateView):
    template_name = 'store/booking.html'
    model = Booking
    form_class = BookingForm
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')
    

    def post(self, request, *args, **kwargs):
        Booking.objects.create(
            store_id = kwargs['store_id'],
            user_id = request.user.id,
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            tel = request.POST['tel'],
            remarks = request.POST['remarks'],
            start = request.POST['start'],
        )
        
        return redirect('thanks')

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

