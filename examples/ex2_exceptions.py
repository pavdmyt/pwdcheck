#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple CLI application that prints detailed error messages
if provided password policy violated.

pwdcheck API demonstration.
"""

from _base import CliExample
from pwdcheck.exceptions import ComplexityCheckError


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
        # except ValueError as err:
        #     print("Error: {0}".format(err))
        except ComplexityCheckError as err:
            print("'{}' : '{}' violated: {} given, but {} required"
                  .format(err.policy_param_name,
                          err.param_name,
                          err.aval,
                          err.pval))


def main():
    my_app = ExampleApp()
    my_app.run()


if __name__ == '__main__':
    main()
