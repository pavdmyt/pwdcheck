# -*- coding: utf-8 -*-

"""
tests.cxty.test_complexity
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `pwdcheck.cxty` module.
"""

import pytest

from pwdcheck.cxty import Complexity
from pwdcheck.exceptions import PolicyError


def test_init_from_json(mixed_policy_json, mixed_policy):
    # :mixed_policy_json                                 type: str
    cxty = Complexity.from_json("pwd", mixed_policy_json)
    assert cxty._policy == mixed_policy


@pytest.mark.parametrize("policy_obj, exc_type", [
    ({}, None),         # <- valid :policy type, no exceptions
    ([], PolicyError),  # <- unsupported :policy type, exception
])
def test_policy_property(policy_obj, exc_type):
    cxty = Complexity("pwd", policy_obj)

    if exc_type is not None:
        with pytest.raises(exc_type) as exc_info:
            cxty.policy  # pylint: disable=pointless-statement
        assert str(exc_info.value) == "unsupported data type"
    else:
        assert isinstance(cxty.policy, dict)
