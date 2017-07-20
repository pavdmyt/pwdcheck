# -*- coding: utf-8 -*-

from getpass import getpass
from pprint import pprint

from pwdcheck import check


def main():
    policy = dict(
        minlen=10,  # length
        umin=1,     # uppercase
        lmin=1,     # lowercase
        dmin=1,     # digits
        omin=1,     # other (including special chars)
    )

    pwd = getpass()
    res = check(pwd, policy)
    pprint(res)


if __name__ == '__main__':
    main()
