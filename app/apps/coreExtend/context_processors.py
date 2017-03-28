from django.conf import settings
import datetime



def template_settings(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_desc': settings.SITE_DESC,
        'site_url': settings.SITE_URL,
        'site_register': settings.ALLOW_NEW_REGISTRATIONS,
        'BASE_URL': 'http://' + request.get_host(),
        'BASE_HOST': request.get_host().split(':')[0],
    }

def template_times(request):
    return {
        'today': datetime.datetime.now(),
        'yesterday': datetime.datetime.now() - datetime.timedelta(1),
    }
