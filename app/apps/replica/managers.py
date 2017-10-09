import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class TopicManager(models.Manager):
    def public(self):
        return super(TopicManager, self).get_queryset().filter(is_public=True)

class EntryManager(models.Manager):
    def posts(self):
        return super(EntryManager, self).get_queryset().exclude(channel__slug='page').exclude(channel__slug='sticky')

    def ideas(self):
        return self.posts().filter(is_active=False)

    def active(self):
        return self.posts().filter(is_active=True)

    def published(self):
        return self.active().filter(pub_date__lte=datetime.datetime.now())

    def upcoming(self):
        return self.active().filter(pub_date__gte=datetime.datetime.now())

    def pages(self):
        return super(EntryManager, self).get_queryset().filter(channel__slug='page')

    def pages_published(self):
        return self.pages().filter(pub_date__lte=datetime.datetime.now()).filter(is_active=True)

    def pages_draft(self):
        return self.pages().filter(pub_date__lte=datetime.datetime.now()).filter(is_active=False)

    def sticky(self):
        return super(EntryManager, self).get_queryset().filter(channel__slug='sticky')

class MediaManager(models.Manager):
    def images(self):
        return super(MediaManager, self).get_queryset().filter(content_type=1)

class CodeManager(models.Manager):
    def partial(self):
        return super(CodeManager, self).get_queryset().filter(type=1)

    def template(self):
        return super(CodeManager, self).get_queryset().filter(type=2)
