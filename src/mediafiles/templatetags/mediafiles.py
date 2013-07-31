# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
#
register = template.Library()
#
@register.simple_tag
def preview(media,templatedir="mediafiles",*args,**kwargs ):
    try:
        t,sub = media.mimetype.split('/')
         
        return template.loader.get_template("%s/%s.html" % ( templatedir,t )).render(
                template.Context({'media':media,}) )
    except:
        return ""

@register.simple_tag(takes_context=True)
def make_delete_url(context,urlname,**kwargs ):
    p = context.get('mediafile_deleter_hint',{} )
    p.update(kwargs)
    return reverse(urlname, kwargs=p)
#
@register.simple_tag(takes_context=True)
def mediafile_delete_url(context,mediafile,**kwargs ):
    urlname = context.get('mediafile_delete_url','gallery_admin_media_delete')
    p = context.get('mediafile_url_hint',{} )
    p.update(kwargs)
    return reverse(urlname, kwargs=p)

@register.simple_tag(takes_context=True)
def mediafile_image_url(context,mediafile,**kwargs ):
    urlname = context.get('mediafile_image_url','mediafiles_preview')
    p = context.get('mediafile_url_hint',{} )
    p.update(kwargs)
    return reverse(urlname, kwargs=p)

@register.simple_tag(takes_context=True)
def mediafile_thumbnail_url(context,mediafile,**kwargs ):
    if mediafile.is_image() == False:
        return mediafile.get_thumbnail_url()

    urlname = context.get('mediafile_thumbnail_url','mediafiles_preview')
    p = context.get('mediafile_url_hint',{} )
    p.update(kwargs)
    return reverse(urlname, kwargs=p)
