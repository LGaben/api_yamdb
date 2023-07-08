from django.contrib import admin

from .models import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'role',
                    'bio',
                    'first_name',
                    'last_name')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserProfileAdmin)