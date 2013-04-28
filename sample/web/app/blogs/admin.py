# -*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.timezone import now

from models import *
from mediafiles.models import MediaFile

class ImageInline(generic.GenericTabularInline):
    model=MediaFile

class PageAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Page._meta.fields ])
    inlines = [
        ImageInline,
    ]
admin.site.register(Page,PageAdmin)

