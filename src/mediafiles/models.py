# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings

import mimetypes
import hashlib
import os
import uuid
from datetime import datetime
import time
import urllib

timestamp = lambda : int(time.mktime(datetime.now().timetuple()))

def create_upload_path(self, filename):
    if self.created == None:
        self.created = now() 

    self.original_name = filename #: original flename
    filename = filename.encode('utf8')      #: conver to ascii
        
    ret =  "%s/%s/%s/%s" % ( 
        self.user.username if self.user else "_anyone_",
            self._meta.module_name,
            self.created.strftime("%y/%m/%d"),
                hashlib.md5(filename).hexdigest()+os.path.splitext(filename)[1].lower() ) 
    return ret 

class MediaFile(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,default=None,
            verbose_name=_(u'User'),on_delete=models.SET_NULL,) 
    #:
    name  = models.CharField(_(u'Name'),max_length=255,blank=True,)
    title = models.CharField(_(u'Title'),max_length=255,blank=True,)
    slug = models.SlugField(_(u'Slug'),unique=True) 
    description = models.TextField(_(u'Description'),blank=True)
    #:
    data = models.FileField(_(u'Data File'),upload_to=create_upload_path)
    mimetype= models.CharField(_(u'Mime Type'),max_length=30,db_index=True,default='',blank=True, )
    #:
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #:
    created = models.DateTimeField(_(u'Created'),default=now,null=True)
    updated = models.DateTimeField(_(u'Updated'),auto_now=True)    

    def save(self,*args,**kwargs):

        if not self.slug or len(self.slug) <1:
            self.slug = slugify(self.title or uuid.uuid1().hex )
            n = MediaFile.objects.filter(slug=self.slug).count()
            if len(self.slug) < 1 or n > 0: 
                self.slug = self.slug + "-%d"% timestamp()

        super(MediaFile,self).save(*args,**kwargs)

        name= getattr(self,'original_name',None)

        if name:
            self.name = name
            self.mimetype = mimetypes.guess_type(self.data.name)[0]
            self.__dict__.pop('original_name')
            self.save()

    def response(self,response_class,meta=False):
        res = response_class(self.data,content_type=self.mimetype)
        if meta:
            res['Content-Disposition'] = 'attachment; filename=%s' % self.name
        return res

    def get_absolute_url(self):
        try:
            return reverse('mediafiles_preview',kwargs={'id': self.id ,} )
        except Exception,e:
            return None

    def get_thumbnail_url(self):
        if self.is_image():
            return self.get_absolute_url()
        return "%sico/%s.gif" % (settings.STATIC_URL,urllib.quote(self.mimetype) )

    def is_image(self):
        return self.mimetype.find("image") ==0

    def __unicode__(self):
        return self.title or self.name or  self.slug or self.id

    class Meta:
        verbose_name = _(u"Media File")
        verbose_name_plural = _(u"Media Files")

class Gallery(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,default=None,
            verbose_name = _(u'User'), on_delete=models.SET_NULL,) 

    name  = models.CharField(_(u'Name'),max_length=255,blank=True,)
    title = models.CharField(_(u'Title'),max_length=255,blank=True,)
    slug = models.SlugField(_(u'Slug'),unique=True) 
    description = models.TextField(_(u'Description'),blank=True)

    created = models.DateTimeField(_(u'Created'),default=now,null=False)
    updated = models.DateTimeField(_(u'Updated'),auto_now=True)    

    medias = models.ManyToManyField(MediaFile,verbose_name = _(u"Media Files"),
                    null=True,blank=True, default=None) 

    def __unicode__(self):
        return self.title or self.name or self.slug

    class Meta:
        verbose_name = _(u"Gallery")
        verbose_name_plural = _(u"Galleries")
