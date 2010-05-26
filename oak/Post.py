# -*- coding: utf-8 -*-

class PostMetadata(object):
    def __dict__(self):
        return {
            'title': self.title,
            'author': self.author,
            'pub_date': self.pub_date,
            'tags': self.tags,
            'layout': self.layout,
        }
