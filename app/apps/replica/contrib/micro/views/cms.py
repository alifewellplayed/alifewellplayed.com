from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from replica.contrib.micro.models import Timeline, Note
from replica.contrib.micro.forms import TimelineModelForm, NoteModelForm

def Index(request):
    template = 'replica/contrib/micro/cms/Index.html'
    variables = {}
    return render(request, template, variables)

def TimelineEdit(request, timelineID=None):
    timelines = Timeline.objects.all()
    if timelineID:
        timeline_obj = get_object_or_404(Timeline, pk=timelineID)
        instance = timeline_obj
        edit = True
        msg = 'Timeline updated.'
        obj_title = "Editing Timeline: {}".format(timeline_obj.name)
    else:
        timeline_obj = None
        instance = Timeline(user=request.user)
        edit = False
        msg = 'New timeline created.'
        obj_title = 'New Timeline'
    if request.method == 'POST':
        f = TimelineModelForm(request.POST or None, request.FILES, instance=instance)
        if f.is_valid():
            f.save()
            messages.info(request, msg)
            return redirect('ReplicaAdmin:TimelineEdit', timelineID=instance.id)
    else:
        f = TimelineModelForm(instance=instance)
    variables = {
        'form': f,
        'obj': timeline_obj,
        'object_list': timelines,
        'content_type': 'Timeline',
        'edit':edit,
        'obj_title':obj_title,
    }
    template = 'replica/contrib/micro/cms/timeline_Edit.html'
    return render(request, template, variables)

def NoteEdit(request, noteID=None, timelineID=None):
    if timelineID:
        timeline_obj = get_object_or_404(Timeline, pk=timelineID)
    else:
        timeline_obj = None
    if noteID:
        note_obj = get_object_or_404(Note, pk=noteID)
        instance = note_obj
        edit = True
        msg = 'Note updated.'
        obj_title = "Editing note: {}".format(note_obj.title)
    else:
        note_obj = None
        instance = Note(user=request.user)
        edit = False
        msg = 'New note created.'
        obj_title = 'New note'
    if request.method == 'POST':
        f = NoteModelForm(request.POST or None, request.FILES, instance=instance)
        if f.is_valid():
            f.save()
            messages.info(request, msg)
            return redirect('ReplicaAdmin:NoteEdit', noteID=instance.id)
    else:
        f = NoteModelForm(instance=instance)
    variables = {
        'form': f,
        'note_obj': note_obj,
        'timeline_obj': timeline_obj,
        'content_type': 'Note',
        'edit':edit,
        'obj_title':obj_title,
    }
    template = 'replica/contrib/micro/cms/timeline_Edit.html'
    return render(request, template, variables)

def NoteDelete(request, noteID):
    obj = get_object_or_404(Note, pk=noteID)
    if request.method == 'POST':
        obj.delete()
        return redirect('ReplicaAdmin:TimelineNoteList', timelineID=obj.slug)
    template = 'replica/cms/shared/delete-confirm.html'
    variables = {'obj': obj, 'content_type': 'Note'}
    return render(request, template, variables)

def TimelineDelete(request, timelineID):
    obj = get_object_or_404(Timeline, pk=timelineID)
    if request.method == 'POST':
        obj.delete()
        return redirect('ReplicaAdmin:TimelineList')
    template = 'replica/cms/shared/delete-confirm.html'
    variables = {'obj': obj, 'content_type': 'Timeline'}
    return render(request, template, variables)
