from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django import template

from replica.pulse.models import Entry, Draft, Topic, Media, Channel, MenuPosition
from replica.contrib.publisher.models import Promoted, Collection

register = template.Library()

@register.inclusion_tag('replica/cms/templatetags/promoted_card.html')
def render_promoted_card(format_string=None):
    try:
        if format_string:
            promoted = Promoted.objects.get(slug=format_string)
        else:
            promoted = Promoted.objects.latest('pub_date')
        return { 'obj': promoted }
    except ObjectDoesNotExist:
        return ''

@register.inclusion_tag('replica/cms/templatetags/lists_card.html')
def render_ideas_card(num=9999, username=None):
    if not username:
        entries = Entry.objects.ideas()[:num]
    else:
        entries = Entry.objects.ideas().filter(user=username)[:num]
    count = entries.count()
    ctx = {
        'object_list': entries,
        'object_count': count,
        'object_title': 'Ideas',
        'object_slug': 'ideas',
        'object_empty': 'No ideas saved.'
    }
    return ctx

@register.inclusion_tag('replica/cms/templatetags/lists_card.html')
def render_published_card(num=9999, username=None, title=None):
    if not username:
        entries = Entry.objects.published()[:num]
    else:
        entries = Entry.objects.published().filter(user=username)[:num]
    count = entries.count()
    ctx = {
        'object_list': entries,
        'object_count': count,
        'object_title': 'Recently Published',
        'object_slug': 'published',
        'object_empty': 'No entries published yet!'
    }
    return ctx

@register.inclusion_tag('replica/cms/templatetags/topics_card.html')
def render_topics_card(num=25, username=None, title=None, show_desc=True):
    if not username:
        topics = Topic.objects.all().order_by('title')[:num]
    else:
        topics = Topic.objects.filter(user=username).order_by('title')[:num]
    count = topics.count()
    ctx = {
        'object_list': topics,
        'object_count': count,
        'object_title': 'Topics',
        'object_slug': 'topics',
        'show_desc': show_desc,
        'object_empty': 'No topics created yet!'
    }
    return ctx

@register.inclusion_tag('replica/cms/templatetags/channels_card.html')
def render_channel_card(num=100, username=None, show_new_btn=True, show_all=False):
    if not username:
        channel = Channel.objects.all().order_by('title')[:num]
    else:
        channel = Channel.objects.filter(user=username).order_by('title')[:num]
    count = channel.count()
    ctx = {
        'object_list': channel,
        'object_count': count,
        'object_title': 'Channels',
        'object_slug': 'channel',
        'show_new_btn': show_new_btn,
        'show_all': show_all,
        'object_empty': 'No channels created yet!'
    }
    return ctx

@register.inclusion_tag('replica/cms/templatetags/sticky_card.html')
def render_sticky_card(num=9999, username=None, title=None):
    if not username:
        entries = Entry.objects.sticky()[:num]
    else:
        entries = Entry.objects.sticky().filter(user=username)[:num]
    count = entries.count()
    ctx = {
        'object_list': entries,
        'object_count': count,
        'object_title': 'Stickied links',
        'object_slug': 'stickied',
        'object_empty': 'No stickied posts.'
    }
    return ctx


@register.inclusion_tag('replica/cms/templatetags/menu_card.html')
def render_menu_card(num=9999):
    menu = MenuPosition.objects.all()[:num]
    count = menu.count()
    ctx = {
        'object_list': menu,
        'object_count': count,
        'object_title': 'Menus',
        'object_slug': 'menu',
        'object_empty': 'No menus.'
    }
    return ctx
