# -*- coding: utf-8 -*-

"""
pwdcheck.helpers
~~~~~~~~~~~~~~~~

"""


class Dotdict(dict):
    """dot.notation access to dict attributes."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
