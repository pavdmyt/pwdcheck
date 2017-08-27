# -*- coding: utf-8 -*-

"""
pwdcheck.cxty
~~~~~~~~~~~~~

Complexity class.
"""

from __future__ import absolute_import

import json
import string
import unicodedata as ud

# XXX: if cardinalizing only few words, better avoid boltons
from pwdcheck.boltons.strutils import cardinalize

from .compat import str
from .exceptions import ComplexityCheckError, PolicyError
from .helpers import Dotdict, cached_property


# TODO: invesigate json imports:
# try:
#     import simplejson as json
# except ImportError:
#     import json


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
    return sum([ud.category(i) in cats for i in str(s)])


# XXX: abstractclass for Complexity and Extras?
# TODO: add __str__ and __repr__
class Complexity(object):

    # policy-item-name -> param-name
    _pname_policy_map = {
        "minlen":       "length",
        "umin":         "uppercase",
        "lmin":         "lowercase",
        "dmin":         "digits",
        "omin":         "non-alphabetic",
    }

    def __init__(self, pwd, policy):
        self._pwd = pwd
        self._policy = policy

    # There is no :from_yaml method since I don't want
    # to include PyYaml into deps. YAML support should
    # be handled in the client code.
    @classmethod
    def from_json(cls, pwd, json_policy_str):
        policy_data = json.loads(json_policy_str)
        return cls(pwd, policy_data)

    @cached_property
    def as_dict(self):
        # XXX: align with Extras.as_dict (all params handled in loop)
        dct = Dotdict()
        dct.length = self.make_resp_dict(len, "minlen")
        dct.uppercase = self.make_resp_dict(count_ucase, "umin")
        dct.lowercase = self.make_resp_dict(count_lcase, "lmin")
        dct.digits = self.make_resp_dict(count_digits, "dmin")
        dct.schars = self.make_resp_dict(count_schars, "omin")
        return dct

    @cached_property
    def policy(self):
        if isinstance(self._policy, dict):
            return Dotdict(self._policy.get("complexity", {}))
        raise PolicyError("unsupported data type")

    def make_resp_dict(self, checker_func, policy_param_name):
        resp = Dotdict()

        # Don't make checks if param is (0, false) or not specified at all
        param = self.policy.get(policy_param_name)
        if not param:
            return resp  # empty dict

        resp.aval = checker_func(self._pwd)                  # actual value
        resp.pval = getattr(self.policy, policy_param_name)  # policy value
        resp.err = resp.aval < resp.pval
        resp.param_name = self._pname_policy_map[policy_param_name]
        resp.policy_param_name = policy_param_name
        resp.err_msg = self.compose_err_msg(resp)
        resp.exc = ComplexityCheckError(
            resp.err_msg,
            aval=resp.aval,
            pval=resp.pval,
            param_name=resp.param_name,
            policy_param_name=resp.policy_param_name,
        ) if resp.err else None

        return resp

    @staticmethod
    def compose_err_msg(resp_obj):
        if not resp_obj.err:
            return ""

        if resp_obj.policy_param_name == "dmin":
            cval = cardinalize("numeral", resp_obj.pval)
        else:
            cval = cardinalize("character", resp_obj.pval)
        base_msg = "password must contain at least"

        if resp_obj.policy_param_name in ("minlen", "dmin"):
            err_msg = "{0} {1} {2}, {3} given".format(
                base_msg, resp_obj.pval, cval, resp_obj.aval
            )
        elif resp_obj.policy_param_name in ("umin", "lmin", "omin"):
            err_msg = "{0} {1} {2} {3}, {4} given".format(
                base_msg, resp_obj.pval, resp_obj.param_name,
                cval, resp_obj.aval
            )
        else:
            raise NotImplementedError

        return err_msg
