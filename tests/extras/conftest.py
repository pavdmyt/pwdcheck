# -*- coding: utf-8 -*-

"""
tests.extras.conftest
~~~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


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


@pytest.fixture(scope='module', params=[
    "true-value",
    "false-value",
])
def unknown_param_policy(request, base_policy):
    p = deepcopy(base_policy)

    if request.param == "true-value":
        p["extras"]["foo-param"] = True
    if request.param == "false-value":
        p["extras"]["foo-param"] = False

    return p
