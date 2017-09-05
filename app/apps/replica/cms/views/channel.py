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

from replica.cms.forms import ChannelModelForm

#Get list of all entries
class ChannelList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/channel/ChannelList.html'
	def get_queryset(self):
		return Channel.objects.all()
	def get_context_data(self, **kwargs):
		context = super(ChannelList, self).get_context_data(**kwargs)
		context.update({'title':'All Channels', 'is_list':True,})
		return context

def ChannelEdit(request, channelID=None):
	if channelID:
		channel = get_object_or_404(Channel, pk=channelID)
		instance = channel
		edit = True
	else:
		channel = ''
		instance = Topic(user=request.user)
		edit = False
	if request.method == 'POST':
		f = ChannelModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message('New channel created.')
			return redirect('Replica:EditChannel', ChannelID=instance.id)
	else:
		f = ChannelModelForm(instance=instance)
	variables = {'form': f, 'obj': channel, 'content_type': 'Channel', 'editing':edit }
	template = 'replica/cms/channel/Edit.html'
	return render(request, template, variables)

def ChannelDelete(request, channelID):
	c = get_object_or_404(Channel, pk=channelID)
	if request.method == 'POST':
		c.delete()
		return redirect('Replica:Index')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': c, 'content_type': 'Channel'}
	return render(request, template, variables)
