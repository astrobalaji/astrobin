# Django
from django.db import models

# AstroBin
from astrobin.models import Image

class ThumbnailGroup(models.Model):
    image = models.ForeignKey(
        Image,
        related_name = 'thumbnails',
    )

    revision = models.CharField(
        max_length = 1,
        default = '0',
    )

    real             = models.CharField(max_length = 512, null = True, blank = True)
    real_inverted    = models.CharField(max_length = 512, null = True, blank = True)
    hd               = models.CharField(max_length = 512, null = True, blank = True)
    hd_anonymized    = models.CharField(max_length = 512, null = True, blank = True)
    hd_inverted      = models.CharField(max_length = 512, null = True, blank = True)
    regular          = models.CharField(max_length = 512, null = True, blank = True)
    regular_inverted = models.CharField(max_length = 512, null = True, blank = True)
    gallery          = models.CharField(max_length = 512, null = True, blank = True)
    gallery_inverted = models.CharField(max_length = 512, null = True, blank = True)
    collection       = models.CharField(max_length = 512, null = True, blank = True)
    thumb            = models.CharField(max_length = 512, null = True, blank = True)
    revision         = models.CharField(max_length = 512, null = True, blank = True)
    histogram        = models.CharField(max_length = 512, null = True, blank = True)
    iotd             = models.CharField(max_length = 512, null = True, blank = True)
    iotd_candidate   = models.CharField(max_length = 512, null = True, blank = True)
    story            = models.CharField(max_length = 512, null = True, blank = True)
    duckduckgo       = models.CharField(max_length = 512, null = True, blank = True)
    duckduckgo_small = models.CharField(max_length = 512, null = True, blank = True)


    def __unicode__(self):
        return "Thumbnails for image %s" % self.image.title

    class Meta:
        app_label = 'astrobin_apps_images'
        unique_together = ('image', 'revision',)

