# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
#
from models import Blog
from forms import BlogForm
from mediafiles.models import MediaFile
#
def media(request,id):
    m = MediaFile.objects.get(id=id )
    return m.response( HttpResponse )

def media_preview(request,id):
    return render_to_response('blogs/media/preview.html',
            {'media': MediaFile.objects.get(id=id) },
            context_instance=template.RequestContext(request))
            

def blog_edit(request,id):
    blog = Blog.objects.get(id=id)

    if request.method == "GET":
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(request.POST,instance=blog)

        if form.is_valid() and formset.is_valid():
            form.save()

    return render_to_response('blogs/blog/edit.html',
            {'form': form, },
        context_instance=template.RequestContext(request))
