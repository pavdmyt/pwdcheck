# -*- coding: utf-8 -*-

"""
tests.extras.test_palindrome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `palindrome` check.
"""

import pytest

from pwdcheck.exceptions import ExtrasCheckError
from pwdcheck.extras import Extras


#
# Test Extras.as_dict out for palindrome checks
#
def test_false_palindrome(false_palindrome_policy):
    # "palindrome": false
    res_dct = Extras("foobar", false_palindrome_policy).as_dict
    assert res_dct.palindrome == {}


def test_empty_err_msg_if_no_err(mixed_policy):
    # "palindrome": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a palindrome
    assert not res_dct.palindrome.err        # no :err
    assert res_dct.palindrome.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "palindrome": true
    res_dct = Extras("foobar", mixed_policy).as_dict  # not a palindrome
    assert not res_dct.palindrome.err        # no :err
    assert res_dct.palindrome.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty (the empty string is a palindrome)
    (
        "",  # <- password
        {'err': True,
         'err_msg': 'password is a palindrome',
         'exc': ExtrasCheckError('password is a palindrome',),
         'param_name': 'palindrome',
         'policy_param_name': 'palindrome'}
    ),

    # Single character (also a palindrome)
    (
        "1",  # <- password
        {'err': True,
         'err_msg': 'password is a palindrome',
         'exc': ExtrasCheckError('password is a palindrome',),
         'param_name': 'palindrome',
         'policy_param_name': 'palindrome'}
    ),

    # Classic example (also a palindrome)
    (
        "racecar",  # <- password
        {'err': True,
         'err_msg': 'password is a palindrome',
         'exc': ExtrasCheckError('password is a palindrome',),
         'param_name': 'palindrome',
         'policy_param_name': 'palindrome'}
    ),

    # Not a palindrome
    (
        "foo",  # <- password
        {'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'palindrome',
         'policy_param_name': 'palindrome'}
    )
])
def test_palindrome(pwd, expected_out, mixed_policy):
    res_dct = Extras(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.palindrome['exc']:
            assert isinstance(res_dct.palindrome[key], ExtrasCheckError)
        else:
            assert res_dct.palindrome[key] == val


#
# Test Extras.is_palindrome method
#
@pytest.mark.parametrize("string, expected", [
    # the empty string is a palindrome
    ("", True),

    # single-character string is a palindrome
    ("u", True),

    # palindrome checks are case-insensitive
    ("raceCAR", True),

    # common palindromes
    ("radar", True),
    ("level", True),
    ("rotor", True),
    ("kayak", True),
    ("refer", True),

    # Non palindromes
    ("foo", False),
    ("bar", False),
    ("42", False),
])
def test_is_palindrome(string, expected):
    assert Extras.is_palindrome(string) == expected
