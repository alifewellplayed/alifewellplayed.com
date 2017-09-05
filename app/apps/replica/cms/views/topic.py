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

from replica.cms.forms import TopicModelForm

#Get list of all entries
class TopicList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/topic/TopicList.html'
	def get_queryset(self):
		return Topic.objects.all()
	def get_context_data(self, **kwargs):
		context = super(TopicList, self).get_context_data(**kwargs)
		context.update({'title':'Topics', 'is_list':True,})
		return context

def TopicEdit(request, TopicID=None):
	if topicID:
		topic = get_object_or_404(Topic, pk=topicID)
		instance = topic
		edit = True
		msg = 'Topic Updated'
	else:
		topic = ''
		instance = Topic(user=request.user)
		edit = False
		msg = 'New Topic Created'
	if request.method == 'POST':
		f = TopicModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(msg)
			return redirect('Replica:EditTopic', TopicID=instance.id)
	else:
		f = TopicModelForm(instance=instance)
	variables = {'form': f, 'obj': topic, 'content_type': 'Topic', 'editing':edit }
	template = 'replica/cms/topic/Edit.html'
	return render(request, template, variables)

def TopicDelete(request, topicID):
	t = get_object_or_404(Topic, pk=topicID)
	if request.method == 'POST':
		t.delete()
		return redirect('Replica:Index')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': t, 'content_type': 'Topic'}
	return render(request, template, variables)
