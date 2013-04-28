#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2013 HDKNR.COM
#
#  Licensed under the Simplified BSD License;
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.freebsd.org/copyright/freebsd-license.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import sys
import os
import glob
from setuptools import setup
#
sys.path.insert(0, os.path.abspath('src'))

# - Meta Info
from mediafiles import get_version

NAME='django-mediafiles'
DESCRIPTION=''
PACKAGES=['mediafiles',]
SCRIPTS=glob.glob('src/scripts/*.py')
URL='https://github.com/hdknr/django-mediafiles.git'
#
try:
    INSTALL_REQUIRES=[ r for r in open('requirements.txt').read().split('\n') if len(r)>0]
except:
    INSTALL_REQUIRES=[] 

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__=='__main__':
    setup(
        name = NAME,
        version = get_version(),
        license = 'Simplfied BSD License',
        author = 'HDKNR',
        author_email = 'gmail [at] hdknr.com',
        maintainer = 'Lafoglia,Inc.',
        maintainer_email = 'gmail [at] hdknr.com',
        url = URL,
        download_url = URL,
        description = 'Media files operation for django',
        long_description = read('README.rst'),
        platforms=['any'],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Simplifed BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
#        package_dir = {'': 'src'},
        packages = PACKAGES,
        include_package_data = True,
        zip_safe = False,
        scripts=SCRIPTS,
    )
