# -*- coding: utf-8 -*-

"""
tests.extras.test_in_dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `in_dictionary` check.
"""

import pytest

from pwdcheck.exceptions import DataTypeError, ExtrasCheckError
from pwdcheck.extras import Extras


#
# Test Extras.as_dict out for in_dictionary checks
#
def test_false_in_dictionary(false_in_dictionary_policy):
    # "in_dictionary": false
    res_dct = Extras("foobar", false_in_dictionary_policy).as_dict
    assert res_dct.in_dictionary == {}


def test_empty_err_msg_if_no_err(mixed_policy):
    # "in_dictionary": true
    res_dct = Extras("foobar", mixed_policy).as_dict   # not a in_dictionary
    assert not res_dct.in_dictionary.err               # no :err
    assert res_dct.in_dictionary.err_msg == ""         # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "in_dictionary": true
    res_dct = Extras("foobar", mixed_policy).as_dict   # not a in_dictionary
    assert not res_dct.in_dictionary.err               # no :err
    assert res_dct.in_dictionary.exc is None           # :exc is None


@pytest.mark.parametrize("pwd, pwd_dict, policy_dict, expected", [
    # Empty
    (
        "",       # <- password
        ["foo"],  # <- :pwd_dict
        ["bar"],  # <- dictionary from policy
        {'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'dictionary',
         'policy_param_name': 'in_dictionary'}
    ),

    # Only :pwd_dict
    (
        "foo",    # <- password
        ["foo"],  # <- :pwd_dict
        [],       # <- dictionary from policy
        {'err': True,
         'err_msg': 'password found in dictionary',
         'exc': ExtrasCheckError('password found in dictionary',),
         'param_name': 'dictionary',
         'policy_param_name': 'in_dictionary'}
    ),

    # Only in policy
    (
        "foo",    # <- password
        [],       # <- :pwd_dict
        ["foo"],  # <- dictionary from policy
        {'err': True,
         'err_msg': 'password found in dictionary',
         'exc': ExtrasCheckError('password found in dictionary',),
         'param_name': 'dictionary',
         'policy_param_name': 'in_dictionary'}
    ),

    # Both in :pwd_dict and in policy
    (
        "foo",           # <- password
        ["foo", "bar"],  # <- :pwd_dict
        ["foo"],         # <- dictionary from policy
        {'err': True,
         'err_msg': 'password found in dictionary',
         'exc': ExtrasCheckError('password found in dictionary',),
         'param_name': 'dictionary',
         'policy_param_name': 'in_dictionary'}
    ),
])
def test_in_dictionary(pwd, pwd_dict, policy_dict, expected, mixed_policy):
    mixed_policy.update({"dictionary": policy_dict})
    res_dct = Extras(pwd, mixed_policy, pwd_dict=pwd_dict).as_dict

    for key, val in expected.items():
        if key == 'exc' and res_dct.in_dictionary['exc']:
            assert isinstance(res_dct.in_dictionary[key], ExtrasCheckError)
        else:
            assert res_dct.in_dictionary[key] == val


#
# Test Extras.dictionary property
#
class TestDictionaryProperty:

    # :arg_items is a list of passwords provided as :pwd_dict
    # argument into the class constructor
    def test_arg_items_accepted_types(self, mixed_policy):
        for dictionary in (list(), tuple(), set()):
            ext = Extras("pwd", mixed_policy, pwd_dict=dictionary)
            assert isinstance(ext.dictionary, list)

    def test_arg_items_non_accepted_types(self, mixed_policy):
        # non-iterable items
        for dictionary in (1, 1.0, lambda: 1):
            ext = Extras("pwd", mixed_policy, pwd_dict=dictionary)
            err_msg = "object provided by 'pwd_dict' is not iterable"

            # Can be catched as pwdcheck.exceptions.DataTypeError
            with pytest.raises(DataTypeError) as datatype_exc:
                ext.dictionary  # pylint: disable=pointless-statement

            # Can be catched as TypeError
            with pytest.raises(TypeError) as type_exc:
                ext.dictionary  # pylint: disable=pointless-statement

            assert str(datatype_exc.value) == err_msg
            assert str(type_exc.value) == err_msg

    @pytest.mark.parametrize("dictionary, expected", [
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
    def test_dictionary_init_as_arg(self, dictionary, expected, mixed_policy):
        # Dictionary init using :pwd_dict argument
        ext = Extras("pwd", mixed_policy, pwd_dict=dictionary)
        assert sorted(ext.dictionary) == sorted(expected)

    @pytest.mark.parametrize("policy_blist, expected", [
        # Empty
        ([], []),

        # Simple
        (["foo", "bar"], ["foo", "bar"]),

        # Removes duplicates
        (["foo", "foo", "bar"], ["foo", "bar"]),
    ])
    def test_dictionary_init_as_policy(self, policy_blist,
                                       expected, mixed_policy):
        # Dictionary init by :dictionary field from policy
        mixed_policy.update({"dictionary": policy_blist})
        ext = Extras("pwd", mixed_policy)
        assert sorted(ext.dictionary) == sorted(expected)

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
    def test_dictionary_mixed_init(self, pwd_blist, policy_blist,
                                   expected, mixed_policy):
        # Dictionary init using both :pwd_dict arg
        # and :dictionary field from policy
        mixed_policy.update({"dictionary": policy_blist})
        ext = Extras("pwd", mixed_policy, pwd_dict=pwd_blist)
        assert sorted(ext.dictionary) == sorted(expected)
