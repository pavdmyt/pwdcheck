# -*- coding: utf-8 -*-

"""
tests.extras.test_extras
~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `pwdcheck.extras` module.
"""

from pwdcheck.extras import Extras


def test_init_from_json(mixed_policy_json, mixed_policy):
    # :mixed_policy_json                                 type: str
    ext = Extras.from_json("pwd", mixed_policy_json)
    assert ext._policy == mixed_policy
