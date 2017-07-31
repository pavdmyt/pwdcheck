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

        def print_err(dct):
            # TODO: I don't like the necessity to refer to .values()
            for item in dct.values():
                if item.err:
                    print("Error: {}".format(item.err_msg))

        print_err(res.complexity)
        print_err(res.extras)


def main():
    my_app = ExampleApp()
    my_app.run()


if __name__ == '__main__':
    main()
