from django.contrib import admin
from django.db import models
from .models import Instagram

class InstagramAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'date_updated', 'user',)
    list_filter = ('user',)

admin.site.register(Instagram, InstagramAdmin)
