from __future__ import absolute_import
import hashlib
#from urlparse import urlparse
from urllib.parse import urlparse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django import template
from django.contrib.admin.models import LogEntry

from replica.pulse.models import Entry, Draft, Topic, Media, Channel

register = template.Library()

@register.inclusion_tag('replica/dashboard/templatetags/render_ideas.html')
def render_ideas(num, username):
	objects = Entry.objects.ideas().filter(user=username)[:num]
	return { 'objects': objects}

@register.inclusion_tag('replica/dashboard/templatetags/render_posts.html')
def render_upcoming(num, username):
	objects = Entry.objects.upcoming().filter(user=username)[:num]
	return { 'objects': objects, 'color':'blue',}

@register.inclusion_tag('replica/dashboard/templatetags/render_posts.html')
def render_published(num, username):
	objects = Entry.objects.published().filter(user=username)[:num]
	return { 'objects': objects, 'color':'green',}

@register.inclusion_tag('replica/dashboard/templatetags/render_topics.html')
def render_topics(num=5, username=None, show_desc=True):
	if not username:
		objects = Topic.objects.all().order_by('title')[:num]
	else:
		objects = Topic.objects.filter(user=username).order_by('title')[:num]
	return { 'objects': objects, 'color':'gray', 'show_desc': show_desc }

@register.inclusion_tag('replica/dashboard/templatetags/render_media.html')
def render_media(username, num):
	objects = Media.objects.filter(user=username)[:num]
	return { 'objects': objects, 'color':'red',}

@register.inclusion_tag('replica/dashboard/templatetags/month_links_snippet.html')
def render_dashboard_months(username):
	dates = Entry.objects.filter(user=username).dates('pub_date', 'month')
	return { 'dates': dates, }

@register.simple_tag
def render_item_counts(username, count_type=None):
	if count_type == 'topic':
		obj_count = Topic.objects.filter(user=username).count()
	elif count_type == 'published':
		obj_count = Entry.objects.published().filter(user=username).count()
	elif count_type == 'upcoming':
		obj_count = Entry.objects.upcoming().filter(user=username).count()
	elif count_type == 'ideas':
		obj_count = Entry.objects.ideas().filter(user=username).count()
	elif count_type == 'channel':
		obj_count = Channel.objects.filter(user=username).count()
	elif count_type == 'pages':
		obj_count = Entry.objects.pages().filter(user=username).count()
	else:
		obj_count = Entry.objects.filter(user=username).count()
	return obj_count
