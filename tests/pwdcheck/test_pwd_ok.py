# -*- coding: utf-8 -*-

"""
tests.pwdcheck.test_pwd_ok
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `_pwd_ok_check` function.
"""

import pytest

from pwdcheck.pwdcheck import _pwd_ok_check


@pytest.mark.parametrize("param_type, param_name, expected", [
    # All `err` attrs are False
    ("", "", True),

    #
    # complexity errors
    #

    # complexity.digits error
    ("complexity", "digits", False),

    # complexity.length error
    ("complexity", "length", False),

    # complexity.lowercase error
    ("complexity", "lowercase", False),

    # complexity.uppercase error
    ("complexity", "uppercase", False),

    # complexity.special error
    ("complexity", "special", False),

    #
    # extras errors
    #

    # extras.blacklist error
    ("extras", "blacklist", False),

    # extras.dictionary error
    ("extras", "dictionary", False),

    # extras.history error
    ("extras", "history", False),

    # extras.palindrome error
    ("extras", "palindrome", False),
])
def test_pwd_ok(param_type, param_name, expected, pwd_ok_full_out):
    try:
        # Introduce some errors
        pwd_ok_full_out[param_type][param_name]['err'] = True
    except KeyError:
        # Skip if no such param in policy
        pass

    pwd_ok = _pwd_ok_check(pwd_ok_full_out)
    assert pwd_ok == expected


# Unsupported policy params or params which shouldn't be
# checked will not be taken into consideration in `pwd_ok`
@pytest.mark.parametrize("param_type, param_name, expected", [
    ("complexity", "foobar", True),  # <- unsupported param
    ("complexity", "digits", True),  # <- shouldn't be checked

    ("extras", "foobar", True),      # <- unsupported param
    ("extras", "history", True),     # <- shouldn't be checked
])
def test_unsupported_policy_param(param_type, param_name, expected,
                                  pwd_ok_full_out):
    pwd_ok_full_out[param_type][param_name] = {}
    pwd_ok = _pwd_ok_check(pwd_ok_full_out)
    assert pwd_ok == expected
