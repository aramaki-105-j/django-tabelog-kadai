from django.contrib import admin
from .models import CustomUser, Store, Booking, Review, Like

admin.site.register(CustomUser)
admin.site.register(Booking)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Like)