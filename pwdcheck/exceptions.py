# -*- coding: utf-8 -*-

"""
pwdcheck.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of pwdcheck's exceptions.
"""


class PwdCheckError(Exception):
    """Basic exception for errors raised by pwdcheck."""


class BaseCheckError(PwdCheckError, ValueError):
    """Base exception for *CheckError(s)."""

    def __init__(self, err_msg, **kwargs):
        super(BaseCheckError, self).__init__(err_msg)
        self.param_name = kwargs.get("param_name")
        self.policy_param_name = kwargs.get("policy_param_name")


class ExtrasCheckError(BaseCheckError):
    """Used for resp.exc objects of the Extras class."""


class ComplexityCheckError(BaseCheckError):
    """Used for resp.exc object of the Complexity class."""

    def __init__(self, err_msg, **kwargs):
        super(ComplexityCheckError, self).__init__(err_msg, **kwargs)
        self.aval = kwargs.get("aval")
        self.pval = kwargs.get("pval")
