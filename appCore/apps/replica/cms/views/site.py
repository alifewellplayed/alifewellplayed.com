from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.contrib import messages

from coreExtend.models import Account
from replica import settings as ReplicaSettings
from replica.pulse.models import Entry, Draft, Media, Topic, Channel, EntryLink 
from replica.cms.models import MenuPosition, MenuItem, SiteSettings
from replica.cms.forms import SiteModelForm, MenuPositionModelForm, MenuItemModelForm

#Replica Editor homepage
def Index(request):
	template = 'replica/cms/site_Index.html'
	variables = {'is_home':True, 'is_list':False,}
	return render(request, template, variables)

#List of Site Plugins
def PluginList(request):
	template = 'replica/cms/site_PluginList.html'
	variables = {'is_home':False, 'is_list':False,}
	return render(request, template, variables)

#Site Settings
def Settings(request):
	current_site =  get_object_or_404(SiteSettings, id=settings.SITE_ID)
	if request.method == 'POST':
		f = SiteModelForm(request.POST or None, request.FILES, instance=current_site)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Settings have been updated.')
			return redirect('ReplicaAdmin:SiteSettings')
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

def MenuEdit(request, menuID=None):
	menus = MenuPosition.objects.all()
	if menuID:
		menu = get_object_or_404(MenuPosition, pk=menuID)
		menu_items = MenuItem.objects.filter(position=menu)
		instance = menu
		menu_items_count = menu_items.count(),
		edit = True
		msg = 'Menu updated.'
		obj_title = "Editing: {}".format(menu.title)
	else:
		menu = None
		menu_items = None
		menu_items_count = None
		instance = MenuPosition()
		edit = False
		msg = 'New menu created.'
		obj_title = 'New Menu'
	if request.method == 'POST':
		f = MenuPositionModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:MenuEdit', menuID=instance.id)
	else:
		f = MenuPositionModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': menu,
		'obj_items': menu_items,
		'obj_items_count': menu_items_count,
		'object_list': menus,
		'content_type': 'Menu',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/cms/Menu_Edit.html'
	return render(request, template, variables)

def MenuDelete(request, menuID):
	menu = get_object_or_404(MenuPosition, pk=menuID)
	if request.method == 'POST':
		msg = 'Menu deleted.'
		messages.warning(request, msg)
		menu.delete()
		return redirect('ReplicaAdmin:MenuEdit')
	template = 'replica/cms/delete-confirm.html'
	variables = {'obj': menu, 'content_type': 'Menu'}
	return render(request, template, variables)

def MenuItemEdit(request, menuID, itemID=None):
	menu = get_object_or_404(MenuPosition, pk=menuID)
	menu_items = MenuItem.objects.filter(position=menu)

	if itemID:
		menu_item = get_object_or_404(MenuItem, pk=itemID)
		instance = menu_item
		edit = True
		obj_title = "Editing: {}".format(menu_item.title)
		msg = 'Menu item updated.'
	else:
		menu_item = ''
		instance = MenuItem(position=menu)
		edit = False
		obj_title = 'Adding menu item'
		msg = 'New menu item added'
	if request.method == 'POST':
		f = MenuItemModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.info(request, msg)
			return redirect('ReplicaAdmin:MenuItemEdit', menuID=menu.id, itemID=instance.id)
	else:
		f = MenuItemModelForm(instance=instance)
	variables = {
		'form': f,
		'menu_obj': menu,
		'edit':edit,
		'object_list': menu_items,
		'content_type': 'Menu Item',
		'obj_title':obj_title,
	}
	template = 'replica/cms/Menuitem_Edit.html'
	return render(request, template, variables)

def MenuItemDelete(request, menuID, itemID):
	menu = get_object_or_404(MenuPosition, pk=menuID)
	menuitem = get_object_or_404(MenuItem, pk=menuID)
	if request.method == 'POST':
		msg = 'Menu item deleted.'
		messages.warning(request, msg)
		menuitem.delete()
		return redirect('ReplicaAdmin:MenuEdit', menuID=menu.pk)
	template = 'replica/cms/delete-confirm.html'
	variables = {'obj': menuitem, 'content_type': 'Menu Item'}
	return render(request, template, variables)
