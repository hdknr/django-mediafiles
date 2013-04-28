# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timezone import now
from django.contrib.auth.models import User

import mimetypes
import hashlib
import os

def create_upload_path(self, filename):
    if self.created == None:
        self.created = now() 

    self.original_name = filename #: original flename
        
    ret =  "%s/%s/%s/%s" % ( 
        self.user.username if self.user else "_anyone_",
            self._meta.module_name,
            self.created.strftime("%y/%m/%d"),
                hashlib.md5(filename).hexdigest()+os.path.splitext(filename)[1].lower() ) 
    return ret 

class MediaFile(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,default=None,
            on_delete=models.SET_NULL,) 
    #:
    title = models.CharField(max_length=255,blank=True,)
    slug = models.SlugField(unique=True) 
    description = models.TextField(blank=True)
    #:
    data = models.FileField(upload_to=create_upload_path)
    mimetype= models.CharField(u'Mime Type',max_length=30,db_index=True,default='',blank=True, )
    #:
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #:
    created = models.DateTimeField(u'Created',default=now,null=False)
    updated = models.DateTimeField(u'Updated',auto_now=True)    

    def save(self,*args,**kwargs):
        super(MediaFile,self).save(*args,**kwargs)
        self.title= getattr(self,'original_name',None)
        self.mimetype = mimetypes.guess_type(self.data.name)[0]
        
        if self.title:
            self.__dict__.pop('original_name')
            self.save()

    def response(self,response_class):
        res = response_class(self.data,content_type=self.mimetype)
        res['Content-Disposition'] = 'attachment; filename=%s' % self.title
        return res
