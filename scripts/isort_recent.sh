#!/bin/bash

# Use isort on a recently modified *.py files.
# Recently modified are those which are in `git status` output.
RECENT_PY=$(git status -s | grep -o "^ M.*\.py$" | awk '{ print $2 }')


# Isort
echo "==> Isort"
for checkable in $RECENT_PY
do
    echo "-> $checkable"
    isort $checkable
done

exit 0
