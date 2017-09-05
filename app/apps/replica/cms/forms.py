import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from coreExtend.models import Account
from replica.pulse.models import Entry, Draft, Topic, Media, Channel


class ChannelModelForm(forms.ModelForm):
	class meta:
		model = Channel
		exclude = ('id', 'user', 'date_created', 'date_updated', 'slug')

class TopicModelForm(forms.ModelForm):
	class meta:
		model = Channel
		exclude = ('id', 'user', 'date_created', 'date_updated', 'slug')
