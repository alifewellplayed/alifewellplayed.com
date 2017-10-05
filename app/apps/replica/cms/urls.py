from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import routers

from .views import site as siteView
from .views import user as userView
from .views import entry as entryView
from .views import channel as channelView
from .views import topic as topicView
from .views import media as mediaView
from .views import templete as templateView

APP_URLS = [
	url(r'^app/$',login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/app.html"))), name="App" ),
	url(r'^app/(?P<path>.*)/$', login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/app.html"))), name="App" ),
]

SITE_URLS = [
	url(r'^$', login_required(siteView.Index), name = "Home"),
	url(r'^site/$', login_required(siteView.Settings), name = "SiteSettings"),
	url(r'^site/menu/$', login_required(siteView.MenuEdit), name = "MenuList"),
	url(r'^site/menu/(?P<menuID>[\w-]+)/$', login_required(siteView.MenuEdit), name = "MenuEdit"),
	url(r'^site/menu/(?P<menuID>[\w-]+)/delete/$', login_required(siteView.MenuDelete), name = "MenuDelete"),
	url(r'^site/menu/(?P<menuID>[\w-]+)/item/$', login_required(siteView.MenuItemEdit), name = "MenuItemNew"),
	url(r'^site/menu/(?P<menuID>[\w-]+)/item/(?P<itemID>[\w-]+)/$', login_required(siteView.MenuItemEdit), name = "MenuItemEdit"),
	url(r'^site/menu/(?P<menuID>[\w-]+)/item/(?P<itemID>[\w-]+)/delete/$', login_required(siteView.MenuItemDelete), name = "MenuItemDelete"),
]

USER_URLS = [
	url(r'^site/users/$', login_required(userView.UserList.as_view()), name = "UserList"),
	url(r'^site/users/create/$', login_required(userView.UserEdit), name = "UserCreate"),
	url(r'^site/users/(?P<userID>[\w-]+)/$', login_required(userView.UserEdit), name = "UserEdit"),
	url(r'^site/users/(?P<userID>[\w-]+)/delete/$', login_required(userView.UserEdit), name = "UserDelete"),
	url(r'^site/users/(?P<userID>[\w-]+)/entries/$', login_required(userView.UserEntriesList.as_view()), name = "UserEntriesList"),
]

TEMPLATE_URLS = [
	url(r'^templates/$', login_required(templateView.EntryTemplateList.as_view()), name = "TemplateList"),
	url(r'^templates/new/$', login_required(templateView.EntryTemplateEdit), name = "TemplateCreate"),
	url(r'^templates/(?P<templateID>[\w-]+)/$', login_required(templateView.EntryTemplateEdit), name = "TemplateEdit"),
	url(r'^templates/(?P<templateID>[\w-]+)/delete/$', login_required(templateView.EntryTemplateDelete), name = "TemplateDelete"),
]

ENTRY_URLS = [
	url(r'^edit/$', login_required(entryView.Editor), name = "Editor"),
	url(r'^edit/entry/(?P<entryID>[\w-]+)/$', login_required(entryView.Editor), name = "EntryEdit"),
	url(r'^entries/$', login_required(entryView.EntryList.as_view()), name = "EntryList"),
	url(r'^entries/pages/$', login_required(entryView.PageList.as_view()), name = "PageList"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/$', login_required(entryView.EntryDetail.as_view()), name = "EntryDetails"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/delete/$', login_required(entryView.EntryDelete), name = "EntryDelete"),
	url(r'^entries/tree/(?P<entryID>[\w-]+)/draft/(?P<draftID>[\w-]+)/$', login_required(entryView.EntryDraft), name = "EntryDrafts"),
]

CHANNEL_URLS = [
	url(r'^channels/$', login_required(channelView.ChannelEdit), name = "ChannelList"),
	url(r'^channels/edit/(?P<channelID>[\w-]+)/$', login_required(channelView.ChannelEdit), name = "ChannelEdit"),
	url(r'^channels/edit/(?P<channelID>[\w-]+)/delete/$', login_required(channelView.ChannelDelete), name = "ChannelDelete"),
]

TOPIC_URLS = [
	url(r'^topics/$', login_required(topicView.TopicEdit), name = "TopicList"),
	url(r'^topics/edit/(?P<topicID>[\w-]+)/$', login_required(topicView.TopicEdit), name = "TopicEdit"),
	url(r'^topics/edit/(?P<topicID>[\w-]+)/delete/$', login_required(topicView.TopicDelete), name="TopicDelete"),
]

MEDIA_URLS = [
	url(r'^media/$', login_required(mediaView.MediaList.as_view()), name = "MediaList"),
	url(r'^edit/media/$', login_required(mediaView.MediaEdit), name = "MediaNew"),
	url(r'^edit/media/(?P<mediaID>[\w-]+)/$', login_required(mediaView.MediaEdit), name = "MediaEdit"),
	url(r'^edit/media/(?P<mediaID>[\w-]+)/delete/$', login_required(mediaView.MediaDelete), name="MediaDelete"),
]

urlpatterns = [
	url(r'^beta/', include(APP_URLS)),
	url(r'', include(ENTRY_URLS)),
	url(r'', include(SITE_URLS)),
	url(r'', include(USER_URLS)),
	url(r'', include(CHANNEL_URLS)),
	url(r'', include(TOPIC_URLS)),
	url(r'', include(MEDIA_URLS)),

]
