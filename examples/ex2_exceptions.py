#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple CLI application that prints detailed error messages
if provided password policy violated.

pwdcheck API demonstration.
"""

from getpass import getpass

import pwdcheck
from _base import CliExample
from _data import BLACKLIST, HISTORY, PWD_DICT


class ExampleApp(CliExample):

    def app_code(self, policy_data):
        pwd = getpass()
        pwd_ok, res = pwdcheck.check(pwd, policy_data,
                                     pwd_dict=PWD_DICT,
                                     pwd_blacklist=BLACKLIST,
                                     pwd_history=HISTORY)

        if pwd_ok:
            print("Password conforms given policy")
            return

        def raiser(dct):
            for item in dct.values():
                if item.exc:
                    raise item.exc

        try:
            raiser(res.complexity)
            raiser(res.extras)
        except ValueError as err:
            print("Error: {0}".format(err))


def main():
    my_app = ExampleApp()
    my_app.run()


if __name__ == '__main__':
    main()
