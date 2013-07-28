# -*- coding: utf-8 -*-
from django import template
from django.template.loaders.filesystem import Loader
import os

DIR=[os.path.join( os.path.dirname( os.path.dirname( os.path.abspath(__file__) )),'templates')]

register = template.Library()

@register.simple_tag
def literal_include(template_name):
    return  Loader().load_template_source(template_name,DIR)[0]
