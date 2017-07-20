# -*- coding: utf-8 -*-

"""
pwdcheck.pwdcheck
~~~~~~~~~~~~~~~~~

"""

import pwdcheck.count as count
from pwdcheck.helpers import Dotdict


# TODO: @property -> @cached_property
class Inspector(object):

    def __init__(self, pwd, policy):
        self._pwd = pwd
        self._policy = policy
        self._dict = Dotdict()

        # Results
        self.length = self.make_resp_dict(len, "minlen")
        self.ucase = self.make_resp_dict(count.uppercase, "umin")
        self.lcase = self.make_resp_dict(count.lowercase, "lmin")
        self.digits = self.make_resp_dict(count.digits, "dmin")
        self.schars = self.make_resp_dict(count.schars, "omin")

    @property
    def as_dict(self):
        self._dict.pwd_ok = self.pwd_ok
        self._dict.length = self.length
        self._dict.uppercase = self.ucase
        self._dict.lowercase = self.lcase
        self._dict.digits = self.digits
        self._dict.schars = self.schars
        return self._dict

    @property
    def policy(self):
        if isinstance(self._policy, dict):
            return Dotdict(self._policy)
        else:
            # accept obj's with attrs specified in
            # policy spec
            raise NotImplementedError

    def make_resp_dict(self, checker_func, policy_param_name):
        res = Dotdict()
        res.val = checker_func(self._pwd)
        res.err = res.val < getattr(self.policy, policy_param_name)
        return res

    @property
    def pwd_ok(self):
        return not any([
            self.length.err,
            self.ucase.err,
            self.lcase.err,
            self.digits.err,
            self.schars.err,
        ])


def check(pwd, policy):
    ins = Inspector(pwd, policy)
    return ins.as_dict
