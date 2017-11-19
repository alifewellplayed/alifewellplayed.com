from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from replica import settings as replicaSettings
from replica.contrib.micro.models import Timeline, Note
from replica.contrib.micro.forms import TimelineModelForm, NoteModelForm

THEME = replicaSettings.SITE_THEME

class TimelinesListView(ListView):
    paginate_by = 25
    template_name='themes/{0}/contrib/micro/timeline_list.html'.format(THEME)

    def get_queryset(self):
        return Timeline.objects.order_by('-date_updated')

    def get_context_data(self, **kwargs):
        context = super(TimelinesListView, self).get_context_data(**kwargs)
        context.update({})
        return context

class NoteListView(ListView):
    paginate_by = 100
    template_name='themes/{0}/contrib/micro/note_list.html'.format(THEME)

    def get_queryset(self):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        if self.request.user.is_staff:
            b = Note.objects.filter(timeline=self.timeline)
        else:
            b = Note.objects.filter(timeline=self.timeline, is_private=False)
        if self.timeline.rev_order == True:
            return b.order_by('-date_updated')
        else:
            return b.order_by('date_updated')

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update({'timeline': self.timeline,})
        return context

class LatestNoteListView(ListView):
    paginate_by = 100
    template_name='themes/{0}/contrib/micro/note_list.html'.format(THEME)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Note.objects.order_by('pub_date')
        else:
            return Note.objects.order_by('pub_date').filter(is_private=False)

    def get_context_data(self, **kwargs):
        context = super(LatestNoteListView, self).get_context_data(**kwargs)
        return context

def SingleNote(request, note_id):
    #Shows a single note.
    note = get_object_or_404(Note, pk=note_id)
    ctx = {'note': note}
    return render(request, 'replica/contrib/micro/note.html', ctx)
