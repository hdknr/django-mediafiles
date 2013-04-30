from django.conf.urls import patterns, include, url 
from views import *

urlpatterns = patterns('',
    url('preview/(?P<id>.+)',preview,name='mediafiles_preview'),
    url('download/(?P<id>.+)',download,name='mediafiles_download'),
)
