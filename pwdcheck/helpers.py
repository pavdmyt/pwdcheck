# -*- coding: utf-8 -*-

"""
pwdcheck.helpers
~~~~~~~~~~~~~~~~

"""


class Dotdict(dict):
    """dot.notation access to dict attributes."""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class cached_property(object):
    """Decorator that converts a method with a single self argument
    into a property cached on the instance.
    """
    def __init__(self, fn):
        self.__fn = fn

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.__fn.__name__] = self.__fn(instance)
        return res
