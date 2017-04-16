from __future__ import absolute_import

import logging
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from .models import Timeline, Note
from .forms import TimelineModelForm, NoteModelForm

class TimelinesListView(ListView):
	paginate_by = 25
	template_name = 'replica/contrib/micro/timeline_list.html'

	def get_queryset(self):
		return Timeline.objects.order_by('-date_updated')

	def get_context_data(self, **kwargs):
		context = super(TimelinesListView, self).get_context_data(**kwargs)
		context.update({})
		return context

class NoteListView(ListView):
	paginate_by = 100
	template_name = 'replica/contrib/micro/note_list.html'

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
	template_name = 'replica/contrib/micro/note_list.html'

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


@login_required
def AddNote(request, timeline_slug):
	#Lets user add new enties to a list.
	ft = get_object_or_404(Timeline, slug=timeline_slug)
	instance = Note(user=request.user, timeline=ft)
	f = NoteModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Note Added.')
		return redirect('ReplicaMicro:Add', timeline_slug=timeline_slug)

	ctx = {'form': f, 'timeline': ft, 'adding': True}
	return render(request, 'replica/contrib/micro/edit-note.html', ctx)

@login_required
def AddTimeline(request):
	#add a timeline.
	instance = Timeline(user=request.user)
	f = TimelineModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'New list created.')
		return redirect('ReplicaMicro:Timelines')

	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/contrib/micro/edit-timeline.html', ctx)

@login_required
def EditTimeline(request, timeline_slug):
	#Lets a user edit a note they've previously added.
	timeline = get_object_or_404(Timeline, slug=timeline_slug)
	f = TimelineModelForm(request.POST or None, instance=timeline)
	if f.is_valid():
		f.save()
		return redirect('ReplicaMicro:Timeline', timeline_slug=timeline_slug)
	ctx = {'form': f, 'timeline': timeline, 'adding': False}
	return render(request, 'replica/contrib/micro/edit-timeline.html', ctx)

@login_required
def EditNote(request, note_id):
	#Lets a user edit a note they've previously added.
	note = get_object_or_404(Note, pk=note_id, user=request.user)
	f = NoteModelForm(request.POST or None, instance=note)
	if f.is_valid():
		f.save()
		return redirect('ReplicaMicro:Timeline', timeline_slug=timeline_slug)

	ctx = {'form': f, 'note': note, 'adding': False}
	return render(request, 'replica/contrib/micro/edit-note.html', ctx)

@login_required
def DeleteNote(request, note_id):
	#Lets a user delete an note they've previously added.
	#Only entries the user "owns" can be deleted.
	note = get_object_or_404(Note, pk=note_id, user=request.user)
	if request.method == 'POST':
		note.delete()
		return redirect('ReplicaMicro:Timelines')
	return render(request, 'replica/contrib/micro/delete-confirm.html', {'note': note})
