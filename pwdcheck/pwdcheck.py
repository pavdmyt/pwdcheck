# -*- coding: utf-8 -*-

"""
pwdcheck.pwdcheck
~~~~~~~~~~~~~~~~~

"""

import pwdcheck.helpers as h
from pwdcheck.boltons.strutils import cardinalize


PNAME_POLICY_MAP = {
    "minlen":       "length",
    "umin":         "uppercase",
    "lmin":         "lowercase",
    "dmin":         "digits",
    "omin":         "non-alphabetic",
}


# TODO: @property -> @cached_property
class Complexity(object):

    def __init__(self, pwd, policy):
        self._pwd = pwd
        self._policy = policy

        # Results
        self.length = self.make_resp_dict(len, "minlen")
        self.ucase = self.make_resp_dict(h.count_ucase, "umin")
        self.lcase = self.make_resp_dict(h.count_lcase, "lmin")
        self.digits = self.make_resp_dict(h.count_digits, "dmin")
        self.schars = self.make_resp_dict(h.count_schars, "omin")

    @property
    def pwd_ok(self):
        return not any([
            self.length.err,
            self.ucase.err,
            self.lcase.err,
            self.digits.err,
            self.schars.err,
        ])

    @property
    def as_dict(self):
        dct = h.Dotdict()
        dct.length = self.length
        dct.uppercase = self.ucase
        dct.lowercase = self.lcase
        dct.digits = self.digits
        dct.schars = self.schars
        return dct

    @property
    def policy(self):
        if isinstance(self._policy, dict):
            return h.Dotdict(self._policy)
        else:
            # accept obj's with attrs specified in
            # policy spec
            raise NotImplementedError

    def make_resp_dict(self, checker_func, policy_param_name):
        resp = h.Dotdict()

        resp.aval = checker_func(self._pwd)                  # actual value
        resp.pval = getattr(self.policy, policy_param_name)  # policy value
        resp.err = resp.aval < resp.pval
        resp.param_name = PNAME_POLICY_MAP[policy_param_name]
        resp.policy_param_name = policy_param_name
        resp.err_msg = self.compose_err_msg(resp)
        # TODO: provide useful args for ValueError
        resp.exc = ValueError(resp.err_msg) if resp.err else None
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
            err_msg = "not yet ready!"
        return err_msg


def get_extras(pwd, history=None, dct=None):
    ext = h.Dotdict()
    ext.palindrome = h.is_palindrome(pwd)
    return ext


def check(pwd, policy, history=None, dct=None):
    result = h.Dotdict()
    result.complexity = Complexity(pwd, policy).as_dict
    result.extras = get_extras(pwd, history=history, dct=dct)
    return result
