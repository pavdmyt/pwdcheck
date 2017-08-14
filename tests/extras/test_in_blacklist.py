# -*- coding: utf-8 -*-

"""
tests.extras.test_in_blacklist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `in_blacklist` check.
"""

import pytest

from pwdcheck.exceptions import DataTypeError, ExtrasCheckError
from pwdcheck.extras import Extras


#
# Test Extras.as_dict out for in_blacklist checks
#
def test_false_in_blacklist(false_in_blacklist_policy):
    # "in_blacklist": false
    res_dct = Extras("foobar", false_in_blacklist_policy).as_dict
    assert res_dct.in_blacklist == {}


def test_empty_err_msg_if_no_err(mixed_policy):
    # "in_blacklist": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a in_blacklist
    assert not res_dct.in_blacklist.err               # no :err
    assert res_dct.in_blacklist.err_msg == ""         # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "in_blacklist": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a in_blacklist
    assert not res_dct.in_blacklist.err               # no :err
    assert res_dct.in_blacklist.exc is None           # :exc is None


@pytest.mark.parametrize("pwd, pwd_blist, policy_blist, expected", [
    # Empty
    (
        "",       # <- password
        ["foo"],  # <- :pwd_blacklist
        ["bar"],  # <- blacklist from policy
        {'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'blacklist',
         'policy_param_name': 'in_blacklist'}
    ),

    # Only :pwd_blacklist
    (
        "foo",    # <- password
        ["foo"],  # <- :pwd_blacklist
        [],       # <- blacklist from policy
        {'err': True,
         'err_msg': 'password found in blacklist',
         'exc': ExtrasCheckError('password found in blacklist',),
         'param_name': 'blacklist',
         'policy_param_name': 'in_blacklist'}
    ),

    # Only in policy
    (
        "foo",    # <- password
        [],       # <- :pwd_blacklist
        ["foo"],  # <- blacklist from policy
        {'err': True,
         'err_msg': 'password found in blacklist',
         'exc': ExtrasCheckError('password found in blacklist',),
         'param_name': 'blacklist',
         'policy_param_name': 'in_blacklist'}
    ),

    # Both in :pwd_blacklist and in policy
    (
        "foo",           # <- password
        ["foo", "bar"],  # <- :pwd_blacklist
        ["foo"],         # <- blacklist from policy
        {'err': True,
         'err_msg': 'password found in blacklist',
         'exc': ExtrasCheckError('password found in blacklist',),
         'param_name': 'blacklist',
         'policy_param_name': 'in_blacklist'}
    ),
])
def test_in_blacklist(pwd, pwd_blist, policy_blist, expected, mixed_policy):
    mixed_policy.update({"blacklist": policy_blist})
    res_dct = Extras(pwd, mixed_policy, pwd_blacklist=pwd_blist).as_dict

    for key, val in expected.items():
        if key == 'exc' and res_dct.in_blacklist['exc']:
            assert isinstance(res_dct.in_blacklist[key], ExtrasCheckError)
        else:
            assert res_dct.in_blacklist[key] == val


#
# Test Extras.blacklist property
#
class TestBlacklistProperty:

    # :arg_items is a list of passwords provided as :pwd_blacklist
    # argument into the class constructor
    def test_arg_items_accepted_types(self, mixed_policy):
        for blacklist in (list(), tuple(), set()):
            ext = Extras("pwd", mixed_policy, pwd_blacklist=blacklist)
            assert isinstance(ext.blacklist, list)

    def test_arg_items_non_accepted_types(self, mixed_policy):
        # non-iterable items
        for blacklist in (1, 1.0, lambda: 1):
            ext = Extras("pwd", mixed_policy, pwd_blacklist=blacklist)

            # Can be catched as pwdcheck.exceptions.DataTypeError
            with pytest.raises(DataTypeError) as exc_info:
                ext.blacklist  # pylint: disable=pointless-statement
                assert ("object provided by 'pwd_blacklist' "
                        "is not iterable") in exc_info

            # Can be catched as TypeError
            with pytest.raises(TypeError) as exc_info:
                ext.blacklist  # pylint: disable=pointless-statement
                assert ("object provided by 'pwd_blacklist' "
                        "is not iterable") in exc_info

    @pytest.mark.parametrize("blacklist, expected", [
        # Everything which evaluates into False
        (None, []),
        (list(), []),
        (set(), []),
        (tuple(), []),

        # XXX: does this behavior desired?
        (int(), []),
        (float(), []),

        # Always returns list
        (["foo", "bar"], ["foo", "bar"]),
        (("foo", "bar"), ["foo", "bar"]),
        ({"foo", "bar"}, ["foo", "bar"]),

        # Removes duplicates
        (["foo", "foo", "bar"], ["foo", "bar"]),
    ])
    def test_blacklist_init_as_arg(self, blacklist, expected, mixed_policy):
        # Blacklist init using :pwd_blacklist argument
        ext = Extras("pwd", mixed_policy, pwd_blacklist=blacklist)
        assert sorted(ext.blacklist) == sorted(expected)

    @pytest.mark.parametrize("policy_blist, expected", [
        # Empty
        ([], []),

        # Simple
        (["foo", "bar"], ["foo", "bar"]),

        # Removes duplicates
        (["foo", "foo", "bar"], ["foo", "bar"]),
    ])
    def test_blacklist_init_as_policy(self, policy_blist,
                                      expected, mixed_policy):
        # Blacklist init by :blacklist field from policy
        mixed_policy.update({"blacklist": policy_blist})
        ext = Extras("pwd", mixed_policy)
        assert sorted(ext.blacklist) == sorted(expected)

    @pytest.mark.parametrize("pwd_blist, policy_blist, expected", [
        # Both are empty
        ([], [], []),

        # One is empty
        ([], ["spam", "eggs"], ["spam", "eggs"]),
        (["foo", "bar"], [], ["foo", "bar"]),

        # Duplicates
        (["foo", "bar"], ["bar"], ["foo", "bar"]),
        (["bar"], ["foo", "bar"], ["foo", "bar"]),
        (["foo", "bar"], ["foo", "bar"], ["foo", "bar"]),

        # Different
        (["foo"], ["bar"], ["foo", "bar"]),
    ])
    def test_blacklist_mixed_init(self, pwd_blist, policy_blist,
                                  expected, mixed_policy):
        # Blacklist init using both :pwd_blacklist arg
        # and :blacklist field from policy
        mixed_policy.update({"blacklist": policy_blist})
        ext = Extras("pwd", mixed_policy, pwd_blacklist=pwd_blist)
        assert sorted(ext.blacklist) == sorted(expected)
