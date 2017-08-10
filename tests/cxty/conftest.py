# -*- coding: utf-8 -*-

"""
tests.cxty.conftest
~~~~~~~~~~~~~~~~~~~

"""

from copy import deepcopy

import pytest


@pytest.fixture(scope='module')
def base_policy():
    return {"complexity": {"minlen": 8,
                           "umin": 1,
                           "lmin": 1,
                           "dmin": 2,
                           "omin": 1}}


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
