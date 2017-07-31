#!/bin/bash

# Reference:
# https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps

SRC="$HOME/PY_proj/pwdcheck/"
DST="$HOME/Dropbox/PythonProjects/pwdcheck"

# -v       : verbose
# -z       : compression (for network transfer)
# --delete : delete files from $DST
rsync -avz --delete $SRC $DST
