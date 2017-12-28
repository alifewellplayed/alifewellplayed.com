from __future__ import unicode_literals
from whitenoise.storage import CompressedManifestStaticFilesStorage

class StaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False
