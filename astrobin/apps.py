# Django
from django.apps import AppConfig
from django.db.utils import IntegrityError, ProgrammingError, OperationalError


class AstroBinAppConfig(AppConfig):
    name = 'astrobin'
    verbose_name = 'AstroBin'

    def registerActStreamModels(self):
        from actstream import registry
        registry.register('auth.user')
        registry.register('astrobin.gear')
        registry.register('astrobin.telescope')
        registry.register('astrobin.camera')
        registry.register('astrobin.mount')
        registry.register('astrobin.filter')
        registry.register('astrobin.software')
        registry.register('astrobin.accessory')
        registry.register('astrobin.focalreducer')
        registry.register('astrobin.image')
        registry.register('astrobin.imagerevision')
        registry.register('rawdata.PublicDataPool')
        registry.register('rawdata.RawImage')
        registry.register('nested_comments.nestedcomment')
        registry.register('reviews.review')
        registry.register('toggleproperties.toggleproperty')
        registry.register('astrobin_apps_groups.group')

    def ready(self):
        from astrobin.signals import *
        from astrobin_apps_notifications.signals import *
        from rawdata.signals import *

        self.registerActStreamModels()