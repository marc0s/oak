# -*- coding: utf-8 -*-
"Helper functions for oak"

import datetime
import hashlib
import os
import shutil
import time

def copytree_(src, dst):
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                copytree_(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error), why:
            raise Exception(why)
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        raise Exception(why)

class Filters:
    @staticmethod
    def datetimeformat(value, oformat='%Y-%m-%d', iformat="%Y-%m-%d %H:%M:%S"):
        return time.strftime(oformat, time.strptime(str(value), iformat))

    @staticmethod
    def my_date(value=None, oformat='a', iformat='%Y-%m-%d %H:%M:%S'):
        """
            oformat values:
            'a': Dow, month dom, year
            'b': month dom, year
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
        if oformat == 'c':
            return datetime.datetime.fromtimestamp(time.mktime(d)).isoformat()

    @staticmethod
    def longdate(value):
        return Filters.my_date(value, 'a')

    @staticmethod 
    def shortdate(value):
        return Filters.my_date(value, 'b')

    @staticmethod
    def isodate(value):
        return Filters.my_date(value, 'c')

class Atom(object):
    """Class for Atom-related stuff.
    """

    @staticmethod
    def gen_id(string):
        h = hashlib.new('sha1')
        h.update(string)
        return h.hexdigest()

    @staticmethod
    def blog_id(string):
        h = hashlib.new('sha1')
        h.update(string)
        return h.hexdigest()

