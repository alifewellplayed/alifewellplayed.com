from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, html_safe

class CustomSplitDateTimeWidget(forms.SplitDateTimeWidget):

    template_name = 'replica/forms/splitdatetime.html'

    def __init__(self, attrs=None, date_format=None, time_format=None, date_attrs=None, time_attrs=None):
        super(CustomSplitDateTimeWidget, self).__init__(attrs=attrs, date_format=date_format, time_format=time_format)

        if date_attrs:
            self.widgets[0].attrs.update(date_attrs)
        if time_attrs:
            self.widgets[1].attrs.update(time_attrs)
