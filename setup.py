#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup


LIBNAME = "pwdcheck"


def read_dunder(package, dunder):
    init_path = os.path.join(package, '__init__.py')
    with open(init_path, 'r') as fd:
        for line in fd:
            if line.startswith(dunder + " ="):
                return line.split()[-1].strip().strip("'")


# Get package metadata
version = read_dunder(LIBNAME, "__version__")
author = read_dunder(LIBNAME, "__author__")
email = read_dunder(LIBNAME, "__email__")
license_ = read_dunder(LIBNAME, "__license__")


# import codecs
# with codecs.open('requirements.txt', encoding='utf-8') as fd:
#     required = fd.read().splitlines()
required = []


setup(
    name=LIBNAME,
    version=version,
    author=author,
    author_email=email,
    description='Check password against given password policy',
    url='',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=required,
    classifiers=(
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
