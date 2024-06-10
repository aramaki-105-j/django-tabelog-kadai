from django.contrib import admin
from .models import CustomUser, Store, Booking, Review, Like, Category, Company

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'address')
    search_fields = ('first_name', 'last_name', 'address')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'category')
    search_fields = ('name', 'address')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Company)