# -*- coding: utf-8 -*-

from markdownprocessor import CodeBlockPreprocessor

import markdown

class Processor(object):
    """This class is the one responsible for processing the posts sources
    and generate the resulting HTML code.
    """

    def process(self, data):
        """This method is responsible of processing the post's markup into HTML.

        It must be redefined for the different markups that are going to be supported.
        The resulting HTML *must* be stored in data['post']['html']

        If this Processor is used, the content is returned as is.

        :param data: the dict with the data to process.
        :returns: dict
        """
        return data

class MarkdownProcessor(Processor):
    """The markdown syntax processor for oak posts.

    """

    def process(self, data):
        """The process method for Markdown posts.

        """
        if data.get('post'):
            md = markdown.Markdown()
            md.preprocessors.insert(0, 'text', CodeBlockPreprocessor())
            data['post']['html'] = md.convert(data.get('post')['raw'])
        return data 

