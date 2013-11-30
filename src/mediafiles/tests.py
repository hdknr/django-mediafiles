# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase,client
from django.core.urlresolvers import reverse,resolve
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect,Http404

from urllib import urlparse,urlencode

from models import *

import os

class RootTest(TestCase):

    def setUp(self):
        #: site admins
        self.admins_name=[ 'admin1','admin2']
        self.admins = [ User.objects.get_or_create(
                            username=u,
                                is_staff=True,is_superuser=True,)[0] 
                           for u in self.admins_name ]
        
        #: users
        self.users_name=['member1','member2']
        self.users = [ User.objects.get_or_create(
                        username=u)[0]
                    for u in self.users_name ]

        #: password
        map(lambda u: u.set_password(u.username), self.users )
        map(lambda u: u.save(), self.users )
        map(lambda u: u.set_password(u.username), self.admins)
        map(lambda u: u.save(), self.admins)

    def auth(self,user=None):
        if user:
            self.assertTrue( User.objects.filter(id =user.id).exists() )
            self.assertTrue( self.client.login(username=user.username, password=user.username,) )

    def get(self,name,status_code=200,user=None,msg="Exception",query={},**kwargs):
        ''' response object
        '''
        self.auth( user )

        self.last_url = reverse( name,kwargs=kwargs )
        if query:
           self.last_url = self.last_url +"?" + urlencode(query) 
        response = self.client.get( self.last_url )
        self.assertEqual(response.status_code,status_code,msg)
        return response

    def post(self,name,status_code=200,user=None,msg="Exception",query={},form={},**kwargs):
        ''' response object
        '''
        self.auth( user )

        self.last_url = reverse( name,kwargs=kwargs )
        if query:
           self.last_url = self.last_url +"?" + urlencode(query) 
        response = self.client.post( self.last_url,form )
        self.assertEqual(response.status_code,status_code,msg)
        return response

class MediaFileTest(RootTest):

    def upload_file(self,gallery_id,image_file):
        response = None
        with open(image_file) as fp :
            response = self.post('gallery_admin_media_create', 
                        user =self.users[0], form={ 'data': fp, } ,id=gallery_id) 
        return response

    def download(self,url,target='/tmp', update=False):
        import  os
        import requests
        fname = os.path.join(target,url.split('/')[-1:][0] )
        if update or not os.path.isfile(fname):
            with open(fname, 'wb') as f:
                r = requests.get(url,stream=True)
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
        return fname

    def test_upload(self):
        ''' python manage.py test mediafiles.MediaFileTest.test_upload'''
       
        image_file = os.path.join(
                        os.path.dirname( 
                            os.path.abspath( __file__)), 'fixtures/papi.jpg') 

        g = Gallery()
        g.save()
                   
        self.assertEqual( g.medias.count(),0 )
        self.assertEqual( MediaFile.objects.count() ,0)
        response = self.upload_file( g.id, image_file )
        self.assertEqual( g.medias.count(),1 )
        self.assertEqual( MediaFile.objects.count() ,1)
       
        mediafile = MediaFile.objects.all()[0]
        self.assertEqual( mediafile.mimetype, 'image/jpeg')

        media_path = mediafile.data.path
        mediafile.delete()

        self.assertFalse( os.path.isfile( media_path ) )
        

    def test_pdf(self):
        ''' python manage.py test mediafiles.MediaFileTest.test_pdf'''
        url = "http://www.city.shibuya.tokyo.jp/city/saiyo/pdf/saiyo_annai.pdf" 
        pdf_file =self.download(url)

        g = Gallery()
        g.save()
                   
        self.assertEqual( g.medias.count(),0 )
        self.assertEqual( MediaFile.objects.count() ,0)
        response = self.upload_file( g.id, pdf_file )
        self.assertEqual( g.medias.count(),1 )
        self.assertEqual( MediaFile.objects.count() ,1)
       
        mediafile = MediaFile.objects.all()[0]
        self.assertEqual( mediafile.mimetype, 'application/pdf')

        media_path = mediafile.data.path
        print mediafile.data.path

        mediafile.pdf_to_images()

        import glob 
        from models import UPLOAD_TMP_DIR
        ext = "jpg" 
        jpgs = glob.glob( os.path.join(UPLOAD_TMP_DIR, "pdf.*.jpg" ))
        print jpgs
        jpg_medias = MediaFile.objects.filter(mimetype="image/jpeg" ) 

        #:ファイル名ルールチェック
        import re
        self.assertEqual(jpg_medias.count(), len(jpgs) )
        for p in jpg_medias:
            self.assertIsNotNone( re.search(r"pdf.%d.\d+.jpg" % mediafile.id, p.name ) )
    
        #:削除
        mediafile.delete()
        self.assertFalse( os.path.isfile( media_path ) )

    def save_pdf(self):
        ''' python manage.py test mediafiles.MediaFileTest.save_pdf'''
        url = "http://www.city.shibuya.tokyo.jp/city/saiyo/pdf/saiyo_annai.pdf" 
        pdf_file =self.download(url)

        m=MediaFile.create(pdf_file)

        self.assertEqual(MediaFile.objects.count(),1)
        self.assertEqual( m.mimetype, 'application/pdf')
        print  m.mimetype, m.data.path
        
    
    def test_thumbnail(self):
        ''' python manage.py test mediafiles.MediaFileTest.test_thumbnail'''

        image_file = os.path.join(
                        os.path.dirname( 
                            os.path.abspath( __file__)), 'fixtures/papi.jpg') 
        g = Gallery()
        g.save()

        response = self.upload_file( g.id, image_file )
        mediafile = MediaFile.objects.all()[0]

        from thumbs import cached_thumb
        ret = cached_thumb( mediafile.data )

        response = self.get("gallery_admin_media_thumb",
             id=g.id ,mid=mediafile.id,query={'width':100, 'height':30,})
        self.assertEqual(response['Content-Type'],"image/jpeg" )

        import hashlib
        hash_content = hashlib.md5( response.content).hexdigest()
        hash_file = hashlib.md5( open( mediafile.thumb_path(size=(100,30))).read() ).hexdigest() 
        self.assertEqual( hash_content,hash_file )
           
        response = self.get("mediafiles_thumbnail",id=mediafile.id, width=100, height=30)
        hash_content_2 = hashlib.md5( response.content).hexdigest()
        self.assertEqual( hash_content,hash_content_2)

        self.assertEqual(self.last_url , mediafile.get_thumbnail_url(size=(100,30) )  )

        #: clean image files
        mediafile.delete()
