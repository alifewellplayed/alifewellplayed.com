from __future__ import absolute_import
from django.contrib import admin
from django.db import models

from .forms import AdminEntryForm, AdminSiteSettingsForm
from .models import *

def force_save(modeladmin, request, queryset):
    for item in queryset.iterator():
        item.save()
force_save.short_description = "Save Selected objects"

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_updated', 'user', 'is_public')
    list_filter = ('is_public',)
    prepopulated_fields = {"slug": ("title",)}

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_updated', 'user',)
    list_filter = ('user',)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user',)
    list_filter = ('user',)

class CodeBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description',)
    list_filter = ('user', 'type')

class EntryAdmin(admin.ModelAdmin):
    form = AdminEntryForm
    list_display = ('title', 'pub_date', 'is_active', 'channel', 'user', 'template')
    list_filter = ('is_active', 'channel', 'topic')
    exclude = ('deck_html', 'body_html',)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('topic',)
    list_per_page=250
    actions=[ force_save, ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs['rows'] = 25
        return formfield

class DraftAdmin(admin.ModelAdmin):
    list_display = ('entry', 'title', 'date_updated',)
    list_filter = ('user',)

class SiteSettingsAdmin(admin.ModelAdmin):
    form = AdminSiteSettingsForm
    list_display = ('name', 'domain', 'id')

class EntryLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'entry')

class MenuPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_updated')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_url', 'position', 'weight')
    list_filter = ('position',)

admin.site.register(EntryLink, EntryLinkAdmin)
admin.site.register(CodeBlock, CodeBlockAdmin)
admin.site.register(MenuPosition, MenuPositionAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Draft, DraftAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
