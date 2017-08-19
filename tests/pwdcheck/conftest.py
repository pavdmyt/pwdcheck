# -*- coding: utf-8 -*-

"""
tests.pwdcheck.conftest
~~~~~~~~~~~~~~~~~~~~~~~

"""

import pytest


@pytest.fixture(scope='function', params=[
    "dict-policy",
    "json-policy",
])
def policy(request):
    if request.param == "dict-policy":
        return request.getfuncargvalue("mixed_policy")
    if request.param == "json-policy":
        return request.getfuncargvalue("mixed_policy_json")


@pytest.fixture(scope='function')
def broken_json_policy(mixed_policy_json):
    return "#!" + mixed_policy_json
