import os
import markdown
import datetime
import uuid
from PIL import Image
from time import strftime
from hashlib import md5
from io import StringIO, BytesIO

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, wordcount
from django.conf import settings
from django.urls import get_script_prefix
from django.utils.encoding import iri_to_uri
from django.contrib.sites.models import Site

from replica import settings as replicaSettings
from replica.pulse.models import Media, Entry, DefaultEntry
from replica.uploads import *
from replica.pulse.utils import create_thumbnail, DefaultUser

# Create custom menus. Useful for themes.
# Example: Footer Menu, Primary Menu, etc.
class MenuPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, default='Untitled')
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_MenuPosition'
        verbose_name = "Menu"
        verbose_name_plural = 'Menus'
        ordering = ('-title',)

    def __unicode__(self):
        return "%s" % (self.title,)

    def __str__(self):
        return self.title

    def menu_count(self):
        total = MenuItem.objects.filter(position=self).count()
        return total

    def save(self, *args, **kwargs):
        super(MenuPosition, self).save(*args, **kwargs)

class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icon = models.SlugField(max_length=replicaSettings.MAX_LENGTH, choices=replicaSettings.ICON_CHOICES, blank=True)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, default='Untitled')
    description = models.CharField(help_text=_("Optional subtitle"), max_length=replicaSettings.MAX_LENGTH, blank=True)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    page = models.ForeignKey(Entry, blank=True, null=True, default=DefaultEntry, on_delete=models.SET_DEFAULT)
    url = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    position = models.ForeignKey(MenuPosition, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_MenuItem'
        verbose_name = "Menu Item"
        verbose_name_plural = 'Menu Items'
        ordering = ('weight',)

    def menu_url(self):
        if self.page:
            return self.page.get_absolute_url()
        elif self.url:
            return self.url
        else:
            return '#'

    def __unicode__(self):
        return "%s" % (self.title,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(MenuItem, self).save(*args, **kwargs)

class SiteSettings(Site):
    is_enabled = models.BooleanField(help_text="Is site enabled?", choices=replicaSettings.IS_SITE_CHOICES, default=True)
    password = models.CharField(blank=True, max_length=128)
    secret_token = models.CharField(max_length=12, blank=True)
    view_settings = models.TextField(default="{}")
    author = models.CharField(max_length=510, blank=True)
    description = models.TextField(help_text="Site Description", blank=True, null=True)
    summary = models.TextField(help_text="Summary", blank=True)
    summary_html = models.TextField(blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    logo = models.ForeignKey(Media, blank=True, null=True, related_name='logo', on_delete=models.SET_NULL)
    featured = models.ForeignKey(Media, help_text="Featured Image", related_name='featured', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'r_SiteSettings'
        verbose_name = "Site Settings"
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.summary_html = markdown.markdown(self.summary)
        super(SiteSettings, self).save(*args, **kwargs)

class Plugin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH)
    is_enabled = models.BooleanField(help_text=_("Check to enable plugin"), choices=replicaSettings.IS_SITE_CHOICES, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_Plugin'
        verbose_name = "Plugin"
        verbose_name_plural = 'Plugins'
        ordering = ('slug',)
