from __future__ import absolute_import

from django.conf.urls import *
from . import views
from . import feeds

urlpatterns = [
    url(r'^feeds/public/$', feeds.PublicFeed(), name='Public-RSS'),
    url(r'^feeds/list/$', feeds.TimelinesFeed(), name='Timelines-RSS'),
    url(r'^feeds/list/(?P<timeline_slug>[-\w]+)/$', feeds.TimelineFeed(), name='Timeline-RSS'),
    url(r'^id/(?P<note_id>\d+)/$', views.SingleNote, name = 'Note'),
    url(r'^(?P<timeline_slug>[-\w]+)/$', views.NoteListView.as_view(), name = "Timeline"),
    url(r'^$', views.TimelinesListView.as_view(), name = 'Timelines'),
]
