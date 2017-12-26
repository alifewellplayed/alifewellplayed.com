from django.conf import settings
import datetime

def template_settings(request):
    return {
        'network_name': settings.SITE_NAME,
        'network_desc': settings.SITE_DESC,
        'network_author': settings.SITE_AUTHOR,
        'network_url': settings.SITE_URL,
        'network_register': settings.ALLOW_NEW_REGISTRATIONS,
        'BASE_URL': 'http://' + request.get_host(),
        'BASE_HOST': request.get_host().split(':')[0],
    }

def template_times(request):
    return {
        'today': datetime.datetime.now(),
        'yesterday': datetime.datetime.now() - datetime.timedelta(1),
    }
