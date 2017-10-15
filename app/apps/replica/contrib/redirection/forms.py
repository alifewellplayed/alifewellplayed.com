import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from pagedown.widgets import AdminPagedownWidget

from coreExtend.models import Account
from replica.contrib.redirection.models import *
from replica.widgets import CustomSplitDateTimeWidget

class SiteLinkModelForm(forms.ModelForm):
    class Meta:
        model = SiteLink
        exclude = ('id', 'date_created', 'date_updated', 'user', 'note_html')
        widgets = {
            'link': forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL', 'value':''}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Optional slug', 'value':''}),
            'note': forms.TextInput(attrs={'class':'form-control replica-form-control', 'placeholder':'Description', 'value':''}),
        }

class BlockedIpModelForm(forms.ModelForm):
    class Meta:
        model = BlockedIp
        exclude = ('id', 'date_created', 'date_updated',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name', 'value':''}),
            'ip_addr': forms.TextInput(attrs={'class':'form-control', 'placeholder':'IP Address', 'value':''}),
        }
