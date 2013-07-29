# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
#
from models import MediaFile,Gallery
from forms import GalleryMediaFileForm
import uuid
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
        context['salt'] =  uuid.uuid1().hex
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
        form.instance.user = self.request.user      #:ログインユーザー
        new_media = form.save()

        self.gallery = Gallery.objects.get(id=self.kwargs['id'])    #: 別なところで
        self.gallery.medias.add( new_media )  

#        f = self.request.FILES.get('file')
        url = reverse('mediafiles_preview',kwargs={'id': new_media.id ,} )
        
        #: jquery file upload API data (JSON)
        data = [{'name': new_media.name, 
                'url': url,
                'thumbnail_url': url,
                'delete_url': reverse('gallery_admin_media_delete', 
                    kwargs={'id':self.kwargs['id'], 'mid':new_media.id,} ),
                'delete_type': "DELETE"
                }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

class GalleryAdminMediaDelete(DeleteView):
    model = MediaFile

    def get_object(self,*args,**kwargs):
        return Gallery.objects.get(id=self.kwargs['id'] ).medias.get(id=self.kwargs['mid'])

    def delete(self, request, *args, **kwargs):
        """ 
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()        #:削除
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect( 
            reverse( 'gallery_admin_detail',kwargs={'id': self.kwargs['id'],} ) )

GalleryAdminDetailView = login_required(GalleryAdminDetail.as_view())
GalleryAdminListView = login_required(GalleryAdminList.as_view())
GalleryAdminMediaCreateView = login_required(GalleryAdminMediaCreate.as_view())
GalleryAdminMediaDeleteView = login_required(GalleryAdminMediaDelete.as_view())
