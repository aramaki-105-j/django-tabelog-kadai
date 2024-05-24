from django.urls import path, include

from tabelog.views import credit, views, booking
from django.contrib import admin
from django.conf.urls.static import static 
from django.conf import settings





urlpatterns = [
    path('account/', include('allauth.urls')),
    path('', views.StoreView.as_view(), name="home"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    
    path('calendar/<int:pk>/', booking.CalendarView.as_view(), name='calendar'), 
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', booking.CalendarView.as_view(), name='calendar'), 
    path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', booking.BookingView.as_view(), name='booking'),
    path('thanks/', booking.ThanksView.as_view(), name='thanks'),
    path('review/store/<int:store_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review_list/', views.ReviewList.as_view(), name='review_list'),
    
         

    path('credit/register', credit.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update', credit.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel', credit.SubscriptionCancelView.as_view(), name='subscription-cancel'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)