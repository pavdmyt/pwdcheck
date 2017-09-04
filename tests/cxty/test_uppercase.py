# -*- coding: utf-8 -*-

"""
tests.cxty.test_uppercase
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for "uppercase" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError, PolicyError


def test_zero_uppercase(zero_umin_policy):
    # "umin": 0
    res_dct = Complexity("foobar", zero_umin_policy).as_dict
    expected = {
        'aval': 0,
        'err': False,
        'err_msg': '',
        'exc': None,
        'param_name': 'uppercase',
        'policy_param_name': 'umin',
        'pval': 0
    }
    assert res_dct.uppercase == expected


def test_none_umin(none_umin_policy):
    # no "umin" in policy
    res_dct = Complexity("foobar", none_umin_policy).as_dict
    assert Complexity._pname_policy_map["umin"] not in res_dct.keys()


def test_nonint_umin(nonint_umin_policy):
    # non-int type: "umin"
    with pytest.raises(PolicyError) as exc_info:
        Complexity("foobar", nonint_umin_policy).as_dict
    assert "non-int value set to" in str(exc_info.value)


def test_empty_err_msg_if_no_err(mixed_policy):
    # "umin": 2
    res_dct = Complexity("UU", mixed_policy).as_dict
    assert not res_dct.uppercase.err        # no :err
    assert res_dct.uppercase.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "umin": 2
    res_dct = Complexity("UU", mixed_policy).as_dict
    assert not res_dct.uppercase.err        # no :err
    assert res_dct.uppercase.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty
    (
        "",  # <- password
        {'aval': 0,
         'err': True,
         'err_msg': 'password must contain at least 2 uppercase '
                    'characters, 0 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'uppercase characters, 0 given',),
         'param_name': 'uppercase',
         'policy_param_name': 'umin',
         'pval': 2}
    ),

    # Short
    (
        "U",  # <- password
        {'aval': 1,
         'err': True,
         'err_msg': 'password must contain at least 2 uppercase '
                    'characters, 1 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'uppercase characters, 1 given',),
         'param_name': 'uppercase',
         'policy_param_name': 'umin',
         'pval': 2}
    ),

    # Good
    (
        "UU",  # <- password
        {'aval': 2,
         'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'uppercase',
         'policy_param_name': 'umin',
         'pval': 2}
    )
])
def test_uppercase(pwd, expected_out, mixed_policy):
    res_dct = Complexity(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.uppercase['exc']:
            assert isinstance(res_dct.uppercase[key], ComplexityCheckError)
        else:
            assert res_dct.uppercase[key] == val
