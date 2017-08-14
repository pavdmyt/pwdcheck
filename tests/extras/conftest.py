# -*- coding: utf-8 -*-

"""
tests.extras.conftest
~~~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


@pytest.fixture(scope='module')
def base_policy():
    return {"extras": {"palindrome": True,
                       "in_dictionary": True,
                       "in_blacklist": True,
                       "in_history": True}}


@pytest.fixture(scope='module', params=[
    # Empty blacklist field
    "empty",

    # Simple blacklist
    "spam-eggs",

    # Blacklist with duplicates
    "spam-eggs-spam",
])
def policy_with_blacklist(base_policy, request):
    p = deepcopy(base_policy)

    if request.param == "empty":
        p.update(
            {"blacklist": []}
        )
    if request.param == "spam-eggs":
        p.update(
            {"blacklist": ["spam", "eggs"]}
        )
    if request.param == "spam-eggs-spam":
        p.update(
            {"blacklist": ["spam", "eggs", "spam"]}
        )
    return p


# For consistency with /tests/cxty
@pytest.fixture(scope='function')
def mixed_policy(base_policy):
    p = deepcopy(base_policy)
    return p


@pytest.fixture(scope='module')
def false_palindrome_policy(base_policy):
    p = deepcopy(base_policy)
    p["extras"]["palindrome"] = False
    return p


@pytest.fixture(scope='module')
def false_in_blacklist_policy(base_policy):
    p = deepcopy(base_policy)
    p["extras"]["in_blacklist"] = False
    return p
