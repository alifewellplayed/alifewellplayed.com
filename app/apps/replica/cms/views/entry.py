from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse

from coreExtend.models import Account
from replica import settings as ReplicaSettings
from replica.pulse.models import Entry, Draft, Media, Topic, Channel, MenuPosition, MenuItem, EntryLink, SiteSettings
from replica.pulse.mixins import PulseViewMixin

def Editor(request, entryID=None):
	template = 'replica/cms/entry/Editor.html'
	variables = {'is_list':False, 'edit':False,}
	return render(request, template, variables)

#Get list of all entries
class EntryList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/entry/EntryList.html'
	def get_queryset(self):
		return Entry.objects.posts()
	def get_context_data(self, **kwargs):
		context = super(EntryList, self).get_context_data(**kwargs)
		context.update({'title':'All Entries', 'is_list':True,})
		return context

#Get list of all pages
class PageList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/entry/PageList.html'
	def get_queryset(self):
		return Entry.objects.pages()
	def get_context_data(self, **kwargs):
		context = super(PagesList, self).get_context_data(**kwargs)
		context.update({'is_list':True, 'title':'All Pages', })
		return context

#Entry Detailed page
class EntryDetail(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/entry/EntryDetail.html'
	def get_queryset(self):
		self.entry = get_object_or_404(Entry, pk=self.kwargs.pop('entryID'))
		return Entry.objects.pages()
	def get_context_data(self, **kwargs):
		context = super(PagesList, self).get_context_data(**kwargs)
		context.update({'is_list':True, 'title':'All Pages', })
		return context

class EntryDetail(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/entry/EntryDetail.html'
	def get_queryset(self):
		self.entry = get_object_or_404(Entry, pk=self.kwargs.pop('entryID'))
		return Draft.objects.filter(entry=self.entry)
	def get_context_data(self, **kwargs):
		context = super(EntryDetail, self).get_context_data(**kwargs)
		context.update({'entry_obj': self.entry, 'is_list':True, 'title':'User Entries', })
		return context

def EntryDelete(request, entryID):
	entry = get_object_or_404(Entry, pk=entryID)
	if request.method == 'POST':
		entry.delete()
		return redirect('Replica:Index')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': entry, 'content_type': 'Entry'}
	return render(request, template, variables)

def EntryDraft(request, entryID, draftID):
	entry = get_object_or_404(Entry, pk=entryID)
	draft = get_object_or_404(Draft, pk=draftID)
	template = 'replica/cms/entry/EntryDraft.html'
	variables = {'obj_e': entry, obj_d:'draft', 'content_type': 'Entry'}
	return render(request, template, variables)
