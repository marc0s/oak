# -*- coding: utf-8 -*-
import os
from distutils.core import setup

def find_templates():
    _paths = []
    for r, d, f in os.walk('oak/layouts'):
        if len(f):
            for _f in f:
                _paths.append(r.strip('oak/') + '/' + _f)
    return _paths


setup(
    name='Oak',
    version='dev',
    url='http://github.com/marc0s/oak',
    author='marc0s',
    author_email='marc0s@fsfe.org',
    packages=['oak', 'oak.models', 'oak.processors', 'oak.utils'],
    package_data={'oak': ['scripts/manage.py', ] + find_templates() },
    scripts=['bin/oak-admin.py',],
    requires=['Jinja2','Markdown','PyYAML','Pygments'],
    license='WTFPL',
    description='A simple static-blog generator',
    long_description=open('README.md').read(),
)

