from django.urls import path, include

from tabelog.views import credit, views, booking, like, company
from django.contrib import admin
from django.conf.urls.static import static 
from django.conf import settings





urlpatterns = [
    path('account/', include('allauth.urls')),
    path('', views.StoreView.as_view(), name="home"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    
    path('booking/store/<int:store_id>/', booking.BookingView.as_view(), name='booking'),
    path('booking/store/booking_cancel/<int:pk>/', booking.BookingCancelView.as_view(), name='booking_cancel'),
    path('booking/store/booking_list/', booking.BookingListView.as_view(), name='booking_list'),
    path('thanks/', booking.ThanksView.as_view(), name='thanks'),

    path('review/store/<int:store_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review_list/', views.ReviewList.as_view(), name='review_list'),
    path('review/store/review_delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review/store/update/<int:pk>/', views.ReviewUpdateView.as_view(), name='review_update'),
    
    path('like_create/store/<int:store_id>/', like.LikeCreateView.as_view(), name='like_create'),
    path('like_cancel/store/<int:pk>/', like.LikeCancelView.as_view(), name='like_cancel'),
    path('like_list/store/', like.LikeListView.as_view(), name='like_list'),     

    path('credit/register', credit.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update', credit.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel', credit.SubscriptionCancelView.as_view(), name='subscription-cancel'),

    path('company/admin/', company.StoreAdminView.as_view(), name='store_admin'),
    path('company/store/create/', company.StoreCreateView.as_view(), name='store_create'),
    path('company/store/edit/<int:pk>/', company.StoreEditView.as_view(), name='store_edit'),
    path('company/store/delete/<int:pk>/', company.StoreDeleteView.as_view(), name='store_delete'),
    path('user_list/', company.UserListView.as_view(), name='user_list'),
    path('category_list/category/create/', company.CategoryCreateView.as_view(), name='category_create'),
    path('category_list/', company.CategoryListView.as_view(), name='category_list'),
    path('category_list/category/delete/<int:pk>/', company.CategoryDeleteView.as_view(), name='category_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)