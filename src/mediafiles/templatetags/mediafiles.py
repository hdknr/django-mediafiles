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
