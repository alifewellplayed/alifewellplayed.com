import datetime

from django.conf import settings
from django.shortcuts import render_to_response, render, get_object_or_404, redirect

from coreExtend.models import Account
from replica.pulse.models import Entry, Media, Channel, Topic, Draft, MenuPosition, MenuItem, SiteSettings

def currentSite(request):
    current_site_id = settings.SITE_ID
    current_site = get_object_or_404(SiteSettings, pk=current_site_id)
    if current_site.featured:
        site_featured_image = current_site.featured.image.url
    else:
        site_featured_image = None
    if current_site.logo:
        site_logo = current_site.logo.image.url
    else:
        site_logo = None

    return {
        'site_id': current_site.id,
        'site_name': current_site.name,
        'site_domain': current_site.domain,
        'site_description': current_site.description,
        'site_summary': current_site.summary_html,
        'site_enabled': current_site.is_enabled,
        'site_author': current_site.author,
        'site_created': current_site.date_created,
        'site_updated': current_site.date_updated,
        'site_logo': site_logo,
        'site_featured_image': site_featured_image,
    }
