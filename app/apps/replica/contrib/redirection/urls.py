from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.redirection.views import pulse as pulseViews
from replica.contrib.redirection.views import cms as cmsViews

REDIRECTION_PULSE_URLS = [
	url(r'^(?P<slug>[-\w]+)/$', pulseViews.LinkRedirect, name = 'link_redirect'),
]

REDIRECTION_CMS_URLS = [
	url(r'^urls/$', cmsViews.SiteLinkListView.as_view(), name = 'SiteLinkList'),
	url(r'^urls/new/$', login_required(cmsViews.SiteLinkEdit), name="SiteLinkNew"),
    url(r'^urls/edit/(?P<promotedID>[\w-]+)/$', login_required(cmsViews.SiteLinkEdit), name = "SiteLinkEdit"),
    url(r'^urls/edit/(?P<promotedID>[\w-]+)/delete/$', login_required(cmsViews.SiteLinkDelete), name = "SiteLinkDelete"),
	url(r'^blocked/$', cmsViews.BlockedIpListView.as_view(), name = 'BlockedIpList'),
	url(r'^blocked/new/$', login_required(cmsViews.BlockedIpEdit), name="BlockedIpNew"),
    url(r'^blocked/edit/(?P<promotedID>[\w-]+)/$', login_required(cmsViews.BlockedIpEdit), name = "BlockedIpEdit"),
    url(r'^blocked/edit/(?P<promotedID>[\w-]+)/delete/$', login_required(cmsViews.BlockedIpDelete), name = "BlockedIpDelete"),
]
