from django.contrib import admin

# Register your models here.
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'phone']
    readonly_fields = ['username', 'password', 'phone']

admin.site.register(User, UserAdmin)
