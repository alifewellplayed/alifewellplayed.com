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
from replica.pulse.models import Entry, Draft, Media, Channel, EntryLink
from replica.pulse.mixins import PulseViewMixin

from replica.cms.forms import ChannelModelForm

#Get list of all entries
def ChannelEdit(request, channelID=None):
	channels = Channel.objects.all()
	if channelID:
		channel = get_object_or_404(Channel, pk=channelID)
		instance = channel
		edit = True
		msg = 'Channel updated.'
		obj_title = "Editing channel: {}".format(channel.title)
	else:
		channel = ''
		instance = Channel(user=request.user)
		edit = False
		msg = 'New channel created.'
		obj_title = 'New Channel'
	if request.method == 'POST':
		f = ChannelModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:EditChannel', channelID=instance.id)
	else:
		f = ChannelModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': channel,
		'object_list': channels,
		'content_type': 'Channel',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/cms/channel_Edit.html'
	return render(request, template, variables)

def ChannelDelete(request, channelID):
	c = get_object_or_404(Channel, pk=channelID)
	if request.method == 'POST':
		msg = 'Channel has been deleted.'
		messages.warning(request, msg)
		c.delete()
		return redirect('ReplicaAdmin:ChannelList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': c, 'content_type': 'Channel'}
	return render(request, template, variables)
