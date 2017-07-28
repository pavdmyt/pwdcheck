# -*- coding: utf-8 -*-

"""
pwdcheck.helpers
~~~~~~~~~~~~~~~~

"""

import string
import unicodedata as ud


class Dotdict(dict):
    """dot.notation access to dict attributes."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def count_digits(s):
    # type: (str) -> int
    return sum([i in string.digits for i in s])


def count_ucase(s):
    # type: (str) -> int
    return sum([i.isupper() for i in s])


def count_lcase(s):
    # type: (str) -> int
    return sum([i.islower() for i in s])


def count_schars(s):
    # type: (str) -> int
    #
    # Unicode categories:
    #   https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    cats = ('Pc', 'Sc', 'Ps', 'Pe', 'Pd', 'Po', 'Sk', 'Sm', 'So')
    return sum([ud.category(i) in cats for i in s])
