
"""
tests.cxty.test_length
~~~~~~~~~~~~~~~~~~~~~~

Tests for "length" output param.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import ComplexityCheckError


def test_zero_length(zero_len_policy):
    # "minlen": 0
    res_dct = Complexity("foobar", zero_len_policy).as_dict
    assert res_dct.length == {}


def test_false_length(false_len_policy):
    # "minlen": false
    res_dct = Complexity("foobar", false_len_policy).as_dict
    assert res_dct.length == {}


def test_empty_err_msg_if_no_err(mixed_policy):
    # "minlen": 8
    res_dct = Complexity("foobar11", mixed_policy).as_dict
    assert not res_dct.length.err        # no :err
    assert res_dct.length.err_msg == ""  # empty :err_msg


def test_none_exc_if_no_err(mixed_policy):
    # "minlen": 8
    res_dct = Complexity("foobar11", mixed_policy).as_dict
    assert not res_dct.length.err        # no :err
    assert res_dct.length.exc is None    # :exc is None


@pytest.mark.parametrize("pwd, expected_out", [
    # Empty
    (
        "",  # <- password
        {'aval': 0,
         'err': True,
         'err_msg': 'password must contain at least 8 characters, 0 given',
         'exc': ComplexityCheckError('password must contain at least 8 characters, 0 given',),  # noqa
         'param_name': 'length',
         'policy_param_name': 'minlen',
         'pval': 8}
    ),

    # Short
    (
        "foo",  # <- password
        {'aval': 3,
         'err': True,
         'err_msg': 'password must contain at least 8 characters, 3 given',
         'exc': ComplexityCheckError('password must contain at least 8 characters, 3 given'),  # noqa
         'param_name': 'length',
         'policy_param_name': 'minlen',
         'pval': 8}
    ),

    # Good
    (
        "foobar11",  # <- password
        {'aval': 8,
         'err': False,
         'err_msg': '',
         'exc': None,
         'param_name': 'length',
         'policy_param_name': 'minlen',
         'pval': 8}
    )
])
def test_length(pwd, expected_out, mixed_policy):
    res_dct = Complexity(pwd, mixed_policy).as_dict

    for key, val in expected_out.items():
        if key == 'exc' and res_dct.length['exc']:
            assert isinstance(res_dct.length[key], ComplexityCheckError)
        else:
            assert res_dct.length[key] == val
