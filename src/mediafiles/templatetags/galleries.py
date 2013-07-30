# -*- coding: utf-8 -*-
from django import template
from django.template.loaders.filesystem import Loader
import os

DIR=[os.path.join( os.path.dirname( os.path.dirname( os.path.abspath(__file__) )),'templates')]

register = template.Library()

@register.simple_tag
def literal_include(template_name):
    return  Loader().load_template_source(template_name,DIR)[0]

@register.simple_tag
def gallery_download_script(template_name='mediafiles/uploader/download_script.html' ):
    return literal_include(template_name)

@register.simple_tag
def gallery_upload_script(template_name='mediafiles/uploader/upload_script.html' ):
    return literal_include(template_name)

@register.inclusion_tag("mediafiles/uploader/js.html",takes_context=True)
def gallery_include_js(context):
    return context

@register.inclusion_tag("mediafiles/uploader/css.html" ,takes_context=True)
def gallery_include_css(context):
    return context

@register.inclusion_tag("mediafiles/uploader/uploader.html" ,takes_context=True)
def gallery_include_uploader(context,mediafile_uploder=None, data_field=None):
    context['mediafile_uploader'] = context.get('mediafile_uploader',mediafile_uploder or '' )
    context['data_field'] = context.get('data_field', data_field or 'data' )
    return context

@register.inclusion_tag("mediafiles/uploader/modal.html",takes_context=True)
def gallery_include_preview(context):
    return context
