# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255,blank=True,)
    slug = models.SlugField(unique=True) 
    description = models.TextField(blank=True)
# When a Page is deleted, mediafiles' content_type and object_id are still there.

from mediafiles.models import MediaFile

class Entry(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255,blank=True,)
    slug = models.SlugField(unique=True) 
    description = models.TextField(blank=True)
    medias = models.ManyToManyField(MediaFile,
                    through='EntryMedia',
                    null=True,blank=True, default=None) 

class EntryMedia(models.Model):
    entry = models.ForeignKey(Entry)
    media = models.ForeignKey(MediaFile)
