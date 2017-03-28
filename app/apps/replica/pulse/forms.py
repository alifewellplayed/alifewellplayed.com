import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from pagedown.widgets import AdminPagedownWidget

from coreExtend.models import Account
from replica.pulse.models import Entry, Media, Draft, Topic, Channel


class AdminEntryForm(forms.ModelForm):
    deck = forms.CharField(widget=AdminPagedownWidget())
    body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Entry
        fields = ['title', 'deck', 'body', 'slug', 'url', 'user', 'topic', 'pub_date', 'is_active', 'channel', 'content_format', 'featured_image', ]
