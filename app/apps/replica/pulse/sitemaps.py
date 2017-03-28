import datetime

from django.contrib.sitemaps import Sitemap
from .models import Entry


class PulseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Entry.objects.published()


    def lastmod(self, obj):
        return obj.pub_date
