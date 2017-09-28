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

from replica.cms.forms import SiteModelForm

#Replica Editor homepage
def Index(request):
	template = 'replica/cms/site_Index.html'
	variables = {'is_home':True, 'is_list':False,}
	return render(request, template, variables)

#Site Settings
def Settings(request, siteID=None):
	current_site =  get_object_or_404(SiteSettings, id=settings.SITE_ID)
	if request.method == 'POST':
		f = SiteModelForm(request.POST or None, request.FILES, instance=current_site)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Settings saved.')
			return redirect('Replica:SiteSettings')
	else:
		f = SiteModelForm(instance=current_site)
	template = 'replica/cms/site_Settings.html'
	variables = {'SiteSettings': current_site, 'title':'Site Settings', 'is_list':False, 'form': f,}
	return render(request, template, variables)

#Get list of all users
class UserList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/site_UserList.html'
	def get_queryset(self):
		return Account.objects.all().order_by('-pub_date')
	def get_context_data(self, **kwargs):
		context = super(UserList, self).get_context_data(**kwargs)
		context.update({'title':'User List', 'is_list':True,})
		return context

#User Profile page
def UserDetail(request, slug):
	u = get_object_or_404(Account, username=username)
	template = 'replica/cms/site/site_UserDetail.html'
	variables = {'user_obj': u, 'title':u.username, 'is_list':False,}
	return render(request, template, variables)

class UserEntriesList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/site/site_UserEntriesList.html'
	def get_queryset(self):
		self.u = get_object_or_404(Account, username=self.kwargs.pop('username'))
		return Entry.objects.filter(user__username=self.u)
	def get_context_data(self, **kwargs):
		context = super(UserEntriesList, self).get_context_data(**kwargs)
		context.update({'user_obj': self.u, 'is_list':True, 'title':'User Entries', })
		return context
