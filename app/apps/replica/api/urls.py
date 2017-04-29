from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers
from .views import *

#contrib
from replica.contrib.micro import api as micro

router = routers.DefaultRouter()
#router.register("search", views.ResultSearchView, base_name="search")

pulse_api = [
    url(r'^dashboard/$', pulse.DashboardView.as_view(), name='Dashboard'),
    url(r'^topics/$', pulse.TopicList.as_view(), name='topic-list'),
    url(r'^topics/(?P<slug>[0-9a-zA-Z_-]+)/$', pulse.TopicDetail.as_view(), name='topic-detail'),
    url(r'^topics/(?P<slug>[0-9a-zA-Z_-]+)/entries/$', pulse.TopicEntryList.as_view(), name='topic-entries-list'),
    url(r'^channels/$', pulse.ChannelList.as_view(), name='channel-list'),
    url(r'^channels/(?P<slug>[0-9a-zA-Z_-]+)/$', pulse.ChannelDetail.as_view(), name='channel-detail'),
    url(r'^channels/(?P<slug>[0-9a-zA-Z_-]+)/entries/$', pulse.ChannelEntryList.as_view(), name='channel-entries-list'),
    url(r'^entries/$', pulse.EntryList.as_view(), name='entry-list'),
    url(r'^entries/ideas/$', pulse.EntryDraftList.as_view(), name='entry-drafts-list'),
    url(r'^entries/upcoming/$', pulse.EntryUpcomingList.as_view(), name='entry-upcoming-list'),
    url(r'^entries/new/$', pulse.EntryCreate.as_view(), name='entry-new'),
    url(r'^entries/detailed/(?P<id>[0-9a-zA-Z_-]+)/$', pulse.EntryDetail.as_view(), name='entry-detail'),
    url(r'^pages/$', pulse.PageList.as_view(), name='page-list'),
    url(r'^pages/(?P<id>[0-9a-zA-Z_-]+)/$', pulse.PageDetail.as_view(), name='page-detail'),
]

micro_api = [
    url(r'^timelines/(?P<slug>[0-9a-zA-Z_-]+)/$', micro.TimelineDetail.as_view(), name='micro-timeline-detail'),
    url(r'^timelines/(?P<slug>[0-9a-zA-Z_-]+)/list/$', micro.TimelineNoteList.as_view(), name='micro-timeline-note-list'),
    url(r'^timelines/$', micro.TimelineList.as_view(), name='micro-timeline-list'),
    url(r'^create/note/$', micro.NoteCreate.as_view(), name='micro-note-new'),
    url(r'^create/timeline/$', micro.TimelineCreate.as_view(), name='micro-timeline-new'),
    url(r'^status/(?P<id>[0-9a-zA-Z_-]+)/$', micro.NoteDetail.as_view(), name='micro-note-detail'),
    url(r'^$', micro.NoteList.as_view(), name='micro-note-list'),
]

user_api = [
    #Micro endpoints
    url(r'^user/(?P<username>[0-9a-zA-Z_-]+)/timelines/$', micro.UserTimelineList.as_view(), name='user-timeline-list'),
    url(r'^user/(?P<username>[0-9a-zA-Z_-]+)/notes/$', micro.UserNoteList.as_view(), name='user-note-list'),

    #Default endpoints
    url(r'^user/(?P<username>[0-9a-zA-Z_-]+)/$', users.UserDetail.as_view(), name='user-detail'),
    url(r'^list/$', users.UserList.as_view(), name='user-list'),

]

current_api = [
    url(r'^$', pulse.CurrentSite.as_view(), name='site-current'),
    url(r'^stats/$', pulse.CurrentSiteStats.as_view(), name='site-current-stats'),
    url(r'^user/$', users.CurrentUser.as_view(), name='site-current-user'),
    url(r'^settings/$', pulse.CurrentSiteSettings.as_view(), name='site-current-settings'),
]

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(pulse_api)),
    url(r'current/', include(current_api)),
    url(r'users/', include(user_api)),
    url(r'micro/', include(micro_api)),
]
