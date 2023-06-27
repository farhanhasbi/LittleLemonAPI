from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Category, MenuItem, Cart, Order, OrderItem

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'get_user_groups')
    ordering = ('id',)

    def get_user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_user_groups.short_description = 'Groups'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register([Category, MenuItem, Cart, Order, OrderItem])