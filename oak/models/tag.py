# -*- coding: utf-8 -*-

class Tag(dict):
    def __init__(self, tag, url='', posts=[]):
        self['tag'] = tag
        self['url'] = url
        self['posts'] = posts

