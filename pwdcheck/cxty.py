# -*- coding: utf-8 -*-

"""
pwdcheck.cxty
~~~~~~~~~~~~~

Complexity class.
"""

from __future__ import absolute_import

import unicodedata as ud

# XXX: if cardinalizing only few words, better avoid boltons
from pwdcheck.boltons.strutils import cardinalize

from .compat import integer_types, json, str
from .exceptions import ComplexityCheckError, PolicyError
from .helpers import Dotdict, cached_property


# XXX: abstractclass for Complexity and Extras?
# TODO: add __str__ and __repr__
class Complexity(object):

    # policy-item-name -> param-name
    _pname_policy_map = {
        "minlen":       "length",
        "umin":         "uppercase",
        "lmin":         "lowercase",
        "dmin":         "digits",
        "omin":         "special",
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
        dct = Dotdict()

        for check_name in self.policy.keys():
            # Unsupported policy entry
            if check_name not in self._pname_policy_map.keys():
                raise PolicyError(
                    "unknown policy parameter '{0}'".format(check_name)
                )

            # Ensure :check_val is int
            check_val = self.policy[check_name]

            # `bool` is a subclass of `int`
            #
            # >>> bool.mro()
            # [bool, int, object]
            is_bool = type(check_val) is bool
            is_int = isinstance(check_val, integer_types)

            if is_bool or not is_int:
                raise PolicyError(
                    "{0}: non-int value set to '{1}' parameter"
                    .format(check_val, check_name)
                )

            # Process
            if check_val >= 0:
                func = self.func_map.get(check_name)
                out_name = self._pname_policy_map[check_name]
                dct[out_name] = self.make_resp_dict(func, check_name)

        return dct

    @cached_property
    def policy(self):
        if isinstance(self._policy, dict):
            return Dotdict(self._policy.get("complexity", {}))
        raise PolicyError("unsupported data type")

    def make_resp_dict(self, checker_func, policy_param_name):
        resp = Dotdict()

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

    @cached_property
    def func_map(self):
        return {
            "dmin":   self.make_counter('isdigit'),
            "umin":   self.make_counter('isupper'),
            "lmin":   self.make_counter('islower'),
            "omin":   self.count_special,
            "minlen": len,
        }

    @staticmethod
    def count_special(s):
        # type: (str) -> int
        #
        # Unicode categories:
        #   https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
        cats = ('Pc', 'Sc', 'Ps', 'Pe', 'Pd', 'Po', 'Sk', 'Sm', 'So')
        return sum([ud.category(i) in cats for i in str(s)])

    @staticmethod
    def make_counter(func_name):
        def count_func(s):
            return sum(
                [getattr(i, func_name)() for i in s]
            )
        return count_func
