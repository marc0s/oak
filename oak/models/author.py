# -*- coding: utf-8 -*-

class Author(dict):
    def __init__(self, author, url='', posts=[]):
        self['author'] = author
        self['url'] = url
        self['posts'] = posts

