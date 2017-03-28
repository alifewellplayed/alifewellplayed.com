import datetime
import hashlib

from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

GENDER_CHOICES = (
	('F', _('Female')),
	('M', _('Male')),
	('P', _('Pirate')),
	('N', _('Ninja')),
	('R', _('Robot')),
	('O', _('Other')),
)

class Account(AbstractUser):

    #Profile Settings
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=500, blank=True)

    #Misc Settings
    hide_mobile = models.BooleanField(default=False)
    last_seen_on = models.DateTimeField(default=datetime.datetime.now)
    preferences = models.TextField(default="{}")
    view_settings = models.TextField(default="{}")
    send_emails = models.BooleanField(default=False)
    is_beta	= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        db_table = 'Account'

    def hash(self):
        hashed = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return hashed

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
