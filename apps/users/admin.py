from django.contrib import admin

from .models import EmailUser


class EmailUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'type']


admin.site.register(EmailUser, EmailUserAdmin)
