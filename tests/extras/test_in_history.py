# -*- coding: utf-8 -*-

"""
tests.extras.test_in_history
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `in_history` check.
"""

import pytest

from pwdcheck.exceptions import DataTypeError, ExtrasCheckError
from pwdcheck.extras import Extras


#
# Test Extras.as_dict out for in_history checks
#
def test_false_in_history(false_in_history_policy):
    # "in_history": false
    res_dct = Extras("foobar", false_in_history_policy).as_dict
    assert "history" not in res_dct.keys()


def test_empty_err_msg_if_no_err(mixed_policy):
    # "in_history": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a in_history
    assert not res_dct.history.err                 # no :err
    assert res_dct.history.err_msg == ""           # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "in_history": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a in_history
    assert not res_dct.history.err                 # no :err
    assert res_dct.history.exc is None             # :exc is None


@pytest.mark.parametrize("pwd, pwd_blist, policy_blist, expected", [
    # Empty
    (
        "",       # <- password
        ["foo"],  # <- :pwd_history
        ["bar"],  # <- history from policy
        {'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'history',
         'policy_param_name': 'in_history'}
    ),

    # Only :pwd_history
    (
        "foo",    # <- password
        ["foo"],  # <- :pwd_history
        [],       # <- history from policy
        {'err': True,
         'err_msg': 'password found in history',
         'exc': ExtrasCheckError('password found in history',),
         'param_name': 'history',
         'policy_param_name': 'in_history'}
    ),

    # Only in policy
    (
        "foo",    # <- password
        [],       # <- :pwd_history
        ["foo"],  # <- history from policy
        {'err': True,
         'err_msg': 'password found in history',
         'exc': ExtrasCheckError('password found in history',),
         'param_name': 'history',
         'policy_param_name': 'in_history'}
    ),

    # Both in :pwd_history and in policy
    (
        "foo",           # <- password
        ["foo", "bar"],  # <- :pwd_history
        ["foo"],         # <- history from policy
        {'err': True,
         'err_msg': 'password found in history',
         'exc': ExtrasCheckError('password found in history',),
         'param_name': 'history',
         'policy_param_name': 'in_history'}
    ),
])
def test_in_history(pwd, pwd_blist, policy_blist, expected, mixed_policy):
    mixed_policy.update({"history": policy_blist})
    res_dct = Extras(pwd, mixed_policy, pwd_history=pwd_blist).as_dict

    for key, val in expected.items():
        if key == 'exc' and res_dct.history['exc']:
            assert isinstance(res_dct.history[key], ExtrasCheckError)
        else:
            assert res_dct.history[key] == val


#
# Test Extras.history property
#
class TestHistoryProperty:

    # :arg_items is a list of passwords provided as :pwd_history
    # argument into the class constructor
    def test_arg_items_accepted_types(self, mixed_policy):
        for history in (list(), tuple(), set()):
            ext = Extras("pwd", mixed_policy, pwd_history=history)
            assert isinstance(ext.history, list)

    def test_arg_items_non_accepted_types(self, mixed_policy):
        # non-iterable items
        for history in (1, 1.0, lambda: 1):
            ext = Extras("pwd", mixed_policy, pwd_history=history)
            err_msg = "object provided by 'pwd_history' is not iterable"

            # Can be catched as pwdcheck.exceptions.DataTypeError
            with pytest.raises(DataTypeError) as datatype_exc:
                ext.history  # pylint: disable=pointless-statement

            # Can be catched as TypeError
            with pytest.raises(TypeError) as type_exc:
                ext.history  # pylint: disable=pointless-statement

            assert str(datatype_exc.value) == err_msg
            assert str(type_exc.value) == err_msg

    @pytest.mark.parametrize("history, expected", [
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
    def test_history_init_as_arg(self, history, expected, mixed_policy):
        # History init using :pwd_history argument
        ext = Extras("pwd", mixed_policy, pwd_history=history)
        assert sorted(ext.history) == sorted(expected)

    @pytest.mark.parametrize("policy_blist, expected", [
        # Empty
        ([], []),

        # Simple
        (["foo", "bar"], ["foo", "bar"]),

        # Removes duplicates
        (["foo", "foo", "bar"], ["foo", "bar"]),
    ])
    def test_history_init_as_policy(self, policy_blist,
                                    expected, mixed_policy):
        # History init by :history field from policy
        mixed_policy.update({"history": policy_blist})
        ext = Extras("pwd", mixed_policy)
        assert sorted(ext.history) == sorted(expected)

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
    def test_history_mixed_init(self, pwd_blist, policy_blist,
                                expected, mixed_policy):
        # History init using both :pwd_history arg
        # and :history field from policy
        mixed_policy.update({"history": policy_blist})
        ext = Extras("pwd", mixed_policy, pwd_history=pwd_blist)
        assert sorted(ext.history) == sorted(expected)
