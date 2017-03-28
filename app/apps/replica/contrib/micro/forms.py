from __future__ import absolute_import

import markdown
from django import forms
from django.forms import widgets
from .models import Timeline, Note


class TimelineModelForm(forms.ModelForm):

	class Meta:
		model = Timeline
		exclude = ('pub_date', 'slug', 'user', 'image', 'id',)
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
		}


class NoteModelForm(forms.ModelForm):

	class Meta:
		model = Note
		exclude = ('pub_date', 'timeline', 'user', 'body_html', 'id')
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control', 'rows':'2', 'placeholder':'Start typing something...'}),
		}
