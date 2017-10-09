from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.contrib import messages

from replica import settings as ReplicaSettings
from replica.pulse.models import CodeBlock
from replica.cms.forms import CodeBlockModelForm

#Get list of all templates
class CodeBlockList(ListView):
    paginate_by = ReplicaSettings.PAGINATE
    template_name = 'replica/cms/template_List.html'
    def get_queryset(self):
        return CodeBlock.objects.all()
    def get_context_data(self, **kwargs):
        context = super(CodeBlockList, self).get_context_data(**kwargs)
        instance = CodeBlock(user=self.request.user)
        f = CodeBlockModelForm(instance=instance)
        context.update({'title':'Temlate List', 'is_list':True, 'form': f})
        return context

def CodeBlockEdit(request, templateID=None):
    if templateID:
        template = get_object_or_404(CodeBlock, pk=templateID)
        instance = template
        edit = True
        msg = 'Template updated.'
        obj_title = "Editing template: {}".format(template.title)
    else:
        template = None
        instance = CodeBlock(user=request.user)
        edit = False
        msg = 'New template created.'
        obj_title = 'New Template'
    if request.method == 'POST':
        f = CodeBlockModelForm(request.POST or None, request.FILES, instance=instance)
        if f.is_valid():
            f.save()
            messages.info(request, msg)
            return redirect('ReplicaAdmin:TemplateEdit', templateID=instance.id)
    else:
        f = CodeBlockModelForm(instance=instance)
    variables = {
        'form': f,
        'obj': template,
        'content_type': 'Template',
        'edit':edit,
        'obj_title':obj_title,
    }
    template = 'replica/cms/template_Edit.html'
    return render(request, template, variables)

def CodeBlockDelete(request, templateID):
	t = get_object_or_404(CodeBlock, pk=templateID)
	if request.method == 'POST':
		t.delete()
		return redirect('ReplicaAdmin:TemplateList')
	template = 'replica/cms/shared/delete-confirm.html'
	variables = {'obj': t, 'content_type': 'Template'}
	return render(request, template, variables)
