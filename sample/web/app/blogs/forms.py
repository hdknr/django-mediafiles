# -*- coding: utf-8 -*-

from django import forms
from django.forms import fields, models, formsets, widgets

from models import Blog,Entry
from mediafiles.models import MediaFile

class BlogForm(forms.models.ModelForm):
    class Meta:
        model = Blog
        exclude=['medias',]

class EntryForm(forms.models.ModelForm):
    class Meta:
        model = Entry
        exclude=['medias',]
