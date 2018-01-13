from django.conf import settings
from django.template import RequestContext, Context, Template
from django.shortcuts import render_to_response, render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse

from coreExtend.models import Account
from replica import settings as replicaSettings
from replica.pulse.models import Topic, Entry
from replica.pulse.mixins import PulseViewMixin

THEME = replicaSettings.SITE_THEME

#Default views
class IndexView(PulseViewMixin, ArchiveIndexView):
    template_name='themes/{0}/entry_archive.html'.format(THEME)
    pass

class YearArchiveView(PulseViewMixin, YearArchiveView):
    template_name='themes/{0}/entry_archive_year.html'.format(THEME)
    make_object_list = True
    pass

class MonthArchiveView(PulseViewMixin, MonthArchiveView):
    template_name='themes/{0}/entry_archive_month.html'.format(THEME)
    pass

class DayArchiveView(PulseViewMixin, DayArchiveView):
    template_name='themes/{0}/entry_archive_day.html'.format(THEME)
    pass

class ArchiveView(TemplateView):
    template_name='themes/{0}/archive.html'.format(THEME)

#@cache_page(60 * 15)
def EntryDetail(request, year, month, slug):
    #entry = get_object_or_404(Entry, pub_date__year=year, pub_date__month=month, slug=slug,).first()
    entry = Entry.objects.filter(pub_date__year=year, pub_date__month=month, slug=slug).first()
    variables = {'object': entry, 'detailed': True,}
    if request.user.is_staff or entry.is_published:
        if entry.template:
            template = Template(entry.template.template_html)
            context = RequestContext(request, variables)
            return HttpResponse(template.render(context))
        else:
            template = [
                'themes/{0}/entry/{1}.html'.format(THEME, entry.slug),
                'themes/{0}/entry_detail.html'.format(THEME),
                'replica/pulse/entries/%s.html' % entry.slug,
                'replica/pulse/entry_detail.html'
            ]
            return render(request, template, variables)
    else:
        raise PermissionDenied


#Entries for topic
class EntriesForTopic(ListView):
    paginate_by = replicaSettings.PAGINATE
    template_name='themes/{0}/topic_entry_list.html'.format(THEME)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs.pop('topic_slug'))
        return Entry.objects.published().filter(topic=self.topic).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(EntriesForTopic, self).get_context_data(**kwargs)
        context.update({'topic' : self.topic, 'is_topic': True,})
        return context

#List of public topics
class TopicsList(ListView):
    paginate_by = replicaSettings.PAGINATE_TOPICS
    template_name='themes/{0}/topic_list.html'.format(THEME)

    def get_queryset(self):
        return Topic.objects.public().order_by('title')

    def get_context_data(self, **kwargs):
        context = super(TopicsList, self).get_context_data(**kwargs)
        context.update({'topic': False, 'display_new_post': True,})
        return context

#Topic entry redirect
@cache_page(60 * 15)
def TopicEntry(request, topic_slug, guid):
    entry = get_object_or_404(Entry, topic__slug=topic_slug, guid=guid)
    return HttpResponseRedirect(entry.get_absolute_url())

@cache_page(60 * 15)
def EntryPage(request, url):
    if not url.startswith('/'):
        url = '/' + url
    try:
        if request.user.is_staff:
            page = get_object_or_404(Entry.objects.pages(), url=url)
        else:
            page = get_object_or_404(Entry.objects.pages_published(), url=url)
        if page.template:
            template = Template(page.template.template_html)
        else:
            template = [
                'themes/{0}/page/{1}.html'.format(THEME, page.slug),
                'themes/{0}/entry_page.html'.format(THEME),
                'replica/pulse/pages/%s.html' % page.slug,
                'replica/pulse/entry_page.html'
            ]
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            page = get_object_or_404(Entry.objects.pages(), url=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    variables = {'object': page, 'detailed': True,}
    return render(request, template, variables)
