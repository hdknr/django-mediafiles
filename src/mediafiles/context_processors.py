# -*- coding: utf-8 -*-

from datetime import datetime
from django.core.urlresolvers import reverse
from django.conf import settings

DEFAULT_CONTEXT={
    "GALLERY_BASE" : "base.html",
    "GALLERY_CONTENT" : "content",
}
def context(request):
    return getattr(settings,'GALLERY_CONTEXT',DEFAULT_CONTEXT)
