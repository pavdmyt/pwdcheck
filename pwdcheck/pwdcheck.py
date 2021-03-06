# -*- coding: utf-8 -*-

"""
pwdcheck.pwdcheck
~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import

from pwdcheck.helpers import Dotdict

from .compat import builtin_str
from .cxty import Complexity
from .exceptions import PolicyError, PolicyParsingError
from .extras import Extras


# TODO: implement func for creating policy guidelines based on
#       policy-file input
# TODO: implement func that prints check output in JSON or YAML
#       format into stdout and allow to use script output with PIPEs.
#       (partially should be done at client side), here only smth
#       like :as_json and :as_yaml API calls
# TODO: create performance benchmark with testing a huge list of passwords
#       against policy with long history, blacklist and monster dictionary


def _pwd_ok_check(dct):
    cxty_dct = dct['complexity']
    extras_dct = dct['extras']

    # `data_dct.get("err", False)` - for unsupported policy param or case
    #                                when corresponding check should be
    #                                skipped (i.e. empty `data_dct`)
    cxty_errs = [data_dct.get("err", False) for data_dct in cxty_dct.values()]
    ext_errs = [data_dct.get("err", False) for data_dct in extras_dct.values()]

    return not any(cxty_errs + ext_errs)


def check(pwd, policy, pwd_dict=None, pwd_blacklist=None, pwd_history=None):
    # JSON case
    if isinstance(policy, builtin_str):
        try:
            cxty = Complexity.from_json(pwd, policy)
            extras = Extras.from_json(pwd, policy,
                                      pwd_dict=pwd_dict,
                                      pwd_blacklist=pwd_blacklist,
                                      pwd_history=pwd_history)
        except ValueError as err:
            # json.decoder.JSONDecodeError is inherited from ValueError
            # raised when invalid JSON in :policy str
            raise PolicyParsingError(err)
    # Common case
    elif isinstance(policy, dict):
        cxty = Complexity(pwd, policy)
        extras = Extras(pwd, policy,
                        pwd_dict=pwd_dict,
                        pwd_blacklist=pwd_blacklist,
                        pwd_history=pwd_history)
    else:
        raise PolicyError("unsupported policy data type")

    result = Dotdict()
    result.complexity = cxty.as_dict
    result.extras = extras.as_dict

    return _pwd_ok_check(result), result
