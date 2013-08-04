# -*- encoding: utf-8 -*-
"""
django-thumbs on-the-fly
https://github.com/madmw/django-thumbs

A fork of django-thumbs [http://code.google.com/p/django-thumbs/] by Antonio Melé [http://django.es].

"""
import cStringIO
from django.core.files.base import ContentFile
import os

DEFAULT_SIZE=(120,90)
try:
    from PIL import Image, ImageOps
except ImportError:
    # Mac OSX
    import Image, ImageOps

def generate_thumb(original, size=DEFAULT_SIZE, preserve_ratio=True, use_cache=True,format='JPEG'):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail

    Arguments:
    original        -- The image being resized as `File`.
    size            -- Desired thumbnail size as `tuple`. Example: (70, 100) (Width,Height)
    preserve_ratio  -- True if the thumbnail is to keep the aspect ratio of the full image
    format          -- Format of the original image ('JPEG', 'PNG', ...) The thumbnail will be generated using this same format.

    """
    size = DEFAULT_SIZE if any([size==None, len(size) != 2, 0 in size ]) else size
    original.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(original)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    if preserve_ratio:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
    io = cStringIO.StringIO()
    if format.upper() == 'JPG':
        format = 'JPEG'
    image.save(io, format)
    return ContentFile(io.getvalue())

def get_cached_file( data, size ):
    base,ext = os.path.splitext(data.path) 
    return  "%s.%sx%s%s" % ( base,size[0],size[1],ext)

def cached_thumb(original, size=DEFAULT_SIZE, preserve_ratio=True, format='JPEG'):
    size = DEFAULT_SIZE if any([size==None, len(size) != 2, 0 in size ]) else size
    cached_path = get_cached_file(original,size)
    if os.path.isfile(cached_path):
        return ContentFile( open(cached_path).read())
    new_thumb= generate_thumb(original,size,preserve_ratio,format) 
    original.storage.save(cached_path,new_thumb) 
    return new_thumb
