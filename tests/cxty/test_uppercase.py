
"""
tests.cxty.test_uppercase
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for "uppercase" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError


def test_zero_uppercase(zero_umin_policy):
    # "umin": 0
    res_dct = Complexity("foobar", zero_umin_policy).as_dict
    assert res_dct.uppercase == {}


def test_false_uppercase(false_umin_policy):
    # "umin": false
    res_dct = Complexity("foobar", false_umin_policy).as_dict
    assert res_dct.uppercase == {}


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
          'err_msg': 'password must contain at least 2 uppercase characters, 0 given',  # noqa
          'exc': ComplexityCheckError('password must contain at least 2 uppercase characters, 0 given',),  # noqa
          'param_name': 'uppercase',
          'policy_param_name': 'umin',
          'pval': 2}
    ),

    # Short
    (
        "U",  # <- password
        {'aval': 1,
         'err': True,
         'err_msg': 'password must contain at least 2 uppercase characters, 1 given',  # noqa
         'exc': ComplexityCheckError('password must contain at least 2 uppercase characters, 1 given',),  # noqa
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
            print(key, val)
            assert res_dct.uppercase[key] == val
