from django.contrib import admin

from chat.models import ChatDialog, ChatMessage


class DialogAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'is_active']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'dialog', 'create_at']
    search_fields = ['user']


admin.site.register(ChatDialog, DialogAdmin)
admin.site.register(ChatMessage, MessageAdmin)
