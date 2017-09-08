import os
from PIL import Image
import markdown
import datetime
from time import strftime
from hashlib import md5
import uuid
from io import StringIO

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, wordcount
from django.conf import settings
from django.core.urlresolvers import get_script_prefix
from django.contrib.sites.models import Site

from replica import settings as replicaSettings
from replica.pulse.models import Entry, Media
from replica.pulse.managers import TopicManager, EntryManager, MediaManager

class Promoted(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    deck = models.TextField(max_length=1020, blank=True)
    deck_html = models.TextField(blank=True, editable=False)
    pub_date = models.DateTimeField(verbose_name=_("Publication date"), default=datetime.datetime.now, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='promoted_entries')
    image = models.ForeignKey(Media, blank=True, null=True)
    entry = models.ForeignKey(Entry)

    class Meta:
        db_table = 'r_Promoted'
        verbose_name_plural = 'Promoted Entries'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return "%s" % (self.title,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.deck:
            self.deck_html = markdown.markdown(self.deck)
        super(Promoted, self).save(*args, **kwargs)


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='collections')
    image = models.ForeignKey(Media, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    deck = models.TextField(max_length=1020, blank=True)
    deck_html = models.TextField(blank=True, editable=False)
    pub_date = models.DateTimeField(verbose_name=_("Publication date"), default=datetime.datetime.now, blank=True)
    entries = models.ManyToManyField(Entry, db_table='r_Collection_Entries', blank=True)

    class Meta:
        db_table = 'r_Collection'
        verbose_name_plural = 'Collections'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return "%s" % (self.title,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.deck:
            self.deck_html = markdown.markdown(self.deck)
        super(Collection, self).save(*args, **kwargs)
