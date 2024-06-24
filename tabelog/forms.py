from django import forms
from allauth.account.forms import SignupForm 
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser, Store, Review, Booking, Company
from django.forms import ModelForm, DateInput, TimeInput
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    email = forms.CharField(max_length=150, label='メールアドレス')
    telephone_number = forms.CharField(max_length=150, label='電話番号')
    post_code = forms.CharField(max_length=150, label='郵便番号')
    address = forms.CharField(max_length=150, label='住所')

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    email = forms.CharField(max_length=150, label='メールアドレス')
    telephone_number = forms.CharField(max_length=150, label='電話番号')
    post_code = forms.CharField(max_length=150, label='郵便番号')
    address = forms.CharField(max_length=150, label='住所')
    
    class Meta:
        model = CustomUser

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.telephone_number = self.cleaned_data['telephone_number']
        user.post_code = self.cleaned_data['post_code']
        user.address = self.cleaned_data['address']
        user.save()
        return user

class StoreForm(forms.ModelForm):   
    class Meta:
        model = Store
        fields = '__all__'

class BookingForm(forms.ModelForm):

    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), label='開始日')
    start_time = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}), label='開始時間')

    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'tel', 'remarks', 'start_date', 'start_time']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')

        # 現在時刻を取得
        now = timezone.localtime(timezone.now())

        # フォームから取得した日付と時間を組み合わせて予約開始時刻を作成
        naive_start = datetime.combine(start_date, start_time)
        start = timezone.make_aware(naive_start, timezone.get_default_timezone())

        # 予約開始時刻が現在時刻より少なくとも2時間後であることを確認
        if start < now + timedelta(hours=2):
            raise ValidationError('予約開始時刻は現在時刻より2時間後でなければなりません。')

        return cleaned_data 
        

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['comment', 'score']

class StoreCreateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'address', 'tel', 'description', 'category', 'image']
