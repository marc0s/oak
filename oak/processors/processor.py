# -*- coding: utf-8 -*-

from markdownprocessor import CodeBlockPreprocessor

import markdown

class Processor(object):
    """This class is the one responsible for processing the posts sources
    and generate the resulting HTML code.
    """

    def process(self, post):
        """This method is responsible of processing the post's markup into HTML.

        It must be redefined for the different markups that are going to be supported.
        The resulting HTML *must* be stored in post['html']

        If this Processor is used, the content is returned as is.

        :param post: the dict with the post to process
        :returns: dict
        """
        return post

class MarkdownProcessor(Processor):
    """The markdown syntax processor for oak posts.

    """

    def process(self, post):
        """The process method for Markdown posts.

        """
        if post.get('raw'):
            md = markdown.Markdown()
            md.preprocessors.insert(0, 'text', CodeBlockPreprocessor())
            post['html'] = md.convert(post.get('raw'))
        return post

