from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.micro import feeds
from replica.contrib.micro.views import pulse as pulseViews
from replica.contrib.micro.views import cms as cmsViews

MICRO_CMS_URLS = [
    url(r'^$', login_required(cmsViews.Index), name="MicroIndex"),
    url(r'^timelines/$', login_required(cmsViews.TimelineEdit), name="TimelineNew"),
    url(r'^timelines/edit/(?P<timelineID>[\w-]+)/$', login_required(cmsViews.TimelineEdit), name = "TimelineEdit"),
    url(r'^timelines/edit/(?P<timelineID>[\w-]+)/delete/$', login_required(cmsViews.TimelineDelete), name = "TimelineDelete"),

    #url(r'^notes/$', login_required(cmsViews.NoteDelete), name = "NoteList"),
    url(r'^notes/edit/(?P<noteID>[\w-]+)/delete/$', login_required(cmsViews.NoteDelete), name = "NoteDelete"),
]

MICRO_PULSE_URLS = [
    url(r'^feeds/public/$', feeds.PublicFeed(), name='Public-RSS'),
    url(r'^feeds/list/$', feeds.TimelinesFeed(), name='Timelines-RSS'),
    url(r'^feeds/list/(?P<timeline_slug>[-\w]+)/$', feeds.TimelineFeed(), name='Timeline-RSS'),

    url(r'^id/(?P<note_id>\d+)/$', pulseViews.SingleNote, name = 'Note'),
    url(r'^(?P<timeline_slug>[-\w]+)/$', pulseViews.NoteListView.as_view(), name = "Timeline"),
    url(r'^$', pulseViews.TimelinesListView.as_view(), name = 'Timelines'),
]
