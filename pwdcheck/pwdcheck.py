# -*- coding: utf-8 -*-

"""
pwdcheck.pwdcheck
~~~~~~~~~~~~~~~~~

"""

from pwdcheck.helpers import Dotdict

from .cxty import Complexity
from .extras import Extras


def _pwd_ok_check(dct):
    cxty_dct = dct.complexity
    extras_dct = dct.extras

    cxty_errs = [val.err for val in cxty_dct.values()]
    extras_errs = [val for val in extras_dct.values()]

    return not any(cxty_errs + extras_errs)


def check(pwd, policy, history=None, pwd_dict=None):
    # JSON case
    if isinstance(policy, str):
        try:
            cxty = Complexity.from_json(pwd, policy)
            extras = Extras.from_json(pwd, policy, pwd_dict=pwd_dict)
        except ValueError as err:
            # TODO: implement pwdcheck.errors or exceptions
            raise NotImplementedError(err)
    # Common case
    elif isinstance(policy, dict):
        cxty = Complexity(pwd, policy)
        extras = Extras(pwd, policy, pwd_dict=pwd_dict)
    else:
        raise NotImplementedError("Unsupported policy data type")

    result = Dotdict()
    result.complexity = cxty.as_dict
    result.extras = extras.as_dict

    return _pwd_ok_check(result), result
