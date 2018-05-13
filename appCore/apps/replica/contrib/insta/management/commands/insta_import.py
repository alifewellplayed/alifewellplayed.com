import requests
from urllib.parse import urlparse
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify, wordcount
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django import template
from django.core.files.base import ContentFile
from django.core import files

from replica.pulse.models import Media
from replica.contrib.insta.models import Instagram
from coreExtend.models import Account

from replica.contrib.insta import settings
from replica.contrib.insta.scraper import instagram_profile_json, instagram_profile_obj


def get_profile_media(profile, page = 0):
    """
    Parse a generated media object
    :param profile:
    :param page:
    :return:
    """
    #return profile['entry_data']['ProfilePage'][page]['user']['media']['nodes']
    edges = profile['entry_data']['ProfilePage'][page]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    return [edge['node'] for edge in edges]

class Command(BaseCommand):
    help = 'Import instagram photos into media'

    def add_arguments(self, parser):
        parser.add_argument('instagram_username', type=str)

    def handle(self, *args, **options):
        insta_user = options['instagram_username']
        user_obj = get_object_or_404(Account, username=insta_user)
        profile_data = instagram_profile_obj(insta_user)
        media_list = get_profile_media(profile_data)
        print('importing from {0} user'.format(insta_user))
        #print(media_list)
        for media_obj in media_list:
            try:
                media_id = media_obj['id']
                insta_media = Instagram.objects.get(instagram_id=media_id)
                try:
                    MediaInstance.caption = media_obj['caption']
                except KeyError:
                    pass
                MediaInstance.url = media_obj['shortcode']
                MediaInstance.content_type=3
                img_url = media_obj['thumbnail_src']
                name = urlparse(img_url).path.split('/')[-1]
                response = requests.get(img_url)
                if response.status_code == 200:
                    MediaInstance.image.save(name, ContentFile(response.content), save=True)
                MediaInstance.save()
                print('updating #{0}'.format(media_obj['id']))
            except Instagram.DoesNotExist:
                try:
                    insta_caption = media_obj['caption']
                except KeyError:
                    insta_caption = ''
                MediaInstance = Instagram(
                    instagram_id=media_obj['id'],
                    title = 'Instagram #{0}'.format(media_obj['id']),
                    slug=slugify(media_obj['id']),
                    caption=insta_caption,
                    user=user_obj,
                    #url=media_obj['shortcode'],
                    url = 'https://instagram.com/p/'.format(media_obj['shortcode']),
                    content_type=3 #For Instagram
                )
                img_url = media_obj['thumbnail_src']
                name = urlparse(img_url).path.split('/')[-1]
                response = requests.get(img_url)
                if response.status_code == 200:
                    MediaInstance.image.save(name, ContentFile(response.content), save=True)

                MediaInstance.save()
                print('importing #{0}'.format(media_obj['id']))
