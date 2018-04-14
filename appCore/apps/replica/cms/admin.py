from __future__ import absolute_import
from django.contrib import admin
from django.db import models

from replica.cms.forms import AdminSiteSettingsForm
from replica.cms.models import *

class PluginAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date_updated')

class SiteSettingsAdmin(admin.ModelAdmin):
    form = AdminSiteSettingsForm
    list_display = ('name', 'domain', 'id')

class MenuPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_updated')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_url', 'position', 'weight')
    list_filter = ('position',)

admin.site.register(Plugin, PluginAdmin)
admin.site.register(MenuPosition, MenuPositionAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
