from __future__ import absolute_import

from django.conf import settings
from django.contrib.syndication.views import Feed

from replica.pulse.models import Entry

class RSSFeed(Feed):
    title = settings.SITE_NAME
    link = settings.SITE_URL
    description = settings.SITE_DESC

    def items(self):
        return Entry.objects.published()[:20]

    def item_pubdate(self, item):
        return item.pub_date
