import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from pagedown.widgets import AdminPagedownWidget

from coreExtend.models import Account
from replica.pulse.models import *
from replica.cms.models import *
from replica.widgets import CustomSplitDateTimeWidget

class EntryModelForm(forms.ModelForm):
    pub_date = forms.SplitDateTimeField(
        input_time_formats=['%I:%M%p'],
        widget=CustomSplitDateTimeWidget(
            date_attrs={'placeholder': 'Event Date', 'class': 'form-control datepicker' },
            time_attrs={'placeholder': 'Event Time', 'class': 'form-control timepicker' }
        )
    )
    class Meta:
        model = Entry
        fields = [ 'title', 'deck', 'body', 'slug', 'url', 'user', 'topic', 'pub_date', 'is_active', 'channel', 'content_format', 'featured_image', 'template', ]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Title', 'value':''}),
            'deck': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Optional Summary', 'rows':'1'}),
            'body': forms.Textarea(attrs={'class':'form-control replica-form-control autosize markdown', 'placeholder':'Start typing...', 'rows':'3'}),
            'slug': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Slug', 'value':''}),
            'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'http://', 'value':''}),
            'topic': forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}),
            'is_active': forms.RadioSelect(attrs={'class':'form-check-input'}),
            'content_format': forms.RadioSelect(attrs={'class':'form-check-input'}),
            'channel': forms.Select(attrs={'class':'form-control',}),
            'featured_image': forms.Select(attrs={'class':'form-control',}),
            'template': forms.Select(attrs={'class':'form-control',}),
        }


class ChannelModelForm(forms.ModelForm):
    class Meta:
        model = Channel
        exclude = ('id', 'user', 'date_created', 'date_updated')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Title', 'value':''}),
            'slug': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Slug', 'value':''}),
        }

class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('id', 'user', 'date_created', 'date_updated', 'slug')
        widgets = {
            'image': forms.Select(attrs={'class':'form-control',}),
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Topic Name', 'value':''}),
            'description': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Description', 'rows':'1'}),
            'is_public': forms.RadioSelect(attrs={'class':'form-check-input'}),
        }

class MediaModelForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['user', 'title', 'caption']

class SiteModelForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        exclude = ('id', 'date_created', 'date_updated',)
        widgets = {
            'logo': forms.Select(attrs={'class':'form-control',}),
            'featured': forms.Select(attrs={'class':'form-control',}),
            'name': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Site Name', 'value':''}),
            'domain': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Site description', 'value':''}),
            'password': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Password', 'value':''}),
            'description': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Site description', 'value':''}),
            'author': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Site author', 'value':''}),
            'is_enabled': forms.RadioSelect(attrs={'class':'form-check-input'}),
            'summary': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Optional Summary', 'rows':'1'}),
            'secret_token': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Secret token', 'value':''}),
            'view_settings': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Additional Site settings', 'rows':'1'}),
        }

class MenuPositionModelForm(forms.ModelForm):
    class Meta:
        model = MenuPosition
        exclude = ('id', 'date_created', 'date_updated')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Title', 'value':''}),
            'slug': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Slug', 'value':''}),
        }

class MenuItemModelForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ('id', 'date_created', 'date_updated')
        widgets = {
            'icon': forms.Select(attrs={'class':'form-control',}),
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Menu name', 'value':''}),
            'description': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Description', 'value':''}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'slug', 'value':''}),
            'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'http://', 'value':''}),
            'page': forms.Select(attrs={'class':'form-control',}),
            'weight': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Order position', 'value':''}),
        }

class CodeBlockModelForm(forms.ModelForm):
    class Meta:
        model = CodeBlock
        exclude = ('id', 'date_created', 'date_updated', 'user',)
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Template Title', 'value':''}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'slug', 'value':''}),
            'description': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Description', 'value':''}),
            'template_html': forms.Textarea(attrs={'class':'html-editor sr-only', 'value':''}),
            'type': forms.RadioSelect(attrs={'class':'form-check-input'}),
        }

class PluginModelForm(forms.ModelForm):
    class Meta:
        model = Plugin
        exclude = ('id', 'date_created', 'date_updated')
        widgets = {
            'is_enabled': forms.RadioSelect(attrs={'class':'form-check-input'}),
            'slug': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Slug', 'value':''}),
        }
