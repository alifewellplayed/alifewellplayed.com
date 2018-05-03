from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.micro import feeds
from replica.contrib.micro.views import pulse as views

app_name="replica.micro"
urlpatterns = [
    url(r'^$', views.TimelinesListView.as_view(), name = 'Timelines'),
    url(r'^feeds/public/$', feeds.PublicFeed(), name='Public-RSS'),
    url(r'^feeds/list/$', feeds.TimelinesFeed(), name='Timelines-RSS'),
    url(r'^feeds/list/(?P<timeline_slug>[-\w]+)/$', feeds.TimelineFeed(), name='Timeline-RSS'),

    url(r'^status/(?P<note_id>[-\w]+)/$', views.SingleNote, name = 'Note'),
    url(r'^(?P<timeline_slug>[-\w]+)/$', views.NoteCreate, name = "Timeline"),

]
