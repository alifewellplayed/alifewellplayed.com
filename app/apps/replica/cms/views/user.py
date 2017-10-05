from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.contrib import messages

from coreExtend.models import Account
from replica.cms.forms import AccountModelForm
from replica import settings as ReplicaSettings

class UserList(ListView):
	paginate_by = ReplicaSettings.PAGINATE
	template_name = 'replica/cms/user_List.html'
	def get_queryset(self):
		return Account.objects.order_by('-date_updated')
	def get_context_data(self, **kwargs):
		context = super(AccountList, self).get_context_data(**kwargs)
		context.update({'title':'User Accounts', 'is_list':True,})
		return context

def UserEdit(request, userID=None):
	if username:
		u = get_object_or_404(Account, pk=userID)
		instance = u
		edit = True
		msg = 'User account updated.'
		obj_title = "Editing user: {}".format(menu.title)
	else:
		u = None
		instance = Account()
		edit = False
		msg = 'New Account created.'
		obj_title = 'New User Account'
	if request.method == 'POST':
		f = AccountModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:UserEdit', menuID=instance.id)
	else:
		f = AccountModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': u,
		'content_type': 'Account',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/cms/user_Edit.html'
	return render(request, template, variables)

def UserDelete(request, userID):
	u = get_object_or_404(Account, pk=userID)
	if request.method == 'POST':
		u.delete()
		return redirect('Replica:Index')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': u, 'content_type': 'Media'}
	return render(request, template, variables)
