# -*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.timezone import now

from models import *

class MediaFileAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in MediaFile._meta.fields ])
admin.site.register(MediaFile,MediaFileAdmin)

