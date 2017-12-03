import os
import markdown
import datetime
import uuid
from PIL import Image
from time import strftime
from hashlib import md5
from io import StringIO, BytesIO

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, wordcount
from django.conf import settings
from django.urls import get_script_prefix
from django.utils.encoding import iri_to_uri
from django.contrib.sites.models import Site

from replica import settings as replicaSettings
from replica.uploads import *
from replica.pulse.utils import create_thumbnail

class Plugin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=replicaSettings.MAX_LENGTH)
    is_enabled = models.BooleanField(help_text=_("Check to enable plugin"), choices=replicaSettings.IS_SITE_CHOICES, default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'r_Plugin'
        verbose_name = "Plugin"
        verbose_name_plural = 'Plugins'
        ordering = ('slug',)
