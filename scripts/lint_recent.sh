#!/bin/bash

# Use pylint and flake8 on a recently modified *.py files.
# Recently modified are those which are in `git status` output.
RECENT_PY=$(git status -s | grep -o "^ M.*\.py$" | awk '{ print $2 }')


# pylint
echo "==> Pylint"
for checkable in $RECENT_PY
do
    pylint $checkable -rn -f colorized
done


# flake8
echo ""
echo "==> flake8"
flake8 $RECENT_PY

exit 0
