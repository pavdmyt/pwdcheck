# -*- coding: utf-8 -*-

"""
tests.pwdcheck.conftest
~~~~~~~~~~~~~~~~~~~~~~~

"""

import pytest


@pytest.fixture(scope='function', params=[
    "dict-policy",
    "json-policy",
    # "broken-json-policy",
])
def policy(request):
    if request.param == "dict-policy":
        return request.getfuncargvalue("mixed_policy")
    if request.param == "json-policy":
        return request.getfuncargvalue("mixed_policy_json")
    # if request.param == "broken-json-policy":
    #     return request.getfuncargvalue("mixed_policy_json") + "#!"
