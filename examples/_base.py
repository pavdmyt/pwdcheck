# -*- coding: utf-8 -*-

"""
Basic building blocks to show pwdcheck API usage examples.
"""

import os

from docopt import docopt
from yaml import load


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


CLI_SPEC = """\
usage:
    pwdcheck <policy-file>
    pwdcheck (-h | --help)

options:
    -h --help                    Show this screen

"""


class CliExample(object):
    _cli_spec = CLI_SPEC

    @property
    def cli_args(self):
        return docopt(self._cli_spec)

    @staticmethod
    def _path_check(fpath):
        if not os.path.exists(fpath):
            raise IOError("{}: no such file".format(fpath))
        if not os.path.isfile(fpath):
            raise IOError("{}: is not a file".format(fpath))
        return fpath

    def run(self):
        # Boilerplate
        try:
            policy_path = self._path_check(self.cli_args['<policy-file>'])
        except IOError as err:
            print("Error: {}".format(err))
            return

        path_ext = os.path.splitext(policy_path)[-1]
        if path_ext == ".yaml":
            with open(policy_path, 'r') as fd:
                policy_data = load(stream=fd, Loader=Loader)
        elif path_ext == ".json":
            with open(policy_path, 'r') as fd:
                policy_data = fd.read()
        else:
            print("Error: unsupported policy file type")
            return

        # Application
        self.app_code(policy_data)

    def app_code(self, policy_data):
        # Should be implemented by child class
        raise NotImplementedError
