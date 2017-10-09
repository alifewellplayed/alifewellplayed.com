from django import template
from django.contrib.admin.models import LogEntry
from django.template import RequestContext, Context, Template
from django.utils.safestring import mark_safe

from replica.pulse.models import Entry, Draft, Topic, Media, Channel, CodeBlock
from replica import settings as ReplicaSettings

register = template.Library()

class RenderNode(template.Node):
    def __init__(self, content):
        self.content = content

    def render(self, context):
        try:
            self.content = template.resolve_variable(self.content, context)
            return template.Template(self.content).render(template.Context(context, autoescape=False))
        except (template.TemplateSyntaxError, e):
            return mark_safe("<strong>Template error: There is an error one of this page's template tags: <code>%s</code></small>" % e.message)


@register.inclusion_tag('replica/cms/components/_header.html', takes_context=True)
def componentHeader(context, user=None):
	request = context['request']
	u = request.user
	return {'user_obj':u, 'request':request }

@register.inclusion_tag('replica/dashboard/templatetags/month_links_snippet.html')
def render_dashboard_months(username):
	dates = Entry.objects.filter(user=username).dates('pub_date', 'month')
	return { 'dates': dates, }

@register.simple_tag
def render_counts(obj_type):
	if obj_type == 'topic':
		obj_count = Topic.objects.count()
	elif obj_type == 'published':
		obj_count = Entry.objects.published().count()
	elif obj_type == 'upcoming':
		obj_count = Entry.objects.upcoming().count()
	elif obj_type == 'idea':
		obj_count = Entry.objects.ideas().count()
	elif obj_type == 'channel':
		obj_count = Channel.objects.all().count()
	elif obj_type == 'media':
		obj_count = Media.objects.all().count()
	elif obj_type == 'page':
		obj_count = Entry.objects.pages().count()
	elif obj_type == 'entry':
		obj_count = Entry.objects.all().count()
	else:
		obj_count = '0'
	return obj_count

@register.simple_tag
def codeblock(slug):
	code = get_object_or_404(CodeBlock, type=2, slug=slug)
	template = Template(code.template_html)
	return template

@register.tag(name='render')
def render_django(parser, token):
    #Example: {% render flatpage.content %}
    content = token.split_contents()[-1]
    return RenderNode(content)
render_django.is_safe = True
