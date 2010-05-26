# -*- coding: utf-8 -*-

import sys
import os
import glob

from optparse import OptionParser
from oak import Processor, Post

import settings

def main(argv):
    parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")
    parser.add_option("-g", "--generate", action = "store_true",
                        dest = "generate", default = False,
                        help = "Generate the source for your site.")
    parser.add_option("-l", "--layout", dest = "layout", default = settings.DEFAULT_LAYOUT)

    (options, args) = parser.parse_args()

    cwd = os.getcwdu()
    content = os.path.sep.join([cwd, settings.CONTENT_PATH])
    templates = os.path.sep.join([cwd, settings.LAYOUTS_PATH, options.layout])
    if options.generate:
        p = Processor.Processor(templates)
        print(" * Using %s as source of content" % (content,))
        print(" * Using '%s' as layout name" % (options.layout,))
        for f in glob.glob("%s/*.md" % (content,)):
            print(" * processing %s..." % (os.path.basename(f),))
            p.render('base',{'body': open(f).read()})
     

if __name__ == "__main__":
    main(sys.argv[1:])

