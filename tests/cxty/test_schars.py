# -*- coding: utf-8 -*-

"""
tests.cxty.test_schars
~~~~~~~~~~~~~~~~~~~~~~

Tests for "special" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError


def test_zero_special(zero_omin_policy):
    # "omin": 0
    res_dct = Complexity("foobar", zero_omin_policy).as_dict
    expected = {
        'aval': 0,
        'err': False,
        'err_msg': '',
        'exc': None,
        'param_name': 'special',
        'policy_param_name': 'omin',
        'pval': 0
    }
    assert res_dct.special == expected


def test_false_special(false_omin_policy):
    # "omin": false
    res_dct = Complexity("foobar", false_omin_policy).as_dict
    assert res_dct.special == {}


def test_none_special(none_omin_policy):
    # no "omin" in policy
    res_dct = Complexity("foobar", none_omin_policy).as_dict
    assert Complexity._pname_policy_map["omin"] not in res_dct.keys()


def test_empty_err_msg_if_no_err(mixed_policy):
    # "omin": 2
    res_dct = Complexity("#!", mixed_policy).as_dict
    assert not res_dct.special.err        # no :err
    assert res_dct.special.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "omin": 2
    res_dct = Complexity("#!", mixed_policy).as_dict
    assert not res_dct.special.err        # no :err
    assert res_dct.special.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty
    (
        "",  # <- password
        {'aval': 0,
         'err': True,
         'err_msg': 'password must contain at least 2 special '
                    'characters, 0 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'special characters, 0 given',),
         'param_name': 'special',
         'policy_param_name': 'omin',
         'pval': 2}
    ),

    # Short
    (
        "!",  # <- password
        {'aval': 1,
         'err': True,
         'err_msg': 'password must contain at least 2 special '
                    'characters, 1 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'special characters, 1 given',),
         'param_name': 'special',
         'policy_param_name': 'omin',
         'pval': 2}
    ),

    # Good
    (
        "#!",  # <- password
        {'aval': 2,
         'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'special',
         'policy_param_name': 'omin',
         'pval': 2}
    )
])
def test_special(pwd, expected_out, mixed_policy):
    res_dct = Complexity(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.special['exc']:
            assert isinstance(res_dct.special[key], ComplexityCheckError)
        else:
            assert res_dct.special[key] == val
