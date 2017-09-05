# -*- coding: utf-8 -*-

"""
tests.conftest
~~~~~~~~~~~~~~

Top-level conftest.
"""

import json
from copy import deepcopy

import pytest

from pwdcheck.helpers import Dotdict


def dotdictify(dct):
    """Returns copy of the `dct` but with all `dict` objects
    replaced with `Dotdict` objects.
    """
    dotdict = Dotdict()
    for key, val in dct.items():
        if isinstance(val, dict):
            dotdict[key] = dotdictify(val)
        else:
            dotdict[key] = val
    return dotdict


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


@pytest.fixture(scope='function')  # <- scope 'function' is important
def pwd_ok_full_out():
    # `dotdictify` required to imitate actual pwdcheck.check output
    return dotdictify({
        'complexity': {
            'digits': {'aval': 2,
                       'err': False,
                       'err_msg': '',
                       'exc': None,
                       'param_name': 'digits',
                       'policy_param_name': 'dmin',
                       'pval': 2},
            'length': {'aval': 14,
                       'err': False,
                       'err_msg': '',
                       'exc': None,
                       'param_name': 'length',
                       'policy_param_name': 'minlen',
                       'pval': 8},
            'lowercase': {'aval': 8,
                          'err': False,
                          'err_msg': '',
                          'exc': None,
                          'param_name': 'lowercase',
                          'policy_param_name': 'lmin',
                          'pval': 2},
            'special': {'aval': 2,
                        'err': False,
                        'err_msg': '',
                        'exc': None,
                        'param_name': 'special',
                        'policy_param_name': 'omin',
                        'pval': 2},
            'uppercase': {'aval': 2,
                          'err': False,
                          'err_msg': '',
                          'exc': None,
                          'param_name': 'uppercase',
                          'policy_param_name': 'umin',
                          'pval': 2}},
        'extras': {
            'blacklist': {'err': False,
                          'err_msg': '',
                          'exc': None,
                          'param_name': 'blacklist',
                          'policy_param_name': 'in_blacklist'},
            'dictionary': {'err': False,
                           'err_msg': '',
                           'exc': None,
                           'param_name': 'dictionary',
                           'policy_param_name': 'in_dictionary'},
            'history': {'err': False,
                        'err_msg': '',
                        'exc': None,
                        'param_name': 'history',
                        'policy_param_name': 'in_history'},
            'palindrome': {'err': False,
                           'err_msg': '',
                           'exc': None,
                           'param_name': 'palindrome',
                           'policy_param_name': 'palindrome'}},
    })
