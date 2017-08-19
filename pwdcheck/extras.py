# -*- coding: utf-8 -*-

"""
pwdcheck.extras
~~~~~~~~~~~~~~~

Extras class.
"""

import json

from .exceptions import DataTypeError, ExtrasCheckError, PolicyError
from .helpers import Dotdict, cached_property


# TODO: add __str__ and __repr__
class Extras(object):

    # policy-item-name -> param-name
    _pname_policy_map = {
        "palindrome":       "palindrome",
        "in_dictionary":    "dictionary",
        "in_blacklist":     "blacklist",
        "in_history":       "history",
    }

    def __init__(self, pwd, policy,
                 pwd_dict=None, pwd_blacklist=None, pwd_history=None):
        self._pwd = pwd
        self._policy = policy
        self._pwd_dict = pwd_dict if pwd_dict else []                 # type: List[str]  # noqa
        self._pwd_blacklist = pwd_blacklist if pwd_blacklist else []  # type: List[str]  # noqa
        self._pwd_history = pwd_history if pwd_history else []        # type: List[str]  # noqa

    # There is no :from_yaml method since I don't want
    # to include PyYaml into deps. YAML support should
    # be handled in the client code.
    @classmethod
    def from_json(cls, pwd, json_policy_str,
                  pwd_dict=None, pwd_blacklist=None, pwd_history=None):
        policy_data = json.loads(json_policy_str)
        inst = cls(
            pwd,
            policy_data,
            pwd_dict=pwd_dict,
            pwd_blacklist=pwd_blacklist,
            pwd_history=pwd_history,
        )
        return inst

    @cached_property
    def as_dict(self):
        dct = Dotdict()

        for check_name in self.policy.keys():
            func = self.func_map.get(check_name)
            dct[check_name] = self.make_resp_dict(func, check_name)

        return dct

    @cached_property
    def policy(self):
        if isinstance(self._policy, dict):
            return Dotdict(self._policy.get("extras", {}))
        raise PolicyError("unsupported data type")

    def make_resp_dict(self, checker_func, policy_param_name):
        resp = Dotdict()

        # Skip unknown (unsupported) entries and
        # Don't make checks if param is (0, false) or not specified at all
        param = self.policy.get(policy_param_name)
        if not (param and checker_func):
            return resp  # empty dict

        resp.err = checker_func(self._pwd)
        resp.param_name = self._pname_policy_map[policy_param_name]
        resp.policy_param_name = policy_param_name
        resp.err_msg = self.compose_err_msg(resp)
        resp.exc = ExtrasCheckError(
            resp.err_msg,
            param_name=resp.param_name,
            policy_param_name=resp.policy_param_name,
        ) if resp.err else None

        return resp

    @staticmethod
    def compose_err_msg(resp_obj):
        if not resp_obj.err:
            return ""

        if resp_obj.policy_param_name == "palindrome":
            err_msg = "password is a palindrome"
        else:
            err_msg = "password found in {0}".format(resp_obj.param_name)

        return err_msg

    @cached_property
    def dictionary(self):
        # type: () -> List[str]
        return self._compose_pwd_list(self._pwd_dict, "dictionary")

    @cached_property
    def blacklist(self):
        # type: () -> List[str]
        return self._compose_pwd_list(self._pwd_blacklist, "blacklist")

    @cached_property
    def history(self):
        # type: () -> List[str]
        return self._compose_pwd_list(self._pwd_history, "history")

    def _compose_pwd_list(self, arg_items, policy_obj_name):
        # type: (List[str], str) -> List[str]
        #
        # Merge password list provided by constructor's argument (if any)
        # with password list provided by policy file (if any)
        #
        # :param arg_items:       list of passwords provided as argument
        #                         into the class constructor
        # :param policy_obj_name: name of the object which lists passwords
        #                         in the policy file
        assert policy_obj_name in ("dictionary", "blacklist", "history")

        try:
            pwd_list = list(arg_items)
        except TypeError:
            map_ = {
                "dictionary": "pwd_dict",
                "blacklist":  "pwd_blacklist",
                "history":    "pwd_history",
            }
            raise DataTypeError(
                "object provided by '{}' is not iterable"
                .format(map_[policy_obj_name])
            )

        # Dictionary provided in policy file
        # XXX: may raise AttributeError if provided non-dict :policy
        #      doesn't call :policy property
        pwds_from_policy = self._policy.get(policy_obj_name, [])

        # Use `set` to avoid duplicates
        return list(set(pwd_list + pwds_from_policy))

    @cached_property
    def func_map(self):
        return {
            "palindrome": self.is_palindrome,
            "in_dictionary": self.in_item_list(self.dictionary),
            "in_blacklist": self.in_item_list(self.blacklist),
            "in_history": self.in_item_list(self.history),
        }

    @staticmethod
    def is_palindrome(s):
        # type: (str) -> bool

        # The following is valid:
        # - the empty string is a palindrome
        # - a string constituted only by a single character is a palindrome
        # - palindrome checks are case-insensitive
        s = s.lower()
        return s == s[::-1]

    @staticmethod
    def in_item_list(item_list):
        def func(s):
            for i in item_list:
                if s == i:
                    return True
            return False
        return func
