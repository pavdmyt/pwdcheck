# -*- coding: utf-8 -*-

"""
pwdcheck.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of pwdcheck's exceptions.
"""


class PwdCheckError(Exception):
    """Basic exception for errors raised by pwdcheck."""


class ComplexityCheckError(PwdCheckError, ValueError):
    """Used for resp.exc objects."""

    def __init__(self, err_msg, **kwargs):
        super(ComplexityCheckError, self).__init__(err_msg)
        self.aval = kwargs.get("aval")
        self.pval = kwargs.get("pval")
        self.param_name = kwargs.get("param_name")
        self.policy_param_name = kwargs.get("policy_param_name")
