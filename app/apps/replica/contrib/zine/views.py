from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.contrib import messages

from coreExtend.models import Account
from replica import settings as ReplicaSettings
from replica.contrib.zine.models import Promoted, Collection
from replica.contrib.zine.forms import PromotedModelForm

#Replica Editor homepage
def Index(request):
	template = 'replica/contrib/zine/cms/Index.html'
	variables = {}
	return render(request, template, variables)

def PromotedEdit(request, promotedID=None):
	promoted = Promoted.objects.all()
	if promotedID:
		promoted_obj = get_object_or_404(Promoted, pk=promotedID)
		instance = promoted_obj
		edit = True
		msg = 'Promotion updated.'
		obj_title = "Editing promotion: {}".format(promoted_obj.title)
	else:
		promoted_obj = None
		instance = Promoted(user=request.user)
		edit = False
		msg = 'New promotion created.'
		obj_title = 'New Promotion'
	if request.method == 'POST':
		f = PromotedModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:PromotedEdit', promotedID=instance.id)
	else:
		f = PromotedModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': promoted_obj,
		'object_list': promoted,
		'content_type': 'Promotion',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/contrib/zine/cms/promoted_Edit.html'
	return render(request, template, variables)

def PromotedDelete(request, promotedID):
	obj = get_object_or_404(Promoted, pk=promotedID)
	if request.method == 'POST':
		obj.delete()
		return redirect('ReplicaAdmin:PromotedList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': obj, 'content_type': 'Promotion'}
	return render(request, template, variables)
