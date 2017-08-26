# -*- coding: utf-8 -*-

"""
pwdcheck.compat
~~~~~~~~~~~~~~~

py2/py3 compatibility support.
"""

import sys


PY2 = sys.version_info[0] == 2


if PY2:
    builtin_str = str
    str = unicode  # noqa
    bytes = str
else:
    builtin_str = str
    str = str
    bytes = bytes
