from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import routers

from .views import site as siteView
from .views import entry as entryView
from .views import channel as channelView
from .views import topic as topicView

APP_URLS = [
	url(r'^app/$',login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/base.html"))), name="App" ),
	url(r'^app/(?P<path>.*)/$', login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/base.html"))), name="App" ),
]

SITE_URLS = [
	url(r'^$', login_required(siteView.Index), name = "Home"),
	url(r'^site/$', login_required(siteView.SiteSettings), name = "SiteSettings"),
	url(r'^site/users/$', login_required(siteView.UserList.as_view()), name = "UserList"),
	url(r'^site/users/(?P<slug>[\w-]+)/$', login_required(siteView.UserDetail), name = "UserDetail"),
	url(r'^site/users/(?P<slug>[\w-]+)/entries/$', login_required(siteView.UserEntriesList.as_view()), name = "UserEntriesList"),
]

ENTRY_URLS = [
	url(r'^edit/$', login_required(entryView.Editor), name = "Editor"),
	url(r'^edit/entry/(?P<entryID>[\w-]+)/$', login_required(entryView.Editor), name = "EditEntry"),
	url(r'^entries/$', login_required(entryView.EntryList.as_view()), name = "EntryList"),
	url(r'^entries/pages/$', login_required(entryView.PageList.as_view()), name = "PageList"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/$', login_required(entryView.EntryDetail.as_view()), name = "EntryDetails"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/delete/$', login_required(entryView.EntryDelete), name = "EntryDelete"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/draft/(?P<draftID>[\w-]+)/$', login_required(entryView.EntryDraft), name = "EntryDrafts"),
]

CHANNEL_URLS = [
	url(r'^channels/$', login_required(channelView.ChannelList.as_view()), name = "ChannelList"),
	url(r'^edit/channels/(?P<channelID>[\w-]+)/$', login_required(channelView.ChannelEdit), name = "ChannelEdit"),
	url(r'^edit/channels/(?P<channelID>[\w-]+)/delete/$', login_required(channelView.ChannelDelete), name = "ChannelDelete"),
	url(r'^edit/channels/$', login_required(channelView.ChannelEdit), name = "ChannelNew"),
]

TOPIC_URLS = [
	url(r'^topics/$', login_required(topicView.TopicList.as_view()), name = "TopicList"),
	url(r'^edit/topics/(?P<topicID>[\w-]+)/$', login_required(topicView.TopicEdit), name = "TopicEdit"),
	url(r'^edit/topics/(?P<topicID>[\w-]+)/delete/$', login_required(topicView.TopicDelete), name="TopicDelete"),
	url(r'^edit/topics/$', login_required(topicView.TopicEdit), name="TopicNew"),
]

MEDIA_URLS = [

]

urlpatterns = [
	url(r'^beta/', include(APP_URLS)),
	url(r'', include(SITE_URLS)),
	url(r'', include(ENTRY_URLS)),
	url(r'', include(CHANNEL_URLS)),
	url(r'', include(TOPIC_URLS)),
]
