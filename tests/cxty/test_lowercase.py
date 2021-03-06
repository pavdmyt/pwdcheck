# -*- coding: utf-8 -*-

"""
tests.cxty.test_lowercase
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for "lowercase" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError, PolicyError


def test_zero_lowercase(zero_lmin_policy):
    # "lmin": 0
    res_dct = Complexity("foobar", zero_lmin_policy).as_dict
    expected = {
        'aval': 6,
        'err': False,
        'err_msg': '',
        'exc': None,
        'param_name': 'lowercase',
        'policy_param_name': 'lmin',
        'pval': 0
    }
    assert res_dct.lowercase == expected


def test_none_lmin(none_lmin_policy):
    # no "lmin" in policy
    res_dct = Complexity("foobar", none_lmin_policy).as_dict
    assert Complexity._pname_policy_map["lmin"] not in res_dct.keys()


def test_nonint_lmin(nonint_lmin_policy):
    # non-int type: "lmin"
    with pytest.raises(PolicyError) as exc_info:
        Complexity("foobar", nonint_lmin_policy).as_dict
    assert "non-int value set to" in str(exc_info.value)


def test_empty_err_msg_if_no_err(mixed_policy):
    # "lmin": 2
    res_dct = Complexity("ll", mixed_policy).as_dict
    assert not res_dct.lowercase.err        # no :err
    assert res_dct.lowercase.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "lmin": 2
    res_dct = Complexity("ll", mixed_policy).as_dict
    assert not res_dct.lowercase.err        # no :err
    assert res_dct.lowercase.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty
    (
        "",  # <- password
        {'aval': 0,
         'err': True,
         'err_msg': 'password must contain at least 2 lowercase '
                    'characters, 0 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'lowercase characters, 0 given',),
         'param_name': 'lowercase',
         'policy_param_name': 'lmin',
         'pval': 2}
    ),

    # Short
    (
        "l",  # <- password
        {'aval': 1,
         'err': True,
         'err_msg': 'password must contain at least 2 lowercase '
                    'characters, 1 given',
         'exc': ComplexityCheckError('password must contain at least 2 '
                                     'lowercase characters, 1 given',),
         'param_name': 'lowercase',
         'policy_param_name': 'lmin',
         'pval': 2}
    ),

    # Good
    (
        "ll",  # <- password
        {'aval': 2,
         'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'lowercase',
         'policy_param_name': 'lmin',
         'pval': 2}
    )
])
def test_lowercase(pwd, expected_out, mixed_policy):
    res_dct = Complexity(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.lowercase['exc']:
            assert isinstance(res_dct.lowercase[key], ComplexityCheckError)
        else:
            assert res_dct.lowercase[key] == val
