from django import forms
from allauth.account.forms import SignupForm 
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser, Store, Review, Booking



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

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    #start = forms.SplitDateTimeField(label='予約日時')

    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'tel', 'remarks', 'start'] 
        

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['comment', 'score']