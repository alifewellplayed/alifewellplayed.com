from __future__ import absolute_import
from urllib.parse import urlparse
import hashlib

from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

from replica.contrib.micro.forms import NoteModelForm
from replica.contrib.micro.models import Timeline, Note

register = template.Library()

@register.inclusion_tag('micro/templatetags/lists.html')
def render_lists(user, num):
    objects = Timeline.objects.filter(user__username=user)[:num]
    return {'objects': objects,}

@register.inclusion_tag('micro/templatetags/render_notes.html')
def render_latest_notes(num=100, user=None):
    objects = Note.objects.filter(timeline=num)
    return { 'objects': objects, }

@register.inclusion_tag('micro/templatetags/render_notes_mobile.html')
def render_latest_notes_mobile(user, num):
    objects = Note.objects.filter(timeline=num).filter(user__username=user)
    return { 'objects': objects, }

@register.inclusion_tag('micro/templatetags/new_note.html')
def new_note(request):
    return {'form': NoteModelForm(),}

@register.simple_tag
def new_note(request):
    return render_to_string('micro/templatetags/new_note.html', {'form': NoteModelForm()}, context_instance=RequestContext(request))
