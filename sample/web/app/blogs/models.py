# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255,blank=True,)
    slug = models.SlugField(unique=True) 
    description = models.TextField(blank=True)
