from django.conf.urls import *
from . import views

urlpatterns = [
	url(r'^urls/$', views.LinkListView.as_view(), name = 'link_list'),
	url(r'^blocked/$', views.BlockedListView.as_view(), name = 'blocked_list'),
	url(r'^(?P<slug>[-\w]+)/$', views.LinkRedirect, name = 'link_redirect'),
]
