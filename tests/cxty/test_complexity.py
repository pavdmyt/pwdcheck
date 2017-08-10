# -*- coding: utf-8 -*-

"""
tests.cxty.test_complexity
~~~~~~~~~~~~~~~~~~~~~~~~~~

Unittests for pwdcheck.cxty.Complexity class.
"""

from pwdcheck.cxty import Complexity

import pytest


# conftest fixtures:
#
# - mixed_spec


class TestErr:

    # Basic smoke test
    @pytest.mark.parametrize("pwd, errors", [
        # errors tmpl: [len, digit, upper, lower, schars]

        # Good one
        ("12FooBars!", [False, False, False, False, False]),

        # Good, with Unicode, Russian
        ("Пароль№42", [False, False, False, False, False]),

        # Good, with Unicode, Greek
        ("Κωδικό πρόσβασης#42", [False, False, False, False, False]),

        # Empty password
        ("", [True] * 5),

        # bad Length
        ("11Foo!", [True, False, False, False, False]),

        # bad Digits
        ("1FooBars!", [False, True, False, False, False]),

        # bad Uppercase
        ("11foobar!", [False, False, True, False, False]),

        # bad Lowercase
        ("11FOOBAR!", [False, False, False, True, False]),

        # bad Special characters
        ("11FOOBARs", [False, False, False, False, True]),
    ])
    def test_mixed_check(self, pwd, errors, mixed_spec):
        res_dct = Complexity(pwd, mixed_spec).as_dict
        len_err, digit_err, upper_err, lower_err, schars_err = errors

        assert res_dct.length.err == len_err
        assert res_dct.uppercase.err == upper_err
        assert res_dct.lowercase.err == lower_err
        assert res_dct.digits.err == digit_err
        assert res_dct.schars.err == schars_err
