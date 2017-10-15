from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.conf import settings
from mixpanel import Mixpanel

from replica.contrib.redirection.models import SiteLink, ClickLink, BlockedIp

def LinkRedirect(request, slug):
	obj = get_object_or_404(SiteLink, slug=slug)
	mp = Mixpanel(settings.MIXPANEL_TOKEN)
	#Redirects links and keeps track of them
	try:
		outgoing_link = obj.link
		link_guid = obj.pk
		link_click = ClickLink(link_id=link_guid)
		link_click.store(request)

		#mixpanel
		mp.track(obj.id, 'Link Tracker', {
			'Link': obj.link,
			'User IP': request.META['REMOTE_ADDR'],
			'Referer': request.META.get('HTTP_REFERER',''),
			'User Agent': request.META.get('HTTP_USER_AGENT','')
		})
	except KeyError:
		# Someone got here without the link param
		# Redirect to Home as default
		link = '/'

	return HttpResponseRedirect(outgoing_link)
