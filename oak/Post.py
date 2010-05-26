# -*- coding: utf-8 -*-

import yaml
import codecs

HEADER_MARK = '---'

class Post(object):
    """
    Dummy class to hold the contents of a post file.
    A post file is a text file which must contain a YAML header
    defining its metadata, and it must be the first content
    of the file, for example:

    ---
      title: 'post title'
      author: 'post author name'
      pub_date: '2010-05-2 17:00:00'
    ---
    
    Post title
    ==========

    This is a sample post.

    Other dashes --- may appear here, obviously.


    As seen in the example, three dashes (---) determines the
    header start and end.

    """
    def __init__(self, f):
        try:
            _f = codecs.open(f, mode='r', encoding='utf-8')
        except:
            raise
        self.f = _f.read()
        if not self.f.startswith(HEADER_MARK):
            raise
        self.metadata = PostMetadata(self.f)
        self.post = self.f.split(HEADER_MARK, 2)[-1]

    def get_post(self):
        return self.post

    def get_metadata(self):
        return self.metadata

    def __dict__(self):
        d = {
            'post': self.get_post()
        }
        d.update(self.metadata.__dict__())
        return d

class PostMetadata(object):
    
    def __init__(self, metadata):
        """
        :param f: a string containing the full post's YAML header
        """
        if metadata.startswith(HEADER_MARK):
            metadata = metadata.split(HEADER_MARK, 2)[1]
        else:
            raise
        self.metadata = yaml.load(metadata)

    def __dict__(self):
        return self.metadata

