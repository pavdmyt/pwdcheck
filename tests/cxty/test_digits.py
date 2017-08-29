# -*- coding: utf-8 -*-

"""
tests.cxty.test_digits
~~~~~~~~~~~~~~~~~~~~~~

Tests for "digits" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError


def test_zero_dmin(zero_dmin_policy):
    # "dmin": 0
    res_dct = Complexity("foobar", zero_dmin_policy).as_dict
    expected = {
        'aval': 0,
        'err': False,
        'err_msg': '',
        'exc': None,
        'param_name': 'digits',
        'policy_param_name': 'dmin',
        'pval': 0
    }
    assert res_dct.digits == expected


def test_false_dmin(false_dmin_policy):
    # "dmin": false
    res_dct = Complexity("foobar", false_dmin_policy).as_dict
    assert res_dct.digits == {}


def test_none_dmin(none_dmin_policy):
    # no "dmin" in policy
    res_dct = Complexity("foobar", none_dmin_policy).as_dict
    assert Complexity._pname_policy_map["dmin"] not in res_dct.keys()


def test_empty_err_msg_if_no_err(mixed_policy):
    # "dmin": 2
    res_dct = Complexity("11", mixed_policy).as_dict
    assert not res_dct.digits.err        # no :err
    assert res_dct.digits.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "dmin": 2
    res_dct = Complexity("11", mixed_policy).as_dict
    assert not res_dct.digits.err        # no :err
    assert res_dct.digits.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty
    (
        "",  # <- password
        {'aval': 0,
         'err': True,
         'err_msg': 'password must contain at least 2 numerals, 0 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'numerals, 0 given',),
         'param_name': 'digits',
         'policy_param_name': 'dmin',
         'pval': 2}
    ),

    # Short
    (
        "1",  # <- password
        {'aval': 1,
         'err': True,
         'err_msg': 'password must contain at least 2 numerals, 1 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'numerals, 1 given',),
         'param_name': 'digits',
         'policy_param_name': 'dmin',
         'pval': 2}
    ),

    # Good
    (
        "11",  # <- password
        {'aval': 2,
         'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'digits',
         'policy_param_name': 'dmin',
         'pval': 2}
    )
])
def test_digits(pwd, expected_out, mixed_policy):
    res_dct = Complexity(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.digits['exc']:
            assert isinstance(res_dct.digits[key], ComplexityCheckError)
        else:
            assert res_dct.digits[key] == val
