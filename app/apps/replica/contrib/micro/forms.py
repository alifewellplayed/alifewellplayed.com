from django import forms
from django.forms import widgets
from replica.widgets import CustomSplitDateTimeWidget
from replica.contrib.micro.models import Timeline, Note

class TimelineModelForm(forms.ModelForm):
	class Meta:
		model = Timeline
		exclude = ('date_created', 'date_updated', 'slug', 'user', 'id', 'deck_html')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Timeline title'}),
			'deck': forms.Textarea(attrs={'class':'form-control replica-form-control autosize', 'placeholder':'Optional Summary', 'rows':'1'}),
			'is_public': forms.CheckboxInput(attrs={'class':'form-check-input'}),
			'rev_order': forms.CheckboxInput(attrs={'class':'form-check-input'}),
		}

class NoteModelForm(forms.ModelForm):
	pub_date = forms.SplitDateTimeField(
        input_time_formats=['%I:%M%p'],
        widget=CustomSplitDateTimeWidget(
            date_attrs={'placeholder': 'Event Date', 'class': 'form-control datepicker' },
            time_attrs={'placeholder': 'Event Time', 'class': 'form-control timepicker' }
        )
    )
	class Meta:
		model = Note
		exclude = ('date_created', 'date_updated', 'user', 'body_html', 'id')
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control autosize', 'rows':'2', 'placeholder':'Start typing something...'}),
			'is_private': forms.CheckboxInput(attrs={'class':'form-check-input'}),
			'timeline': forms.Select(attrs={'class':'form-control',}),
		}
