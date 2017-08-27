#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple CLI application that prints detailed error messages
if provided password policy violated.

pwdcheck API demonstration.
"""

from __future__ import absolute_import, print_function

from _base import CliExample


class ExampleApp(CliExample):

    def app_code(self, pwd_ok, result):
        if pwd_ok:
            print("Password conforms given policy")
            return

        def print_err(dct):
            for item in dct.values():
                if item.err:
                    print("Error: {}".format(item.err_msg))

        print_err(result.complexity)
        print_err(result.extras)


def main():
    my_app = ExampleApp()
    my_app.run()


if __name__ == '__main__':
    main()
