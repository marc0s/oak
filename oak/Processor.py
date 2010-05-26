# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, FileSystemLoader
from markdownprocessor import CodeBlockPreprocessor

import markdown
import codecs

class Processor(object):
    def __init__(self, tpl_path):
        self.env = Environment(loader=FileSystemLoader(tpl_path))

    def render(self, tpl_name, d, output=None):
        # pre-process markdown first
        if d.get('post'):
            md = markdown.Markdown()
            md.preprocessors.insert(0, 'text', CodeBlockPreprocessor())
            d['post'] = md.convert(d.get('post'))
        if not output:
            return self.env.get_template(tpl_name).render(d)
        return False

