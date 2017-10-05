from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView

from replica.pulse.models import EntryTemplate
from replica.cms.forms import EntryTemplateModelForm

#Get list of all templates
class EntryTemplateList(ListView):
    paginate_by = ReplicaSettings.PAGINATE
    template_name = 'replica/cms/template_List.html'
    def get_queryset(self):
        return EntryTemplate.objects.all()
    def get_context_data(self, **kwargs):
        context = super(EntryTemplateList, self).get_context_data(**kwargs)
        context.update({'title':'Temlate List', 'is_list':True,})
        return context

def EntryTemplateEdit(request, templateID=None):
	if templateID:
		template = get_object_or_404(EntryTemplate, pk=templateID)
		instance = template
		edit = True
		msg = 'Template updated.'
		obj_title = "Editing template: {}".format(template.title)
	else:
		template = None
		instance = EntryTemplate(user=request.user)
		edit = False
		msg = 'New template created.'
		obj_title = 'New Template'
	if request.method == 'POST':
		f = EntryTemplateModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(msg)
			return redirect('ReplicaAdmin:EditTemplate', templateID=instance.id)
	else:
		f = EntryTemplateModelForm(instance=instance)
	variables = {
		'form': f,
		'obj': template,
		'content_type': 'Template',
		'edit':edit,
		'obj_title':obj_title,
	}
	template = 'replica/cms/template_Edit.html'
	return render(request, template, variables)

def EntryTemplateDelete(request, templateID):
	t = get_object_or_404(EntryTemplate, pk=templateID)
	if request.method == 'POST':
		t.delete()
		return redirect('ReplicaAdmin:TemplateList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': t, 'content_type': 'Template'}
	return render(request, template, variables)
