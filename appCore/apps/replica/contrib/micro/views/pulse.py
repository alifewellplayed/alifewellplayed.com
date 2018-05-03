from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import CreateView

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
    ctx = {'object': note}
    template_name = 'themes/{0}/contrib/micro/note.html'.format(THEME)
    return render(request, template_name, ctx)


def NoteCreate(request, timeline_slug):
    timeline = get_object_or_404(Timeline, slug=timeline_slug)
    if request.user.is_staff:
        notes = Note.objects.filter(timeline=timeline)
    else:
        notes = Note.objects.filter(timeline=timeline, is_private=False)
    if timeline.rev_order == True:
        notes = notes.order_by('-date_updated')
    else:
        notes = notes.order_by('date_updated')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = NoteModelForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user
                note.is_private=False
                note.timeline=timeline
                note = form.save()
                messages.add_message(request, messages.INFO, u'New note published'.format())
                return redirect('replica.micro:Timeline', timeline_slug=timeline.slug)
            else:
                form = NoteModelForm()
                messages.add_message(request, messages.INFO, u'Unable to publish note.')
        else:
            form = NoteModelForm()
    else:
        form = NoteModelForm()
    ctx = {'timeline': timeline, 'object_list':notes, 'form': form}
    template_name = 'themes/{0}/contrib/micro/noteUpdate.html'.format(THEME)
    return render(request, template_name, ctx)
