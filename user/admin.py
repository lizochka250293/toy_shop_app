from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
# Register your models here.
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'phone']
    readonly_fields = ['username', 'password']

admin.site.register(User, UserAdmin)
