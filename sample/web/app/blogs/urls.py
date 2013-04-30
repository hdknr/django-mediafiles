from django.conf.urls import patterns, include, url 
from views import *

urlpatterns = patterns('',
    url('blog/(?P<id>.+)/edit',blog_edit,name="blogs_blog_edit",),
    url('media/preview/(?P<id>.+)',media_preview,name='blogs_media_preview'),
    url('media/(?P<id>.+)',media,name='blogs_media'),
)
