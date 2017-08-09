#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple CLI application that prints detailed error messages
if provided password policy violated.

pwdcheck API demonstration.
"""

from _base import CliExample
from pwdcheck.exceptions import BaseCheckError


class ExampleApp(CliExample):

    def app_code(self, pwd_ok, result):
        if pwd_ok:
            print("Password conforms given policy")
            return

        def raiser(dct):
            for item in dct.values():
                if item.exc:
                    raise item.exc

        try:
            raiser(result.complexity)
            raiser(result.extras)
        # same as:
        # except (ExtrasCheckError, ComplexityCheckError) as err:
        except BaseCheckError as err:
            print("'{}' : '{}' violated: {}"
                  .format(err.policy_param_name, err.param_name, err))


def main():
    my_app = ExampleApp()
    my_app.run()


if __name__ == '__main__':
    main()
