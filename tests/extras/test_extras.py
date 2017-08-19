# -*- coding: utf-8 -*-

"""
tests.extras.test_extras
~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `pwdcheck.extras` module.
"""

import pytest

from pwdcheck.exceptions import PolicyError
from pwdcheck.extras import Extras


def test_init_from_json(mixed_policy_json, mixed_policy):
    # :mixed_policy_json                                 type: str
    ext = Extras.from_json("pwd", mixed_policy_json)
    assert ext._policy == mixed_policy


@pytest.mark.parametrize("policy_obj, exc_type", [
    ({}, None),         # <- valid :policy type, no exceptions
    ([], PolicyError),  # <- unsupported :policy type, exception
])
def test_policy_property(policy_obj, exc_type):
    extras = Extras("pwd", policy_obj)

    if exc_type is not None:
        with pytest.raises(exc_type) as exc_info:
            extras.policy  # pylint: disable=pointless-statement
        assert str(exc_info.value) == "unsupported data type"
    else:
        assert isinstance(extras.policy, dict)
