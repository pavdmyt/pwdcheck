# -*- coding: utf-8 -*-

"""
Basic building blocks to show pwdcheck API usage examples.
"""

from __future__ import absolute_import

import os
import sys
from getpass import getpass

from docopt import docopt
from yaml import load

# $ pip install -e pwdcheck
# XXX: should be before pwdcheck import
import _install_hook

import pwdcheck
from _data import BLACKLIST, HISTORY, PWD_DICT


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
        argv = sys.argv[1:]
        skipper = "--skip-upd"
        if skipper in argv:
            argv.remove(skipper)
        return docopt(self._cli_spec, argv=argv)

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
        pwd_ok, result = self.pre_setup(policy_data)
        self.app_code(pwd_ok, result)

    @staticmethod
    def pre_setup(policy_data):
        pwd = getpass()
        pwd_ok, result = pwdcheck.check(pwd, policy_data,
                                        pwd_dict=PWD_DICT,
                                        pwd_blacklist=BLACKLIST,
                                        pwd_history=HISTORY)
        return pwd_ok, result

    def app_code(self, pwd_ok, result):
        # Should be implemented by child class
        raise NotImplementedError
