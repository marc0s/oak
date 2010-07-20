# -*- coding: utf-8 -*-

import yaml
import codecs

import oak.processors as procs

HEADER_MARK = '---'

class PostError(Exception):
    """Custom exception for invalid posts."""
    def __init__(self, msg):
        self.msg = msg


class Post(dict):
    """
    A class to hold the contents of a post file.
    A post file is a text file which must contain a YAML header
    defining its metadata, and it must be the first content
    of the file, for example:

    ---
      title: 'post title'
      author: 'post author name'
      pub_date: '2010-05-02 17:00:00'
      tags: ['tag1','tag2',...]
    ---
    
    Post title
    ==========

    This is a sample post.

    Other dashes --- may appear here, obviously.


    As seen in the example, three dashes (---) determines the
    header start and end.

    """
    def __init__(self, f, metadata, processor=None):
        """The Post class __init__

        :param f: the path to the post file
        :param metadata: default metadata dict
        :param processor: the processor to render post's contents
        :processor type: class

        :raises: PostError
        """
        try:
            _f = codecs.open(f, mode='r', encoding='utf-8')
        except:
            raise PostError('Unable to open file. Hint: isn\'t it UTF-8 encoded?')
        
        # Set metadata to the app defaults
        self['metadata'] = metadata.copy()
        self.f = _f.read()
        if not self.f.startswith(HEADER_MARK):
            raise PostError('Post file invalid, no header found.')
        _, metadata, self['raw'] = self.f.split(HEADER_MARK, 2)
        # update the metadata with the header's contents
        self['metadata'].update(yaml.load(metadata))
        # TODO auto determine processor based on metadata['markup']
        if processor:
            p = processor()
            self = p.process(self)

