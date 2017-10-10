from django.contrib import admin
from django.db import models
from .models import Promoted, Collection


class PromotedAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_updated', 'user', 'entry')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'deck', 'pub_date', 'user')
    filter_horizontal = ('entries',)


admin.site.register(Promoted, PromotedAdmin)
admin.site.register(Collection, CollectionAdmin)
