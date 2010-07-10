# -*- coding: utf-8 -*-

class Oak(object):
    "The main class"

    logger = None
    settings = None

    def __init__(self, logger=None, settings=None):
        if logger:
            self.logger = logger
        if settings:
            self.settings = settings
            print(settings.FOO)

    def init(self, path=None):
        if path:
            pass
        else:
            logger.error('No path provided, refusing to initialize.')


    def generate(self, settings=None):
        pass


