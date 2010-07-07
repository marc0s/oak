# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Oak',
    version='0.1dev',
    packages=['oak', 'oak.models', 'oak.processors'],
    license='WTFPL',
    long_description=open('README').read(),
)

