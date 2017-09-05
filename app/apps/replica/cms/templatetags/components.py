from django import template
from django.contrib.admin.models import LogEntry

from replica.pulse.models import Entry, Draft, Topic, Media, Channel
from replica import settings as ReplicaSettings

register = template.Library()

@register.inclusion_tag('replica/cms/templatetags/_header.html', takes_context=True)
def partialHeader():
	request = context['request']
	u = request.user

	return {
		'user_obj':u,
		'SITE_NAME': ReplicaSettings.SITE_NAME,
		'SITE_URL': ReplicaSettings.SITE_URL,
	}
