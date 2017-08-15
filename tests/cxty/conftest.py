# -*- coding: utf-8 -*-

"""
tests.cxty.conftest
~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


#
# minlen
#
@pytest.fixture(scope='module')
def zero_len_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["minlen"] = 0
    return p


@pytest.fixture(scope='module')
def false_len_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["minlen"] = False
    return p


#
# dmin
#
@pytest.fixture(scope='module')
def zero_digits_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["dmin"] = 0
    return p


@pytest.fixture(scope='module')
def false_digits_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["dmin"] = False
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
def false_umin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["umin"] = False
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
def false_lmin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["lmin"] = False
    return p


#
# schars
#
@pytest.fixture(scope='module')
def zero_omin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["omin"] = 0
    return p


@pytest.fixture(scope='module')
def false_omin_policy(base_policy):
    p = deepcopy(base_policy)
    p["complexity"]["omin"] = False
    return p
