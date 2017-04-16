import markdown
import bleach
import uuid

from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from coreExtend.models import Account
from replica.pulse.utils import guid_generator
from .managers import BlockedManager

BLOCKED_IPS_LIST = 'Pithy:blocked-ips'

class SiteLink(models.Model):
    id = models.UUIDField(primary_key=True, default=guid_generator(length=12), editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    link = models.URLField(max_length=512)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=512, blank=True, unique=True)
    note = models.TextField(_('body'), blank=True)
    note_html = models.TextField(blank=True)

    class Meta:
        db_table = 'redirect_Link'
        ordering = ("-date_created",)
        verbose_name = "Link"
        verbose_name_plural = 'Links'

    def get_absolute_url(self):
        if self.slug:
            return self.slug
        else:
            return self.id

    def __unicode__(self):
        return self.link

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if self.note:
            self.note_html = bleach.clean(markdown.markdown(smart_text(self.note)))
        super(SiteLink, self).save(*args, **kwargs)

class ClickLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.ForeignKey(SiteLink, null=True)
    referer = models.CharField(max_length=512, null=True)
    user_agent = models.CharField(max_length=1024, null=True)
    ip_addr = models.GenericIPAddressField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'redirect_Click'
        ordering = ("-date_created",)
        verbose_name = "Click"
        verbose_name_plural = 'Clicks'

    def __str__(self):
        return self.ip_addr

    def __unicode__(self):
        return self.ip_addr

    def store(self, request):
        ip_addr = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT','')
        if ip_addr in BlockedIp.objects.get_ips():
            return None
        self.referer = request.META.get('HTTP_REFERER','')
        self.user_agent = user_agent
        self.ip_addr = ip_addr
        self.save()

class BlockedIp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=True)
    ip_addr = models.GenericIPAddressField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = BlockedManager()

    class Meta:
        db_table = 'redirect_Blocked'
        ordering = ("-date_updated",)
        verbose_name = "Blocked IP"
        verbose_name_plural = 'Blocked IPs'

    def __str__(self):
        return self.ip_addr

    def __unicode__(self):
        return self.ip_addr

    def save(self, *args, **kwargs):
        cache.delete(BLOCKED_IPS_LIST)
        super(BlockedIp, self).save(*args, **kwargs)
