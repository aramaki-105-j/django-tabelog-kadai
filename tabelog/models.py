from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = ((1, 'user'), (2, 'store'),)
    email = models.EmailField(verbose_name='メールアドレス', unique=True)
    first_name = models.CharField(verbose_name='姓', max_length=20)
    last_name = models.CharField(verbose_name='名', max_length=20)
    telephone_number = models.CharField('電話番号', max_length=30, blank=True)
    post_code = models.CharField('郵便番号', max_length=30, blank=True)
    address = models.CharField('住所', max_length=30, blank=True)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_card_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)



    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class Category(models.Model):
    id = models.AutoField('カテゴリーID', primary_key=True)
    name = models.CharField('カテゴリー名', max_length=50)

    def __str__(self):
        return self.name

class Store(models.Model):
    id = models.AutoField('店舗ID', primary_key=True)
    name = models.CharField('店舗名', max_length=100)
    address = models.CharField('住所', max_length=100, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)
    description = models.TextField('説明', default="", blank=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
   
class Booking(models.Model):
    id = models.AutoField('予約ID', primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    first_name = models.CharField('姓', max_length=100, null=True, blank=True)
    last_name = models.CharField('名', max_length=100, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)
    remarks = models.TextField('人数：要望', default="", blank=True)
    start = models.DateTimeField('予約日時', default=timezone.now)
    

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M')
        return f'{self.first_name}{self.last_name} {start}'

class Review(models.Model):
    id = models.AutoField('レビューID', primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name="レビューコメント", blank=False)
    score = models.PositiveSmallIntegerField(verbose_name="レビュースコア", choices=SCORE_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.store)

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent

class Like(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["store", "user"],
                name="like_unique"
            ),
        ]

class Company(models.Model):
    id = models.AutoField('会社ID', primary_key=True)
    name = models.CharField('会社名', max_length=100)
    address = models.CharField('住所', max_length=100, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.company_name