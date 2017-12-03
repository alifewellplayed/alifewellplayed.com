from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.micro import feeds
from replica.contrib.micro.views import cms as views

app_name="replica.micro"
urlpatterns = [
    url(r'^$', login_required(views.Index), name="MicroIndex"),
    url(r'^timelines/$', login_required(views.TimelineEdit), name="TimelineNew"),
    url(r'^timelines/edit/(?P<timelineID>[\w-]+)/$', login_required(views.TimelineEdit), name = "TimelineEdit"),
    url(r'^timelines/edit/(?P<timelineID>[\w-]+)/delete/$', login_required(views.TimelineDelete), name = "TimelineDelete"),

    #url(r'^notes/$', login_required(views.NoteDelete), name = "NoteList"),
    url(r'^notes/edit/(?P<noteID>[\w-]+)/delete/$', login_required(views.NoteDelete), name = "NoteDelete"),
]
