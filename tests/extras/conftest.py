# -*- coding: utf-8 -*-

"""
tests.extras.conftest
~~~~~~~~~~~~~~~~~~~~~

"""

import json
from copy import deepcopy

import pytest


@pytest.fixture(scope='module')
def base_policy():
    return {"extras": {"palindrome": True,
                       "in_dictionary": True,
                       "in_blacklist": True,
                       "in_history": True}}


# For consistency with /tests/cxty
@pytest.fixture(scope='function')
def mixed_policy(base_policy):
    p = deepcopy(base_policy)
    return p


@pytest.fixture(scope='function')
def mixed_policy_json(mixed_policy):
    return json.dumps(mixed_policy)


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


@pytest.fixture(scope='module')
def false_in_dictionary_policy(base_policy):
    p = deepcopy(base_policy)
    p["extras"]["in_dictionary"] = False
    return p


@pytest.fixture(scope='module')
def false_in_history_policy(base_policy):
    p = deepcopy(base_policy)
    p["extras"]["in_history"] = False
    return p