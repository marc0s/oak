# -*- coding: utf-8 -*-

import sys
import os
import logging

from optparse import OptionParser, OptionGroup

import oak

class Launcher(object):
    "The entrypoint for command line calls"

    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    logger = None
    settings = None

    def __init__(self, settings=None):
        self.settings = settings

    def setup_logging(self, loglevel='warning'):
        self.logger = logging.getLogger('oak')
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        ch.setFormatter(formatter)
        ch.setLevel(self.LOG_LEVELS[loglevel])
        self.logger.addHandler(ch)
        self.logger.setLevel(self.LOG_LEVELS[loglevel])

    def get_logger(self, loglevel='warning'):
        if not self.logger:
            self.logger = self.setup_logging(loglevel=loglevel)
        return self.logger
        
    def run(self, argv=None):
        parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")
        parser.add_option("-g", "--generate", action="store_true", dest="generate", default=False, help = "Generate the source for your site.")
        parser.add_option("--loglevel", dest="loglevel", default="warning", help="Set the log output level")

        group = OptionGroup(parser, "Output options (overriding settings.py)")
        group.add_option("-l", "--layout", dest="layout", default=self.settings.DEFAULT_LAYOUT, help="Set the layout to use")
        group.add_option("-d", "--destination", dest="destination", default=self.settings.OUTPUT_PATH, help="Set the destination of the output")
        parser.add_option_group(group)

        (options, args) = parser.parse_args()
        print(options.loglevel)

        self.setup_logging(loglevel=options.loglevel)

        if options.generate:
            # override settings with commandline options
            if options.layout:
                self.settings.DEFAULT_LAYOUT=options.layout
            if options.destination:
                self.settings.OUTPUT_PATH=options.destination
            # set the path to the layouts directory
            self.settings.LAYOUTS_PATH = os.path.sep.join([os.path.dirname(oak.__file__), self.settings.LAYOUTS_PATH])
            self.logger.debug("LAYOUTS_PATH set to %s" % (self.settings.LAYOUTS_PATH,))
            self.logger.info("Settings loaded.")
            # instantiate Oak with the given settings
            my_oak = oak.Oak(logger=self.logger, settings=self.settings)
            self.logger.info("Oak initiated.")
            # call the generation process
            my_oak.generate()
            self.logger.info("Geneartion completed.")
        else:
            parser.print_help()

