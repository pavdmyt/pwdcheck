# -*- coding: utf-8 -*-

"""
pwdcheck.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of pwdcheck's exceptions.
"""


class PwdCheckError(Exception):
    """Basic exception for errors raised by pwdcheck."""


class PolicyError(PwdCheckError):
    """Policy error occurred."""


class PolicyParsingError(PolicyError):
    """An error occurred while parsing policy data."""


class BaseCheckError(PwdCheckError, ValueError):
    """Base exception for *CheckError(s).

    Cathing this error will catch both:
    `pwdcheck.exceptions.ExtrasCheckError` and
    `pwdcheck.exceptions.ComplexityCheckError` errors.
    """

    def __init__(self, err_msg, **kwargs):
        super(BaseCheckError, self).__init__(err_msg)
        self.param_name = kwargs.get("param_name")
        self.policy_param_name = kwargs.get("policy_param_name")


class ExtrasCheckError(BaseCheckError):
    """An error occurred while checking :extras Policy section."""


class ComplexityCheckError(BaseCheckError):
    """An error occurred while checking :complexity Policy section."""

    def __init__(self, err_msg, **kwargs):
        super(ComplexityCheckError, self).__init__(err_msg, **kwargs)
        self.aval = kwargs.get("aval")
        self.pval = kwargs.get("pval")
