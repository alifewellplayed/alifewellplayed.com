from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.redirection.views import cms as views

app_name="replica.redirection"
urlpatterns = [
    url(r'^urls/$', views.SiteLinkListView.as_view(), name = 'SiteLinkList'),
    url(r'^urls/new/$', login_required(views.SiteLinkEdit), name="SiteLinkNew"),
    url(r'^urls/edit/(?P<promotedID>[\w-]+)/$', login_required(views.SiteLinkEdit), name = "SiteLinkEdit"),
    url(r'^urls/edit/(?P<promotedID>[\w-]+)/delete/$', login_required(views.SiteLinkDelete), name = "SiteLinkDelete"),
    url(r'^blocked/$', views.BlockedIpListView.as_view(), name = 'BlockedIpList'),
    url(r'^blocked/new/$', login_required(views.BlockedIpEdit), name="BlockedIpNew"),
    url(r'^blocked/edit/(?P<promotedID>[\w-]+)/$', login_required(views.BlockedIpEdit), name = "BlockedIpEdit"),
    url(r'^blocked/edit/(?P<promotedID>[\w-]+)/delete/$', login_required(views.BlockedIpDelete), name = "BlockedIpDelete"),
]
