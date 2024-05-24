from django.contrib import admin
from .models import CustomUser, Store, Booking, Review

admin.site.register(CustomUser)
admin.site.register(Booking)
admin.site.register(Store)
admin.site.register(Review)