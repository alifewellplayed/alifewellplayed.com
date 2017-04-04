from __future__ import absolute_import
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django import template

from coreExtend.models import Account
from replica.contrib.publisher.models import Promoted, Collection

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
