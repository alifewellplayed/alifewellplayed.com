import logging
import datetime
import markdown
import uuid
from hashlib import md5

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class NoteManager(models.Manager):

    def published(self):
        return self.public().filter(pub_date__lte=datetime.datetime.now())

    def public(self):
        return super(NoteManager, self).get_query_set().filter(is_private=False)


class Timeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    deck = models.TextField(_('deck'), blank=True)
    deck_html = models.TextField(blank=True)
    is_public = models.BooleanField(help_text=_("Should be checked you want anyone to see"), default=True)
    rev_order = models.BooleanField(help_text=_("Reverse order of list displayed? (Newest on top)"), default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='timelines')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'r_Timeline'
        verbose_name_plural = 'Timelines'
        ordering = ('-date_created',)
        get_latest_by = 'date_created'
        unique_together = (('slug','user'),)

    def items(self):
        return Note.objects.filter(timeline=self)

    def item_count(self):
        item_counts = Note.objects.filter(timeline=self).count()
        return item_counts

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.deck_html = markdown.markdown(self.deck)
        super(Timeline, self).save(*args, **kwargs)

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    body_html = models.TextField(editable=False)
    pub_date = models.DateTimeField(verbose_name=_("Date posted"), auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(help_text=_("Should be checked if no one else should see this."), default=False)
    timeline = models.ForeignKey(Timeline, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes')
    objects = NoteManager()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'r_Note'
        verbose_name_plural = 'Notes'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def save(self, *args, **kwargs):
        self.body_html = markdown.markdown(self.body)
        super(Note, self).save(*args, **kwargs)
