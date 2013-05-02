# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class AbstractEntry(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255,blank=True,)
    slug = models.SlugField(unique=True) 
    text = models.TextField(blank=True)
    
    class Meta:
        abstract=True

class Page(AbstractEntry):
    pass
# When a Page is deleted, mediafiles' content_type and object_id are still there.

#####
from mediafiles.models import MediaFile

class Entry(AbstractEntry):
    medias = models.ManyToManyField(MediaFile,
                    through='EntryMedia',
                    null=True,blank=True, default=None) 

class EntryMedia(models.Model):
    entry = models.ForeignKey(Entry)
    media = models.ForeignKey(MediaFile)

#####
class Blog(AbstractEntry):
    medias = models.ManyToManyField(MediaFile,
                    null=True,blank=True, default=None) 

