from __future__ import absolute_import

from django.contrib import admin
from .models import Timeline, Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ("timeline", "pub_date", "is_private")
    list_filter = ('timeline', 'user',)
    exclude = ('body_html',)
    raw_id_fields = ('user',)
    list_per_page = 500

class TimelineAdmin(admin.ModelAdmin):
    list_filter = ('is_public', 'user',)
    exclude = ('deck_html',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Timeline, TimelineAdmin)
admin.site.register(Note, NoteAdmin)
