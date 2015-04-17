import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import taggit_forms

setup(
    name='django-taggit-forms',
    version='.'.join(map(str, taggit_forms.VERSION)),
    packages=['taggit_forms'],
    include_package_data=True,
    license='MIT License',
    description='Tag-creation forms for django-taggit',
    long_description=README,
    url='https://github.com/akiraakaishi/django-taggit-forms',
    author='Akira Akaishi',
    author_email='akira.akaishi@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)