from django.conf.urls import patterns, include, url 
from views import *

urlpatterns = patterns('',
    url('preview/(?P<id>.+)',preview,name='mediafiles_preview'),
    url('download/(?P<id>.+)',download,name='mediafiles_download'),

    url('gallery/admin/(?P<id>\d+)/media/create',GalleryAdminMediaCreateView, name='gallery_admin_media_create'),
    url('gallery/admin/(?P<id>\d+)/media/(?P<mid>\d+)/delete',GalleryAdminMediaDeleteView, name='gallery_admin_media_delete'),
    url('gallery/admin/(?P<id>\d+)/media/(?P<mid>\d+)/image',GalleryAdminMediaImageView, name='gallery_admin_media_image'),
    url('gallery/admin/(?P<id>\d+)',GalleryAdminDetailView, name='gallery_admin_detail'),
    url('gallery/admin/',GalleryAdminListView, name='gallery_admin_list'),
)
