# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Oak',
    version='0.1dev',
    url='http://github.com/marc0s/oak',
    author='marc0s',
    author_email='marc0s@fsfe.org',
    packages=['oak', 'oak.models', 'oak.processors', 'oak.utils'],
    license='WTFPL',
    long_description=open('README').read(),
)

