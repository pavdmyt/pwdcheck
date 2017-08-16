# -*- coding: utf-8 -*-

"""
tests.pwdcheck.test_check
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for `check` function.
"""

from pwdcheck import check
from pwdcheck.cxty import Complexity
from pwdcheck.extras import Extras
# from pwdcheck.exceptions import PolicyParsingError


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
        elif key != kname:
            new_dct[key] = val
        else:
            continue
    return new_dct


def test_policy_types(policy):
    if isinstance(policy, dict):
        cxty_init = Complexity
        extras_init = Extras
    elif isinstance(policy, str):
        cxty_init = Complexity.from_json
        extras_init = Extras.from_json
    else:
        assert 0, "not implemented"

    pwd = "pwd"
    _, res = check(pwd, policy)
    cxty_dct = cxty_init(pwd, policy).as_dict
    extras_dct = extras_init(pwd, policy).as_dict

    # Avoid `exc` fields since exceptions instances
    # break dicts equality test
    res = sanitize_key(res, "exc")
    cxty_dct = sanitize_key(cxty_dct, "exc")
    extras_dct = sanitize_key(extras_dct, "exc")

    assert res.complexity == cxty_dct
    assert res.extras == extras_dct
