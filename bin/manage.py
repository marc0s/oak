#!/usr/bin/env python

import sys
from oak.launcher import Launcher

try:
    import settings
except ImportError:
    print("No settings found. Have you run oak-admin.py --init?")
    sys.exit(1)

if __name__ == '__main__':
    launcher = oak.Launcher(settings=settings)
    launcher.run(sys.argv[1:])

