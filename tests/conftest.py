# -*- coding: utf-8 -*-

"""
tests.conftest
~~~~~~~~~~~~~~

Top-level conftest.
"""

import json
from copy import deepcopy

import pytest


@pytest.fixture(scope='module')
def base_policy():
    return {
        "complexity": {"minlen": 8,
                       "umin": 2,
                       "lmin": 2,
                       "dmin": 2,
                       "omin": 2},
        "extras": {"palindrome": True,
                   "in_dictionary": True,
                   "in_blacklist": True,
                   "in_history": True},
    }


@pytest.fixture(scope='function')
def mixed_policy(base_policy):
    p = deepcopy(base_policy)
    return p


@pytest.fixture(scope='function')
def mixed_policy_json(mixed_policy):
    return json.dumps(mixed_policy)
