# -*- coding: utf-8 -*-

"""
tests.cxty.conftest
~~~~~~~~~~~~~~~~~~~

"""

import pytest


@pytest.fixture(scope='module')
def mixed_spec():
    return {"complexity": {"minlen": 8,
                           "umin": 1,
                           "lmin": 1,
                           "dmin": 2,
                           "omin": 1}}
