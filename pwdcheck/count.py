# -*- coding: utf-8 -*-

"""
pwdcheck.count
~~~~~~~~~~~~~~

"""

import string
import unicodedata as ud


def digits(symbols):
    return sum([i in string.digits for i in symbols])


def uppercase(symbols):
    return sum([i.isupper() for i in symbols])


def lowercase(symbols):
    return sum([i.islower() for i in symbols])


def schars(symbols):
    # Unicode categories:
    #   https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    cats = ('Pc', 'Sc', 'Ps', 'Pe', 'Pd', 'Po', 'Sk', 'Sm', 'So')
    return sum([ud.category(i) in cats for i in symbols])
