# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
#
from models import MediaFile,Gallery
from forms import GalleryMediaFileForm
#
def preview(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse )

def download(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse,meta=True )

#######

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import CreateView, DeleteView, UpdateView, ListView,DetailView
from django.contrib.auth.decorators import login_required, permission_required

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class GalleryAdminDetail(DetailView):
    model = Gallery

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['id'] )

    def get_context_data(self, **kwargs):
        '''
            {'mediafiles': <django.db.models.fields.related.ManyRelatedManager object >
             'object': <Gallery: Gallery object>, 
             'gallery': <Gallery: Gallery object>, 
             'form': <django.forms.models.GalleryForm object >, 
             'view': <mediafiles.views.GalleryAdminEdit object > }
        '''
        context = super(GalleryAdminDetail, self).get_context_data(**kwargs)
        context['mediafiles'] = self.object.medias 
        return context

class GalleryAdminList(ListView):
    '''
    Template(by default):  mediafiles/gallery_list.html
    '''
    model = Gallery

class GalleryAdminMediaCreate(CreateView):
    model = MediaFile
    form_class = GalleryMediaFileForm

#    def get(self,request,*args,**kwargs):  #: for debugging
#        print "HDKNR:", "Ajax?",request.is_ajax()
#        response = super(GalleryAdminEdit,self).get(request,*args,**kwargs)
#        if request.is_ajax():
#            print response.render()
#        return response

#    def post(self, request, *args, **kwargs):      #: for debugging
#        print "HDKNR:post()","Ajax?=",request.is_ajax()
#        print args,kwargs,request.POST,request.FILES
#        response = super(GalleryAdminMediaCreate,self).post(request,*args,**kwargs)
#        return response

#    def form_invalid(self,form):
#        print "HDKNR(form_invalid):",type(form),form.errors
#        return super(GalleryAdminMediaCreate,self).form_invalid(form)
        
    def form_valid(self, form):
        print "HDKNR(form_valid):",dir(self)
        form.instance.user = self.request.user      #:ログインユーザー
        new_media = form.save()
        Gallery.objects.get(id=self.kwargs['id']).medias.add( new_media )  
#        self.object = form.save()

#        f = self.request.FILES.get('file')
        data = [{'name': new_media.name, 
#                'url': settings.MEDIA_URL + "pictures/" + new_media.name.replace(" ", "_"), 
#                'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 
#                'delete_url': reverse('upload-delete', args=[self.object.id]), 
#                'delete_type': "DELETE"
                }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

GalleryAdminDetailView = login_required(GalleryAdminDetail.as_view())
GalleryAdminListView = login_required(GalleryAdminList.as_view())
GalleryAdminMediaCreateView = login_required(GalleryAdminMediaCreate.as_view())
