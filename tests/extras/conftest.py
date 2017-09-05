# -*- coding: utf-8 -*-

"""
tests.extras.conftest
~~~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


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


# Non-bool policies
def compose_nonbool(policy_param_name):

    @pytest.fixture(scope='module', params=[
        "int-value",
        "foo-value",
        "list-value",
    ])
    def nonbool_policy(request, base_policy):
        p = deepcopy(base_policy)

        if request.param == "int-value":
            p["extras"][policy_param_name] = 1
        if request.param == "foo-value":
            p["extras"][policy_param_name] = "foo"
        if request.param == "list-value":
            p["extras"][policy_param_name] = [1, 2, 3]

        return p
    return nonbool_policy


nonbool_palindrome_policy = compose_nonbool("palindrome")
nonbool_in_blacklist_policy = compose_nonbool("in_blacklist")
nonbool_in_dictionary_policy = compose_nonbool("in_dictionary")
nonbool_in_history_policy = compose_nonbool("in_history")


def compose_false(policy_param_name):
    @pytest.fixture(scope='module')
    def false_policy(base_policy):
        p = deepcopy(base_policy)
        p["extras"][policy_param_name] = False
        return p
    return false_policy


false_palindrome_policy = compose_false("palindrome")
false_in_blacklist_policy = compose_false("in_blacklist")
false_in_dictionary_policy = compose_false("in_dictionary")
false_in_history_policy = compose_false("in_history")
