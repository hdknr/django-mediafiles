# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,Http404
#
from mediafiles.models import MediaFile
#
def media(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse )
