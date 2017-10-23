from django.conf import settings

#Site Settings
SITE_NAME = getattr(settings, 'SITE_NAME', 'Replica')
SITE_DESC = getattr(settings, 'SITE_DESC', 'Just a copy of another content publishing platform.')
SITE_URL = getattr(settings, 'SITE_URL', 'http://localhost')
SITE_AUTHOR = getattr(settings, 'SITE_AUTHOR', 'Tyler Rilling')
DECK_ENTS = getattr(settings, 'REPLICA_DECK_ENTS', False)
PAGINATE = getattr(settings, 'REPLICA_PAGINATE', 25)
PAGINATE_TOPICS = getattr(settings, 'REPLICA_PAGINATE_TOPICS', 25)
THUMBNAIL_SMALL = getattr(settings, 'REPLICA_THUMBNAIL_SMALL', 250)
THUMBNAIL_LARGE = getattr(settings, 'REPLICA_THUMBNAIL_LARGE', 750)

#Plugins
PLUGIN_MICRO = getattr(settings, 'REPLICA_ENABLE_MICRO', True)
PLUGIN_WHISPER = getattr(settings, 'REPLICA_ENABLE_WHISPER', False)
PLUGIN_ZINE = getattr(settings, 'REPLICA_ENABLE_ZINE', True)
PLUGIN_INSTA = getattr(settings, 'REPLICA_ENABLE_INSTA', True)
PLUGIN_REDIRECTION = getattr(settings, 'REPLICA_ENABLE_REDIRECTION', True)

#THEME SETTINGS
SITE_THEME = getattr(settings, 'THEME_NAME', 'Exiled')

MAX_LENGTH = 510
CONTENT_FORMAT_CHOICES = ((u'markdown', u'Markdown'), (u'html', u'Raw HTML'),)
IS_ACTIVE_CHOICES = ((True, 'Published'), (False, 'Draft'))
CAN_SUBMIT_CHOICES = ((True, 'Everyone'), (False, 'Only users I allow.'))
IS_PUBLIC_CHOICES = ((True, 'Everyone'), (False, 'No one'))
MEDIA_TYPE_CHOICES = ((0, 'embed'), (1, 'image'), (2, 'url'), (3, 'Instagram'))
IS_SITE_CHOICES = ((True, 'Enabled'), (False, 'Disabled'))
CODE_TYPE_CHOICES = ((1, 'Partial'),(2, 'Page Template'),)

ICON_CHOICES = (
    ('fa fa-home', 'Home'),
    ('fa fa-pencil-square-o', 'Posts'),
    ('fa fa-book', 'Notes'),
    ('fa fa-tags', 'Topics'),
    ('fa fa-code-fork', 'Channels'),
    ('fa fa-file-image-o', 'Media'),
    ('fa fa-cogs', 'Gears'),
)
