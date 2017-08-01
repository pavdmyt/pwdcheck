# -*- coding: utf-8 -*-

"""
Make pwdcheck absolute imports possible in example scripts.
"""

import os
import sys


def pip_install_hook():
    dashes = "-" * 3
    print("{0} Installing latest pwdcheck code:".format(dashes))
    this_dir = os.path.dirname(os.path.realpath(__file__))
    pwdcheck_dir = os.path.dirname(this_dir)
    os.system("pip install -e {0}".format(pwdcheck_dir))
    print("{0} Running example:\n".format(dashes))


if "--skip-upd" not in sys.argv:
    pip_install_hook()
