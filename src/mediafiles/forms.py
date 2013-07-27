# -*- coding: utf-8 -*- from django import forms

from django import forms
from django.conf import settings
from django.forms.models import modelformset_factory

from models import *

class MediaFileForm(forms.ModelForm):
    removing = forms.BooleanField(required=False,initial=False,)
    def __init__(self,*args,**kwargs):
        super(MediaFileForm,self).__init__(*args,**kwargs)
        self.fields['data'].widget = forms.FileInput()  #:diable "Currently" file url

    class Meta:
        model= MediaFile
        exclude = ['user','slug','name','mimetype',
                    'content_type','object_id','content_object',
                    'created','updated',]

class GalleryMediaFileForm(forms.ModelForm):
    ''' Galleryに追加するMediaFile '''
    class Meta:
        model= MediaFile
        exclude = ['user','slug','name','mimetype',
                    'content_type','object_id','content_object',
                    'created','updated',]

def media_formset(request,queryset,prefix='media',*args,**kwargs):
    
    if request == None or request.method=='GET':
        return modelformset_factory(MediaFile,form=MediaFileForm 
                        )(queryset=queryset,prefix=prefix,*args,**kwargs)
    else:
        return modelformset_factory(MediaFile,form=MediaFileForm
                        )(request.POST,request.FILES,
                          queryset=queryset,prefix=prefix,*args,**kwargs)

