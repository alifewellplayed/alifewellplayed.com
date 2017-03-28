from django.conf import settings

#Site Settings
SITE_NAME = getattr(settings, 'SITE_NAME', 'Replica')
SITE_DESC = getattr(settings, 'SITE_DESC', 'Just a copy of another content publishing platform.')
SITE_URL = getattr(settings, 'SITE_URL', 'http://localhost')
SITE_AUTHOR = getattr(settings, 'SITE_AUTHOR', 'Tyler')
DECK_ENTS = getattr(settings, 'REPLICA_DECK_ENTS', False)
PAGINATE = getattr(settings, 'REPLICA_PAGINATE', 25)
PAGINATE_TOPICS = getattr(settings, 'REPLICA_PAGINATE_TOPICS', 25)
THUMBNAIL_SMALL = getattr(settings, 'REPLICA_THUMBNAIL_SMALL', 250)
THUMBNAIL_LARGE = getattr(settings, 'REPLICA_THUMBNAIL_LARGE', 750)

#Plugins
PLUGIN_MICRO = getattr(settings, 'REPLICA_ENABLE_MICRO', True)
PLUGIN_WHISPER = getattr(settings, 'REPLICA_ENABLE_WHISPER', False)
PLUGIN_PUBLISHER = getattr(settings, 'REPLICA_ENABLE_PUBLISHER', True)

#THEME SETTINGS
SITE_THEME = getattr(settings, 'THEME_NAME', 'Exiled')
