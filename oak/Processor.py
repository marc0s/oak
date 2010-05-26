# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, FileSystemLoader
from Markdown import Markdown2Extension

class Processor(object):
    def __init__(self, tpl_path):
        self.env = Environment(loader=FileSystemLoader(tpl_path),extensions=[Markdown2Extension])

    def render(self, tpl_name, d):
        return self.env.get_template(tpl_name).render(d)

