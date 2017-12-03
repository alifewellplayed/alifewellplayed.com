from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.micro import feeds
from replica.contrib.micro.views import pulse as views

app_name="replica.micro"
urlpatterns = [
    url(r'^feeds/public/$', feeds.PublicFeed(), name='Public-RSS'),
    url(r'^feeds/list/$', feeds.TimelinesFeed(), name='Timelines-RSS'),
    url(r'^feeds/list/(?P<timeline_slug>[-\w]+)/$', feeds.TimelineFeed(), name='Timeline-RSS'),
    url(r'^id/(?P<note_id>\d+)/$', views.SingleNote, name = 'Note'),
    url(r'^(?P<timeline_slug>[-\w]+)/$', views.NoteListView.as_view(), name = "Timeline"),
    url(r'^$', views.TimelinesListView.as_view(), name = 'Timelines'),
]
