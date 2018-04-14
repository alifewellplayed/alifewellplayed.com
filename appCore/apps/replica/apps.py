from django.apps import AppConfig

### Core
class CoreConfig(AppConfig):
    name = 'replica.pulse'
    verbose_name = "Replica / Core"

class CMSConfig(AppConfig):
    name = 'replica.cms'
    verbose_name = "Replica / Site Settings"

class APIConfig(AppConfig):
    name = 'replica.api'
    verbose_name = "Replica / API"

### Plugins
class ZineConfig(AppConfig):
    name = 'replica.contrib.zine'
    verbose_name = "Replica / Plugins / Zine"

class RedirectionConfig(AppConfig):
    name = 'replica.contrib.redirection'
    verbose_name = "Replica / Plugins / Redirection"

class MicroConfig(AppConfig):
    name = 'replica.contrib.micro'
    verbose_name = "Replica / Plugins / Micro"

class InstaConfig(AppConfig):
    name = 'replica.contrib.insta'
    verbose_name = "Replica / Plugins / Insta"
