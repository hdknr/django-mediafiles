# -*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.timezone import now

from models import *
from mediafiles.models import MediaFile

class PageMediaInline(generic.GenericTabularInline):
    model=MediaFile

class PageAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Page._meta.fields ])
    inlines = [
        PageMediaInline,
    ]
admin.site.register(Page,PageAdmin)

#####

class EntryMediaInline(admin.TabularInline):
    model = EntryMedia

class EntryAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Entry._meta.fields ])
    inlines = [
        EntryMediaInline,
    ]
admin.site.register(Entry,EntryAdmin)

#####
class BlogMediaInline(admin.TabularInline ):
    model = Blog.medias.through


class BlogAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Blog._meta.fields ])
    exclude=['medias',]
    inlines = [
        BlogMediaInline,
    ]
admin.site.register(Blog,BlogAdmin)

