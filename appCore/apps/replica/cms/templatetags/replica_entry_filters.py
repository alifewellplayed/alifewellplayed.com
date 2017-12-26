from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django import template

from replica.pulse.models import Entry, Draft, Topic, Media, Channel, MenuPosition, CodeBlock

register = template.Library()

@register.inclusion_tag('replica/cms/templatetags/entry_topic_filter.html')
def render_entry_topic_filters():
    topics = Topic.objects.all()
    count = topics.count()
    ctx = {
        'object_list': topics,
        'object_count': count,
        'object_title': 'Filter by Topic',
        'object_slug': 'topics',
        'object_empty': 'No Topics created yet.'
    }
    return ctx

@register.inclusion_tag('replica/cms/templatetags/entry_status_filter.html')
def render_entry_status_filters():
    ctx = {
        'object_title': 'Filter by status',
        'object_slug': 'status',
        'object_empty': None
    }
    return ctx
