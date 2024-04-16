from django.urls import path, include
from . import views
from tabelog import views

app_name = "tabelog"

urlpatterns = [
    path('', views.TopView.as_view(), name="home"),
    #path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
]