from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from coreExtend import views as core_views
from replica.pulse.sitemaps import PulseSitemap
from replica import settings as r_settings

from replica.contrib.micro.urls import MICRO_PULSE_URLS
from replica.contrib.redirection.urls import REDIRECTION_PULSE_URLS

admin.autodiscover()
admin.site.site_header = r_settings.SITE_NAME
sitemaps = {'news': PulseSitemap(),}

urlpatterns = [
    #admin
    url(r'^admin42/', include(admin.site.urls)),

    #API
    #url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/v2/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v2/', include('replica.api.urls', namespace='rest_replica')),

    # Static
    url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404_page"),
    url(r'^500/$', TemplateView.as_view(template_name="500.html"), name="500_page"),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),
    url(r'^manifest\.json$', TemplateView.as_view(template_name="manifest.json", content_type='application/json')),

    # Apps
    url(r'^replica/', include('replica.cms.urls', namespace='ReplicaAdmin')),
    url(r'notes/', include(MICRO_PULSE_URLS, namespace='ReplicaMicro')),
    url(r'^r/', include(REDIRECTION_PULSE_URLS, namespace='ReplicaRedirection')),
    url(r'^', include('coreExtend.urls', namespace='CoreExtend')),
    url(r'^', include('replica.pulse.urls', namespace='ReplicaPulse')),

    #Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
