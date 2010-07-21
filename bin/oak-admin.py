#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from oak.manager import Manager

if __name__ == '__main__':
    manager = Manager()
    manager.run(sys.argv[1:])

