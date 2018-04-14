from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.contrib import messages

from coreExtend.models import Account
from replica import settings as ReplicaSettings
from replica.pulse.models import Entry, Draft, Media, Topic, Media, EntryLink
from replica.pulse.mixins import PulseViewMixin

from replica.cms.forms import MediaModelForm

#Get list of all entries
class MediaList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/media_List.html'
	def get_queryset(self):
		return Media.objects.order_by('-date_updated')
	def get_context_data(self, **kwargs):
		context = super(MediaList, self).get_context_data(**kwargs)
		context.update({'title':'All Media', 'is_list':True,})
		return context

def MediaEdit(request, mediaID=None):
	if mediaID:
		media = get_object_or_404(Media, pk=mediaID)
		instance = media
		edit = True
	else:
		media = None
		instance = Topic(user=request.user)
		edit = False
	if request.method == 'POST':
		f = MediaModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message('New media created.')
			return redirect('ReplicaAdmin:EditMedia', mediaID=instance.id)
	else:
		f = MediaModelForm(instance=instance)
	variables = {'form': f, 'obj': media, 'content_type': 'Media', 'editing':edit }
	template = 'replica/cms/media_Edit.html'
	return render(request, template, variables)

def MediaDelete(request, mediaID):
	c = get_object_or_404(Media, pk=mediaID)
	if request.method == 'POST':
		c.delete()
		return redirect('ReplicaAdmin:MediaList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': c, 'content_type': 'Media'}
	return render(request, template, variables)
