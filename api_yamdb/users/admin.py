from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'bio')
    search_fields = ('username', 'role')
    list_filter = ('username', 'role')
    empty_value_display = '-пусто-'
