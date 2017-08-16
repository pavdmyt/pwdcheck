# -*- coding: utf-8 -*-

"""
tests.pwdcheck.test_check
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `check` function.
"""

from pwdcheck import check
from pwdcheck.cxty import Complexity
from pwdcheck.extras import Extras


def sanitize_key(dct, kname):
    """Returns copy of the `dct` without `kname` field
    from the given `dct` and all it's subdct's.
    """
    # Support for custom types with dict API
    type_ = type(dct)
    new_dct = type_()

    for key, val in dct.items():
        if isinstance(val, type_):
            new_dct[key] = sanitize_key(val, kname)
            continue
        if key != kname:
            new_dct[key] = val
    return new_dct


def test_dict_policy(base_policy):
    pwd = "pwd"
    _, res = check(pwd, base_policy)
    cxty_dct = Complexity(pwd, base_policy).as_dict
    extras_dct = Extras(pwd, base_policy).as_dict

    # Avoid `exc` fields since exceptions instances
    # break dicts equality test
    res = sanitize_key(res, "exc")
    cxty_dct = sanitize_key(cxty_dct, "exc")
    extras_dct = sanitize_key(extras_dct, "exc")

    assert res.complexity == cxty_dct
    assert res.extras == extras_dct
