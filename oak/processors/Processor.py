# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, FileSystemLoader
from markdownprocessor import CodeBlockPreprocessor

import markdown
import codecs
import time

def datetimeformat(value, oformat='%Y-%m-%d', iformat="%Y-%m-%d %H:%M:%S"):
    return time.strftime(oformat, time.strptime(str(value), iformat))

def my_date(value=None, oformat='a', iformat='%Y-%m-%d %H:%M:%S'):
    """
    oformat values:
     'a': Dow, month dom, year
     'b': month dom, year
     ...
    """
    days = {
        0: ['Mon', 'Monday'],
        1: ['Tue', 'Tuesday'],
        2: ['Wed', 'Wednesday'],
        3: ['Thu', 'Thursday'],
        4: ['Fri', 'Friday'],
        5: ['Sat', 'Saturday'],
        6: ['Sun', 'Sunday'],
    }
    months = {
        1: ['Jan', 'January'],
        2: ['Feb', 'February'],
        3: ['Mar', 'March'],
        4: ['Apr', 'April'],
        5: ['May', 'May'],
        6: ['Jun', 'June'],
        7: ['Jul', 'July'],
        8: ['Aug', 'August'],
        9: ['Sep', 'September'],
        10: ['Oct', 'October'],
        11: ['Nov', 'November'],
        12: ['Dec', 'December'],
    }
    
    d = time.strptime(str(value), iformat)
    if oformat == 'a':
        return "%s, %s %s, %s" % (days[d.tm_wday][1], months[d.tm_mon][1], d.tm_mday, d.tm_year)
    if oformat == 'b':
        return "%s %s, %s" % (months[d.tm_mon][0], d.tm_mday, d.tm_year)

def longdate(value):
    return my_date(value, 'a')

def shortdate(value):
    return my_date(value, 'b')

class Processor(object):
    """This class is the one responsible for processing the posts sources
    and generate the resulting HTML code.
    """
    def __init__(self, tpl_path):
        self.env = Environment(loader=FileSystemLoader(tpl_path))
        self.env.filters['datetimeformat'] = datetimeformat
        self.env.filters['longdate'] = longdate
        self.env.filters['shortdate'] = shortdate

    def render(self, tpl_name, d, output=None):
        # TODO be able to choose the markup language: Markdown, reST, Textile
        # pre-process markdown first
        if d.get('post'):
            md = markdown.Markdown()
            md.preprocessors.insert(0, 'text', CodeBlockPreprocessor())
            d['post']['html'] = md.convert(d.get('post')['raw'])
        if not output:
            return self.env.get_template(tpl_name).render(d)
        return False

