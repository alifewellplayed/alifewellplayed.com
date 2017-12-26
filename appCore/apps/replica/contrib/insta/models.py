import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, wordcount
from django.conf import settings

from replica.pulse.models import Media
from replica import settings as replicaSettings

def upload_media(instance, filename):
    ext = filename.split('.')[-1]
    #filename = "%s.%s" % (instance.slug, ext)
    date = instance.date_created
    datepath_path = datetime.date.today().strftime("%Y/%m/%d")
    path = 'media/instagram/%s/%s' % (datepath_path, filename)
    #overwrite_existing(path)
    return path

class Instagram(Media):
    instagram_id = models.CharField(max_length=replicaSettings.MAX_LENGTH, unique=True)

    class Meta:
        db_table = 'r_instagram'
        verbose_name_plural = 'Instagram Media'
