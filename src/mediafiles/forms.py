# -*- coding: utf-8 -*- from django import forms

from django import forms
from django.conf import settings

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
