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
    def nonint_policies(request, base_policy):
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
    return nonint_policies


nonint_minlen_policy = compose_nonint("minlen")
nonint_dmin_policy = compose_nonint("dmin")
nonint_lmin_policy = compose_nonint("lmin")
nonint_umin_policy = compose_nonint("umin")
nonint_omin_policy = compose_nonint("omin")


#
# minlen
#
@pytest.fixture(scope='module')
def zero_minlen_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["minlen"] = 0
    return p


@pytest.fixture(scope='module')
def none_minlen_policy(base_policy):
    p = deepcopy(base_policy)
    del p["complexity"]["minlen"]
    return p


#
# dmin
#
@pytest.fixture(scope='module')
def zero_dmin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["dmin"] = 0
    return p


@pytest.fixture(scope='module')
def none_dmin_policy(base_policy):
    p = deepcopy(base_policy)
    del p["complexity"]["dmin"]
    return p


#
# uppercase
#
@pytest.fixture(scope='module')
def zero_umin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["umin"] = 0
    return p


@pytest.fixture(scope='module')
def none_umin_policy(base_policy):
    p = deepcopy(base_policy)
    del p["complexity"]["umin"]
    return p


#
# lowercase
#
@pytest.fixture(scope='module')
def zero_lmin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["lmin"] = 0
    return p


@pytest.fixture(scope='module')
def none_lmin_policy(base_policy):
    p = deepcopy(base_policy)
    del p["complexity"]["lmin"]
    return p


#
# special
#
@pytest.fixture(scope='module')
def zero_omin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["omin"] = 0
    return p


@pytest.fixture(scope='module')
def none_omin_policy(base_policy):
    p = deepcopy(base_policy)
    del p["complexity"]["omin"]
    return p
