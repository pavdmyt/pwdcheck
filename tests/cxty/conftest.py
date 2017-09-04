# -*- coding: utf-8 -*-

"""
tests.cxty.conftest
~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


@pytest.fixture(scope='module', params=[
    "true-value",
    "false-value",
    "zero-value",
    "one-value",
])
def unknown_param_policy(request, base_policy):
    p = deepcopy(base_policy)

    if request.param == "true-value":
        p["complexity"]["foo-param"] = True

    if request.param == "false-value":
        p["complexity"]["foo-param"] = False

    if request.param == "zero-value":
        p["complexity"]["foo-param"] = 0

    if request.param == "one-value":
        p["complexity"]["foo-param"] = 1

    return p


# Non-int policies
def compose_nonint(policy_param_name):

    @pytest.fixture(scope='module', params=[
        "true-value",
        "false-value",
        "foo-value",
        "list-value",
    ])
    def nonint_policy(request, base_policy):
        p = deepcopy(base_policy)

        if request.param == "true-value":
            p["complexity"][policy_param_name] = True
        if request.param == "false-value":
            p["complexity"][policy_param_name] = False
        if request.param == "foo-value":
            p["complexity"][policy_param_name] = "foo"
        if request.param == "list-value":
            p["complexity"][policy_param_name] = [1, 2, 3]

        return p
    return nonint_policy


nonint_minlen_policy = compose_nonint("minlen")
nonint_dmin_policy = compose_nonint("dmin")
nonint_lmin_policy = compose_nonint("lmin")
nonint_umin_policy = compose_nonint("umin")
nonint_omin_policy = compose_nonint("omin")


def compose_zero(policy_param_name):
    @pytest.fixture(scope='module')
    def zero_policy(base_policy):
        p = deepcopy(base_policy)
        p["complexity"][policy_param_name] = 0
        return p
    return zero_policy


zero_minlen_policy = compose_zero("minlen")
zero_dmin_policy = compose_zero("dmin")
zero_lmin_policy = compose_zero("lmin")
zero_umin_policy = compose_zero("umin")
zero_omin_policy = compose_zero("omin")


def compose_none(policy_param_name):
    @pytest.fixture(scope='module')
    def none_policy(base_policy):
        p = deepcopy(base_policy)
        del p["complexity"][policy_param_name]
        return p
    return none_policy


none_minlen_policy = compose_none("minlen")
none_dmin_policy = compose_none("dmin")
none_lmin_policy = compose_none("lmin")
none_umin_policy = compose_none("umin")
none_omin_policy = compose_none("omin")
