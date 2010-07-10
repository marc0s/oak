# -*- coding: utf-8 -*-

import sys
import os
import logging

from optparse import OptionParser

from oak import Oak

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

    def setup_logging(self, loglevel=LOG_LEVELS['warning']):
        self.logger = logging.getLogger('oak')
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        ch.setFormatter(formatter)
        ch.setLevel(loglevel)
        self.logger.addHandler(ch)
        self.logger.setLevel(loglevel)

    def get_logger(self, loglevel=LOG_LEVELS['warning']):
        if not self.logger:
            self.logger = self.setup_logging(loglevel=loglevel)
        return self.logger
        
    def run(self, argv=None):
        parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1-alpha")
        parser.add_option("-i", "--init", action="store_true", dest="init", default=False, help="Initialize the environment.")
        parser.add_option("-g", "--generate", action="store_true", dest="generate", default=False, help = "Generate the source for your site.")
        parser.add_option("-l", "--layout", dest="layout", default=settings.DEFAULT_LAYOUT, help="Set the layout to use")
        parser.add_option("-d", "--destination", dest="destination", default=settings.OUTPUT_PATH, help="Set the destination of the output")
        parser.add_option("--loglevel", dest="loglevel", default="warning", help="Set the log output level")

        (options, args) = parser.parse_args()

        logger = self.setup_logging(loglevel=options.loglevel)

        oak = Oak(logger=logger, settings=settings)

        if options.init:
            oak.init(path=os.path.getcwdu())
        elif options.generate:
            # override settings with commandline options
            if options.layout:
                settings.DEFAULT_LAYOUT=options.layout
            if options.destination:
                settings.OUTPUT_PATH=options.destination
            # call the generation process
            oak.generate()
        else:
            parser.print_help()

