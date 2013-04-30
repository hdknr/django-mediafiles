# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
#
from models import MediaFile
#
def preview(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse )

def download(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse,meta=True )
