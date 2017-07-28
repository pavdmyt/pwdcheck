# -*- coding: utf-8 -*-

"""
pwdcheck.pwdcheck
~~~~~~~~~~~~~~~~~

"""

import json

import pwdcheck.helpers as h
from pwdcheck.boltons.strutils import cardinalize


PNAME_POLICY_MAP = {
    "minlen":       "length",
    "umin":         "uppercase",
    "lmin":         "lowercase",
    "dmin":         "digits",
    "omin":         "non-alphabetic",
}


EXTRAS_FUNC_MAP = {
    "palindrome": h.is_palindrome,
}


# TODO: @property -> @cached_property
class Complexity(object):

    def __init__(self, pwd, policy):
        self._pwd = pwd
        self._policy = policy.get("complexity", {})

    # There is no :from_yaml method since I don't want
    # to include PyYaml into deps. YAML support should
    # be handled in the client code.
    @classmethod
    def from_json(cls, pwd, json_policy_str):
        policy_data = json.loads(json_policy_str)
        return cls(pwd, policy_data)

    @property
    def as_dict(self):
        dct = h.Dotdict()
        dct.length = self.make_resp_dict(len, "minlen")
        dct.uppercase = self.make_resp_dict(h.count_ucase, "umin")
        dct.lowercase = self.make_resp_dict(h.count_lcase, "lmin")
        dct.digits = self.make_resp_dict(h.count_digits, "dmin")
        dct.schars = self.make_resp_dict(h.count_schars, "omin")
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

        # Don't make checks if param is (0, false) or not specified at all
        param = self.policy.get(policy_param_name)
        if not param:
            return resp  # empty dict

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


class Extras(object):

    def __init__(self, pwd, policy):
        self._pwd = pwd
        self._policy = policy.get("extras", {})

    # There is no :from_yaml method since I don't want
    # to include PyYaml into deps. YAML support should
    # be handled in the client code.
    @classmethod
    def from_json(cls, pwd, json_policy_str):
        policy_data = json.loads(json_policy_str)
        return cls(pwd, policy_data)

    @property
    def as_dict(self):
        dct = h.Dotdict()
        if not self.policy:
            return dct

        # Required checks
        req_checks = [
            check_name for check_name in self.policy.keys()
            if self.policy[check_name]
        ]

        for check_name in req_checks:
            func = EXTRAS_FUNC_MAP[check_name]
            dct[check_name] = func(self._pwd)

        return dct

    @property
    def policy(self):
        if isinstance(self._policy, dict):
            return h.Dotdict(self._policy)
        else:
            # accept obj's with attrs specified in
            # policy spec
            raise NotImplementedError


def _pwd_ok_check(dct):
    cxty_dct = dct.complexity
    extras_dct = dct.extras

    cxty_errs = [val.err for val in cxty_dct.values()]
    extras_errs = [val for val in extras_dct.values()]

    return not any(cxty_errs + extras_errs)


def check(pwd, policy, history=None, dct=None):
    if isinstance(policy, str):
        try:
            cxty = Complexity.from_json(pwd, policy)
            extras = Extras.from_json(pwd, policy)
        except ValueError as err:
            # TODO: implement pwdcheck.errors or exceptions
            raise NotImplementedError(err)
    elif isinstance(policy, dict):
        cxty = Complexity(pwd, policy)
        extras = Extras(pwd, policy)
    else:
        raise NotImplementedError("Unsupported policy data type")

    result = h.Dotdict()
    result.complexity = cxty.as_dict
    result.extras = extras.as_dict

    return _pwd_ok_check(result), result
