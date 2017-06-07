from __future__ import absolute_import
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django import template

from coreExtend.models import Account
from replica.contrib.publisher.models import Promoted, Collection
from replica.pulse.models import Entry

register = template.Library()

@register.simple_tag()
def promoted_image(format_string=None):
    try:
        if format_string:
            promoted = Promoted.objects.get(slug=format_string)
        else:
            promoted = Promoted.objects.latest('pub_date')
        return promoted.image.image.url
    except ObjectDoesNotExist:
        return ''

@register.inclusion_tag('replica/contrib/publisher/templatetags/render_promoted_block.html')
def render_promoted_heading(format_string=None):
    try:
        if format_string:
            promoted = Promoted.objects.get(slug=format_string)
        else:
            promoted = Promoted.objects.latest('pub_date')
        return { 'obj': promoted }
    except ObjectDoesNotExist:
        return ''

@register.inclusion_tag('replica/contrib/publisher/templatetags/render_collections.html')
def render_collections(num=255):
    request = context['request']
    collections = Collection.objects.order_by('-pub_date')[:num]
    return { 'object_list': collections, }


@register.inclusion_tag('replica/contrib/publisher/templatetags/render_sticky.html')
def render_sticky(num=5):
    entries = Entry.objects.sticky()[:num]
    return { 'object_list': entries, }
