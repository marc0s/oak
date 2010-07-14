# -*- coding: utf-8 -*-
"""Oak manager

This class provides the utils to manage the initialization
of new oak projects.

It's pretended to be called from oak-admin.py:

$ oak-admin.py --init <foo>

Its main function is to create the <foo> directory for holding
the blog and copying the default settings.py and other stuff to
the project directory.

"""

import os
import shutil

from optparse import OptionParser

import oak

class Manager(object):
    def __init__(self):
        pass

    def init(self, path):
        """This method creates the needed directories and the settings
        module to be customized as well as the manage.py launcher."""
        # check the path does not already exists
        if os.path.exists(path):
            raise Exception("Refusing to overwrite an existing path.")
        
        # create the base project path and other dirs
        os.makedirs(path)
        os.makedirs(os.path.sep.join([path, 'content'])) # where content is created
        os.makedirs(os.path.sep.join([path, 'site'])) # where blog is generated

        # obtain where the oak module is located and copy settings.py and manage.py
        oak_path = os.path.dirname(oak.__file__)
        shutil.copy2(os.path.sep.join([oak_path, 'settings.py']), path)
        shutil.copy2(os.path.sep.join([oak_path, 'scripts', 'manage.py']), path)
        print("""
        You may now want to edit your %s/settings.py file and initialize the git
        repository on %s.
        """ % (path, path))

    def run(self, argv):
        parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")
        parser.add_option("-i", "--init", dest="init", default=None, help="Initialize project")
        (options, args) = parser.parse_args()

        if options.init:
            path = os.path.abspath(options.init)
            self.init(path=path)


