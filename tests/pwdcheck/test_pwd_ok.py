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

    # complexity.schars error
    ("complexity", "schars", False),

    #
    # extras errors
    #

    # extras.in_blacklist error
    ("extras", "in_blacklist", False),

    # extras.in_dictionary error
    ("extras", "in_dictionary", False),

    # extras.in_history error
    ("extras", "in_history", False),

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
