import markdown
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from coreExtend.models import Account
from replica.contrib.zine.models import Promoted, Collection
from replica.widgets import CustomSplitDateTimeWidget

class PromotedModelForm(forms.ModelForm):
    pub_date = forms.SplitDateTimeField(
        input_time_formats=['%I:%M%p'],
        widget=CustomSplitDateTimeWidget(
            date_attrs={'placeholder': 'Event Date', 'class': 'form-control datepicker' },
            time_attrs={'placeholder': 'Event Time', 'class': 'form-control timepicker' }
        )
    )
    class Meta:
        model = Promoted
        exclude = ('id', 'user', 'date_created', 'date_updated', 'slug', 'deck_html')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control replica-form-control form-control-title', 'placeholder':'Topic Name', 'value':''}),
            'deck': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Description', 'rows':'1'}),
            'image': forms.Select(attrs={'class':'form-control',}),
            'entry': forms.Select(attrs={'class':'form-control',}),
        }
