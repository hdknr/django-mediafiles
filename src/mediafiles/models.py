# -*- coding: utf-8 -*-


class AbstractMedia(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    description = models.TextField(blank=True)
    created = models.DateTimeField(u'Created',default=now,null=False)
    updated = models.DateTimeField(u'Updated',auto_now=True)    
    class Meta:
        abstract = True
