from django import template
from django.contrib.admin.models import LogEntry

from replica.pulse.models import Entry, Draft, Topic, Media, Channel
from replica import settings as ReplicaSettings

register = template.Library()

@register.inclusion_tag('replica/cms/components/_header.html', takes_context=True)
def componentHeader(context, user=None):
	request = context['request']
	u = request.user
	return {'user_obj':u, 'request':request }

@register.inclusion_tag('replica/dashboard/templatetags/month_links_snippet.html')
def render_dashboard_months(username):
	dates = Entry.objects.filter(user=username).dates('pub_date', 'month')
	return { 'dates': dates, }

@register.simple_tag
def render_counts(obj_type):
	if obj_type == 'topic':
		obj_count = Topic.objects.count()
	elif obj_type == 'published':
		obj_count = Entry.objects.published().count()
	elif obj_type == 'upcoming':
		obj_count = Entry.objects.upcoming().count()
	elif obj_type == 'idea':
		obj_count = Entry.objects.ideas().count()
	elif obj_type == 'channel':
		obj_count = Channel.objects.all().count()
	elif obj_type == 'media':
		obj_count = Media.objects.all().count()
	elif obj_type == 'page':
		obj_count = Entry.objects.pages().count()
	elif obj_type == 'entry':
		obj_count = Entry.objects.all().count()
	else:
		obj_count = '0'
	return obj_count
