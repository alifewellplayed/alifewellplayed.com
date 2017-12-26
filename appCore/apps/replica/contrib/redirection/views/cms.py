from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.conf import settings
from mixpanel import Mixpanel

from replica.contrib.redirection.models import SiteLink, ClickLink, BlockedIp

class SiteLinkListView(ListView):
	paginate_by = 25
	template_name = 'replica/contrib/redirection/cms/sitelink_List.html'

	def get_queryset(self):
		links = SiteLink.objects.order_by('-pub_date')
		return links

	def get_context_data(self, **kwargs):
		context = super(SiteLinkListView, self).get_context_data(**kwargs)
		return context

def SiteLinkEdit(request, linkID=None):
	if linkID:
		link_obj = get_object_or_404(SiteLink, pk=linkID)
		instance = link_obj
		edit = True
		msg = 'Redirection link updated.'
		obj_title = "Editing link: {}".format(link_obj.link)
	else:
		link_obj = None
		instance = SiteLink(user=request.user)
		edit = False
		msg = 'New link created.'
		obj_title = 'New site link'
	if request.method == 'POST':
		f = SiteLinkModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:SiteLinkEdit', linkID=instance.id)
	else:
		f = SiteLinkModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': link_obj,
		'content_type': 'Site Link',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/contrib/redirection/cms/sitelink_Edit.html'
	return render(request, template, variables)

def SiteLinkDelete(request, linkID):
	obj = get_object_or_404(SiteLink, pk=noteID)
	if request.method == 'POST':
		obj.delete()
		return redirect('ReplicaAdmin:SiteLinkList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': obj, 'content_type': 'Note'}
	return render(request, template, variables)

class BlockedIpListView(ListView):
	paginate_by = 25
	template_name = 'replica/contrib/zine/cms/blockedip_List.html'
	def get_queryset(self):
		blocked = BlockedIp.objects.order_by('name')
		return blocked
	def get_context_data(self, **kwargs):
		context = super(BlockedIpListView, self).get_context_data(**kwargs)
		return context

def BlockedIpEdit(request, blockedID=None):
	if blockedID:
		blocked_obj = get_object_or_404(BlockedIp, pk=blockedID)
		instance = blocked_obj
		edit = True
		msg = 'Blocked IP updated.'
		obj_title = "Editing IP: {}".format(blocked_obj.ip_addr)
	else:
		blocked_obj = None
		instance = BlockedIp(user=request.user)
		edit = False
		msg = 'Created a new blocked IP.'
		obj_title = 'New site link'
	if request.method == 'POST':
		f = BlockedIpModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:BlockedIpEdit', blockedID=instance.id)
	else:
		f = BlockedIpModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': blocked_obj,
		'content_type': 'BlockedIp',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/contrib/redirection/cms/blockedip_Edit.html'
	return render(request, template, variables)

def BlockedIpDelete(request, blockedID):
	obj = get_object_or_404(BlockedIp, pk=blockedID)
	if request.method == 'POST':
		obj.delete()
		return redirect('ReplicaAdmin:BlockedIpList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': obj, 'content_type': 'BlockedIp'}
	return render(request, template, variables)
