import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from pagedown.widgets import AdminPagedownWidget

from coreExtend.models import Account
from replica.pulse.models import Entry, Draft, Topic, Media, Channel
from replica.widgets import CustomSplitDateTimeWidget

class EntryModelForm(forms.ModelForm):
    #deck = forms.CharField(widget=AdminPagedownWidget())
    #body = forms.CharField(widget=AdminPagedownWidget(), required=False)

    pub_date = forms.SplitDateTimeField(
        input_time_formats=['%I:%M%p'],
        widget=CustomSplitDateTimeWidget(
            date_attrs={'placeholder': 'Event Date', 'class': 'form-control datepicker' },
            time_attrs={'placeholder': 'Event Time', 'class': 'form-control timepicker' }
        )
    )

    class Meta:
        model = Entry
        fields = [
            'title',
            'deck',
            'body',
            'slug',
            'url',
            'user',
            'topic',
            'pub_date',
            'is_active',
            'channel',
            'content_format',
            'featured_image',
            'template'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Title', 'value':''}),
            'deck': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Optional Summary', 'rows':'1'}),
            'body': forms.Textarea(attrs={'class':'form-control replica-form-control autosize markdown', 'placeholder':'Start typing...', 'rows':'3'}),
            'slug': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Slug', 'value':''}),
            'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'http://', 'value':''}),
            'topic': forms.CheckboxSelectMultiple(),
            'is_active': forms.RadioSelect,
            'content_format': forms.RadioSelect,
            'channel': forms.Select(attrs={'class':'form-control',}),
            'featured_image': forms.Select(attrs={'class':'form-control',}),
            'template': forms.Select(attrs={'class':'form-control',}),
        }

class ChannelModelForm(forms.ModelForm):
    class meta:
        model = Channel
        exclude = ('id', 'user', 'date_created', 'date_updated', 'slug')

class TopicModelForm(forms.ModelForm):
    class meta:
        model = Channel
        exclude = ('id', 'user', 'date_created', 'date_updated', 'slug')
