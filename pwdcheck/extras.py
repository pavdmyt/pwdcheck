# -*- coding: utf-8 -*-

"""
pwdcheck.extras
~~~~~~~~~~~~~~~

Extras class.
"""

import json

from pwdcheck.helpers import Dotdict


class Extras(object):

    def __init__(self, pwd, policy, pwd_dict=None):
        self._pwd = pwd
        self._policy = policy
        self._pwd_dict = pwd_dict if pwd_dict else []

    # There is no :from_yaml method since I don't want
    # to include PyYaml into deps. YAML support should
    # be handled in the client code.
    @classmethod
    def from_json(cls, pwd, json_policy_str):
        policy_data = json.loads(json_policy_str)
        return cls(pwd, policy_data)

    @property
    def dictionary(self):
        # Merge password dict (not hash map!) provided by
        # constructor's :pwd_dict with password dict provided
        # by policy file (if any)

        types = (list, set, tuple)
        if self._pwd_dict and isinstance(self._pwd_dict, types):
            pwd_dict = list(self._pwd_dict)
        else:
            pwd_dict = self._pwd_dict

        # Dictionary provided in policy file
        dict_from_policy = self._policy.get("dictionary", [])

        # Use `set` to avoid duplicates
        return list(set(pwd_dict + dict_from_policy))

    @property
    def as_dict(self):
        dct = Dotdict()
        if not self.policy:
            return dct

        # Required checks
        req_checks = [
            check_name for check_name in self.policy.keys()
            if self.policy[check_name]
        ]

        for check_name in req_checks:
            func = self.func_map[check_name]
            dct[check_name] = func(self._pwd)

        return dct

    @property
    def policy(self):
        if isinstance(self._policy, dict):
            return Dotdict(self._policy.get("extras", {}))
        else:
            # accept obj's with attrs specified in
            # policy spec
            raise NotImplementedError

    @property
    def func_map(self):
        return {
            "palindrome": self.is_palindrome,
            "in_dictionary": self.in_dict,
        }

    @staticmethod
    def is_palindrome(s):
        # type: (str) -> bool
        return s == s[::-1]

    def in_dict(self, s):
        # type: (str) -> bool
        for i in self.dictionary:
            if s == i:
                return True
        return False
