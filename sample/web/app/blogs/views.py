# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
#
import uuid
#
from models import Blog
from forms import BlogForm
from mediafiles.models import MediaFile
from mediafiles.forms import MediaFileForm,media_formset
#
def media(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse )

def media_preview(request,id):
    return render_to_response('blogs/media/preview.html',
            {'media': MediaFile.objects.get(id=id) },
            context_instance=template.RequestContext(request))
            
def blog_edit_simple(request,id):
    blog = Blog.objects.get(id=id)

    if request.method == "GET":
        form = BlogForm(instance=blog,prefix='blog')
        media_form = MediaFileForm(prefix='media')
    else:
        form = BlogForm(request.POST,instance=blog,prefix='blog')
        media_form = MediaFileForm(
            request.POST,request.FILES,prefix='media')

        if form.is_valid() :
            form.save()

        if media_form.is_valid():
            media_form.instance.user = request.user
            media_form.instance.slug = uuid.uuid1().hex
            media_form.save()
            blog.medias.add(media_form.instance)
            media_form = MediaFileForm(prefix='media')

    return render_to_response('blogs/blog/edit_simple.html',
            {'form': form,'media_form':media_form, },
        context_instance=template.RequestContext(request))

def blog_edit_formset(request,id):
    blog = Blog.objects.get(id=id)

    form = BlogForm(request.POST if request.method =="POST" else None ,
                    instance=blog,prefix='blog')
    medias = media_formset(request,blog.medias.all())

    if request.method == "POST":

        if form.is_valid() :
            form.save()

        if medias.is_valid():
            for media in medias.forms:
                if media.is_valid() and media.instance.data:
                    if media.cleaned_data.get('removing',False):
                        blog.medias.remove(media.instance)
                    else:
                        media.instance.user = request.user if request.user.is_authenticated() else None
                        media.save()
                        blog.medias.add(media.instance)
        else:
            #: error handling
            print medias.errors

            #: for increase medias.extra_forms after adding new mediafile

        medias = media_formset(None,blog.medias.all())

    return render_to_response('blogs/blog/edit_formset.html',
            {'form': form,'medias':medias, },
        context_instance=template.RequestContext(request))

def blog_edit(request,id):
    return blog_edit_formset(request,id)
