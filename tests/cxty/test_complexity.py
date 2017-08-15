# -*- coding: utf-8 -*-

"""
tests.cxty.test_complexity
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `pwdcheck.cxty` module.
"""

from pwdcheck.cxty import Complexity


def test_init_from_json(mixed_policy_json, mixed_policy):
    # :mixed_policy_json                                 type: str
    cxty = Complexity.from_json("pwd", mixed_policy_json)
    assert cxty._policy == mixed_policy
