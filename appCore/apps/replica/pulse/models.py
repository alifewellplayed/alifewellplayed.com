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
from replica.uploads import *
from replica.managers import TopicManager, EntryManager, MediaManager, CodeManager
from replica.pulse.utils import create_thumbnail, unique_slugify
from coreExtend.models import Account

def DefaultUser():
    user = Account.objects.first()
    if user:
        return user.id
    else:
        return "1"

class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.PositiveSmallIntegerField(choices=replicaSettings.MEDIA_TYPE_CHOICES, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, blank=True, editable=False)
    caption = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    content = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(help_text="Support for PNG, JPG, GIF only", upload_to=upload_media, blank=True, max_length=replicaSettings.MAX_LENGTH)
    thumbnail_small = models.ImageField(upload_to=upload_media_sm, blank=True, max_length=replicaSettings.MAX_LENGTH)
    thumbnail_medium = models.ImageField(upload_to=upload_media_md, blank=True, max_length=replicaSettings.MAX_LENGTH)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='media', on_delete=models.SET_DEFAULT, default=DefaultUser)
    objects = MediaManager()

    class Meta:
        db_table = 'r_Media'
        verbose_name_plural = 'Media'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.content_type == 2:
            return self.url
        elif self.content_type in (1,3):
            return self.image.url
        else:
            return self.content

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.image and self.content_type==1:
            image_name = self.image.name
            try:
                content_type = self.image.file.content_type
            except:
                # No file uploaded, try to guess content_type
                if self.image.name.endswith((".jpg", ".jpeg")):
                    content_type = 'image/jpeg'
                elif self.image.name.endswith(".png"):
                    content_type = 'image/png'
                elif self.image.name.endswith(".gif"):
                    content_type = 'image/gif'
            with Image.open(BytesIO(self.image.read())) as img:
                sm_filename, sm_image = create_thumbnail(image_name, img, content_type, replicaSettings.THUMBNAIL_SMALL, replicaSettings.THUMBNAIL_SMALL)
                self.thumbnail_small.save(sm_filename, sm_image, save=False)
                md_filename, md_image = create_thumbnail(image_name, img, content_type, replicaSettings.THUMBNAIL_LARGE, replicaSettings.THUMBNAIL_LARGE)
                self.thumbnail_medium.save(md_filename, md_image, save=False)
        super(Media, self).save(*args, **kwargs)

class CodeBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, unique=True)
    description = models.TextField(_('description'), blank=True)
    type = models.IntegerField(choices=replicaSettings.CODE_TYPE_CHOICES, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='templates', on_delete=models.SET_DEFAULT, default=DefaultUser)
    css_upload = models.FileField(upload_to=upload_css, blank=True)
    template_html = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    context = models.TextField(_('Context'), blank=True, default="{}")
    objects = CodeManager()

    class Meta:
        db_table = 'r_CodeBlock'
        verbose_name = _('HTML Template')
        verbose_name_plural = 'HTML Templates'
        ordering = ('-date_updated',)
        get_latest_by = 'date_updated'

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH)
    description = models.TextField(max_length=1020, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='topics', on_delete=models.SET_DEFAULT, default=DefaultUser)
    is_public = models.BooleanField(help_text=_("Can everyone see this Topic?"), choices=replicaSettings.IS_PUBLIC_CHOICES, default=True)
    image = models.ForeignKey(Media, blank=True, null=True, on_delete=models.SET_NULL)
    objects = TopicManager()

    class Meta:
        db_table = 'r_Topic'
        verbose_name_plural = 'topics'
        ordering = ['-title']
        get_latest_by = 'title'

    def __unicode__(self):
        return "%s" % (self.title,)

    def __str__(self):
        return self.title

    def entry_count(self):
        total = Entry.objects.filter(topic=self).count()
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='channels', on_delete=models.SET_DEFAULT, default=DefaultUser)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_Channel'
        verbose_name_plural = 'Channels'
        ordering = ('-title',)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def entry_count(self):
        total = Entry.objects.filter(channel=self).count()
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(Channel, self).save(*args, **kwargs)

def DefaultChannel():
    channel = Channel.objects.filter(slug='post').first()
    if channel:
        return channel.id
    else:
        return "927586a4-3258-4aff-a22f-0136c6e9e503"

class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, unique_for_date='pub_date')
    url = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='entries', on_delete=models.SET_DEFAULT, default=DefaultUser)
    topic = models.ManyToManyField(Topic, db_table='r_Entry_Topics', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(verbose_name=_("Publication date"), default=datetime.datetime.now, blank=True)
    is_active = models.BooleanField(help_text=_("This should be checked for live entries"), choices=replicaSettings.IS_ACTIVE_CHOICES, default=False)
    channel = models.ForeignKey(Channel, verbose_name=_("Entry Type"), default=DefaultChannel, on_delete=models.SET_DEFAULT)
    content_format = models.CharField(choices=replicaSettings.CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
    deck = models.TextField(_('deck'), blank=True)
    deck_html = models.TextField(blank=True)
    body = models.TextField(_('body'), blank=True, null=True)
    body_html = models.TextField(blank=True)
    featured_image = models.ForeignKey(Media, blank=True, null=True, on_delete=models.SET_DEFAULT, default=DefaultUser)
    template = models.ForeignKey(CodeBlock, blank=True, null=True, on_delete=models.SET_DEFAULT, default=DefaultUser)
    objects = EntryManager()

    class Meta:
        db_table = 'r_Entry'
        verbose_name_plural = 'entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def Create_Draft(self):
        DraftInstance = Draft(
            entry=self,
            title=self.title,
            slug=self.slug,
            user=self.user,
            deck=self.deck,
            deck_html=self.deck_html,
            body=self.body,
            body_html=self.body_html,
            content_format=self.content_format
        )
        DraftInstance.save()
        return DraftInstance

    def get_absolute_url(self):
        if self.channel.slug == 'page':
            return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
        else:
            return "/%s/%s/" % (self.pub_date.strftime("%Y/%m").lower(), self.slug)

    def is_published(self):
        return self.is_active and self.pub_date <= datetime.datetime.now()
        is_published.boolean = True

    def total_words(self):
        words = wordcount(self.body)
        return words

    def save(self, *args, **kwargs):
        if self.pk:
            self.Create_Draft()
        if self.content_format == u'markdown':
            self.deck_html = markdown.markdown(self.deck)
            self.body_html = markdown.markdown(self.body)
        else:
            self.body_html = self.body
            self.deck_html = self.deck
        if self.title:
            unique_slugify(self, self.title)
        else:
            self.slug = self.id
        super(Entry, self).save(*args, **kwargs)

def DefaultEntry():
    entry = Entry.objects.filter(channel__slug='page').first()
    return entry.id

class Draft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, blank=True)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH, unique_for_date='pub_date')
    channel = models.ForeignKey(Channel, verbose_name=_("Entry Type"), default=DefaultChannel, on_delete=models.SET_DEFAULT)
    content_format = models.CharField(choices=replicaSettings.CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
    deck = models.TextField(_('summary'), blank=True)
    deck_html = models.TextField(blank=True, editable=False)
    body = models.TextField(_('body'), blank=True)
    body_html = models.TextField(blank=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='drafts', on_delete=models.SET_DEFAULT, default=DefaultUser)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_Draft'
        verbose_name_plural = 'drafts'
        ordering = ('-id',)
        get_latest_by = 'date_updated'

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.id

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.id

    def save(self, *args, **kwargs):
        if self.content_format == u'markdown':
            self.deck_html = markdown.markdown(self.deck)
            self.body_html = markdown.markdown(self.body)
        else:
            self.deck_html = self.deck
            self.body_html = self.body
        super(Draft, self).save(*args, **kwargs)

# Optional links for entries. Useful for footer notes or additional reading.
class EntryLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry = models.ForeignKey(Entry, on_delete=models.SET_DEFAULT, default=DefaultEntry)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=DefaultUser)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    url = models.URLField(max_length=replicaSettings.MAX_LENGTH)
    title = models.CharField(max_length=replicaSettings.MAX_LENGTH, default='Untitled')
    deck = models.TextField(_('summary'), blank=True)

    class Meta:
        db_table = 'r_EntryLink'
        verbose_name = "Entry Link"
        verbose_name_plural = 'Entry Links'
        ordering = ('-title',)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(EntryLink, self).save(*args, **kwargs)

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
