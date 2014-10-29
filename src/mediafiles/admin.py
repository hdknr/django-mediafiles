# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Gallery, MediaFile


class MediaFileAdmin(admin.ModelAdmin):
    list_display = tuple([
        f.name for f in MediaFile._meta.fields])
    raw_id_fields = ['user', ]

admin.site.register(MediaFile, MediaFileAdmin)


class GalleryMediaInline(admin.TabularInline):
    model = Gallery.medias.through


class GalleryAdmin(admin.ModelAdmin):
    list_display = tuple([
        f.name for f in Gallery._meta.fields])
    exclude = ['medias', ]
    inlines = [
        GalleryMediaInline,
    ]
admin.site.register(Gallery, GalleryAdmin)
