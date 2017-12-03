from __future__ import absolute_import
from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views
from . import feeds

app_name="replica.pulse"
urlpatterns = [

    #Blog
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<slug>[\w-]+)/$', cache_page(900)(views.EntryDetail), name="entry_detail"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', cache_page(900)(views.DayArchiveView.as_view()), name="entry_day"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', cache_page(900)(views.MonthArchiveView.as_view()), name="entry_month"),
    url(r'^(?P<year>\d{4})/$', cache_page(900)(views.YearArchiveView.as_view()), name="entry_year"),
    url(r'^$', views.IndexView.as_view(), name="Index"),

    #Archive
    url(r'^archive/$', views.ArchiveView.as_view(), name="Archive"),

    #RSS Feeds
    url(r'^feeds/$', TemplateView.as_view(template_name="replica/pulse/feeds.html"), name="Feeds"),
    url(r'^feeds/all/$', feeds.RSSFeed(), name='KitchenSink-RSS'),

    #Topics
    url(r'^topics/$', views.TopicsList.as_view(), name = "Topics"),
    url(r'^topics/(?P<topic_slug>[\w-]+)/$', views.EntriesForTopic.as_view(), name = "EntriesByTopic"),
    url(r'^topics/(?P<topic_slug>[\w-]+)/(?P<guid>[\w-]+)/$', views.TopicEntry, name = "TopicEntry"),

    #Pages
    url(r'^(?P<url>.*/)$', views.EntryPage, name='Page'),

]
