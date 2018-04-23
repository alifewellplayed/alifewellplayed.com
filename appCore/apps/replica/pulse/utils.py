import os
from PIL import Image
import markdown
import datetime
from time import strftime
from hashlib import md5
import uuid
from random import choice
import re

from io import StringIO, BytesIO

from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from coreExtend.models import Account

def create_thumbnail(name, image, content_type, thumb_size_x=250, thumb_size_y=2500):
    THUMBNAIL_SIZE = (thumb_size_x, thumb_size_y)
    if content_type == 'image/jpeg':
        PIL_TYPE = 'jpeg'
        FILE_EXTENSION = 'jpg'
    elif content_type == 'image/png':
        PIL_TYPE = 'png'
        FILE_EXTENSION = 'png'
    copy = image.copy()
    temp_handle = BytesIO()
    copy.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    copy.save(temp_handle, PIL_TYPE)
    temp_handle.seek(0)
    suf = SimpleUploadedFile(os.path.split(name)[-1], temp_handle.read(), content_type=content_type)
    return ('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf)


def guid_generator(base_id=None, length=24):
    if base_id:
        obj = get_object_or_404(Entry, pk=base_id)
        obj_time = obj.date_updated
        guid_base = "%s %s" % (base_id, obj_time)
        guid_encode = guid_base.encode('ascii', 'ignore')
        guid = md5(guid_encode).hexdigest()[:length]
    else:
        guid_base = str(uuid.uuid4())
        guid_encoded = guid_base.encode('ascii', 'ignore')
        guid = md5(guid_encoded).hexdigest()[:length]
    return guid


def username_generator(delimiter='-', tokenLength=4, tokenHex=False, tokenChars='0123456789'):
    """
    Generate Heroku-like random names to use in your applications.
    :param delimiter:
    :param tokenLength:
    :param tokenHex:
    :param tokenChars:
    :return: string
    """

    adjs = [
      'autumn', 'hidden', 'bitter', 'misty', 'silent', 'empty', 'dry', 'dark',
      'summer', 'icy', 'delicate', 'quiet', 'white', 'cool', 'spring', 'winter',
      'patient', 'twilight', 'dawn', 'crimson', 'wispy', 'weathered', 'blue',
      'billowing', 'broken', 'cold', 'damp', 'falling', 'frosty', 'green',
      'long', 'late', 'lingering', 'bold', 'little', 'morning', 'muddy', 'old',
      'red', 'rough', 'still', 'small', 'sparkling', 'throbbing', 'shy',
      'wandering', 'withered', 'wild', 'black', 'young', 'holy', 'solitary',
      'fragrant', 'aged', 'snowy', 'proud', 'floral', 'restless', 'divine',
      'polished', 'ancient', 'purple', 'lively', 'nameless', 'lucky', 'odd', 'tiny',
      'free', 'dry', 'yellow', 'orange', 'gentle', 'tight', 'super', 'royal', 'broad',
      'steep', 'flat', 'square', 'round', 'mute', 'noisy', 'hushy', 'raspy', 'soft',
      'shrill', 'rapid', 'sweet', 'curly', 'calm', 'jolly', 'fancy', 'plain', 'shinny'
    ]

    nouns = [
      'waterfall', 'river', 'breeze', 'moon', 'rain', 'wind', 'sea', 'morning',
      'snow', 'lake', 'sunset', 'pine', 'shadow', 'leaf', 'dawn', 'glitter',
      'forest', 'hill', 'cloud', 'meadow', 'sun', 'glade', 'bird', 'brook',
      'butterfly', 'bush', 'dew', 'dust', 'field', 'fire', 'flower', 'firefly',
      'feather', 'grass', 'haze', 'mountain', 'night', 'pond', 'darkness',
      'snowflake', 'silence', 'sound', 'sky', 'shape', 'surf', 'thunder',
      'violet', 'water', 'wildflower', 'wave', 'water', 'resonance', 'sun',
      'wood', 'dream', 'cherry', 'tree', 'fog', 'frost', 'voice', 'paper',
      'frog', 'smoke', 'star', 'atom', 'band', 'bar', 'base', 'block', 'boat',
      'term', 'credit', 'art', 'fashion', 'truth', 'disk', 'math', 'unit', 'cell',
      'scene', 'heart', 'recipe', 'union', 'limit', 'bread', 'toast', 'bonus',
      'lab', 'mud', 'mode', 'poetry', 'tooth', 'hall', 'king', 'queen', 'lion', 'tiger',
      'penguin', 'kiwi', 'cake', 'mouse', 'rice', 'coke', 'hola', 'salad', 'hat'
    ]

    if tokenHex:
        tokenChars = '0123456789abcdef'

    adj = choice(adjs)
    noun = choice(nouns)
    token = ''.join(choice(tokenChars) for _ in range(tokenLength))

    sections = [adj, noun, token]
    return delimiter.join(filter(None, sections))

def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


def DefaultUser():
    return uuid.uuid4
