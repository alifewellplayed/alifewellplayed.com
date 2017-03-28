from __future__ import absolute_import
from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views
from . import feeds

urlpatterns = [

    #Blog
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<slug>[\w-]+)/$', cache_page(900)(views.EntryDetail), name="entry_detail"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', cache_page(900)(views.DayArchiveView.as_view(template_name='replica/pulse/entry_archive_day.html',)), name="entry_day"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', cache_page(900)(views.MonthArchiveView.as_view(template_name='replica/pulse/entry_archive_month.html',)), name="entry_month"),
    url(r'^(?P<year>\d{4})/$', cache_page(900)(views.YearArchiveView.as_view(template_name='replica/pulse/entry_archive_year.html',)), name="entry_year"),
    url(r'^$', views.ArchiveIndexView.as_view(template_name='replica/pulse/entry_archive.html',), name="Index"),

    #Archive
    url(r'^archive/$', TemplateView.as_view(template_name="replica/pulse/archive.html"), name="Archive"),

    #RSS Feeds
    url(r'^feeds/$', TemplateView.as_view(template_name="replica/pulse/feeds.html"), name="Feeds"),
    url(r'^feeds/all/$', feeds.RSSFeed(), name='KitchenSink-RSS'),

    #Topics
    url(r'^topics/$', views.TopicsList.as_view(), name = "Topics"),
    url(r'^topics/(?P<topic_slug>[\w-]+)/$', views.EntriesForTopic.as_view(), name = "EntriesByTopic"),
    url(r'^topics/(?P<topic_slug>[\w-]+)/(?P<guid>[\w-]+)/$', views.TopicEntry, name = "TopicEntry"),

    #Micro
    url(r'^notes/', include('replica.contrib.micro.urls', namespace='Micro')),

    #Pages
    #url(r'^(?P<url>.*)$', views.EntryPage, name='Page'),

]
