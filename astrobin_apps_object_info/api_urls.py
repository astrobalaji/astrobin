# Django
from django.conf.urls import patterns, url, include
from django.views.generic import *

# This app
from astrobin_apps_object_info.views.query import QueryView

urlpatterns = patterns('',
    url(r"query/(?P<objname>.+)?$", QueryView.as_view(), name = 'astrobin_apps_object_info.query'),
)
