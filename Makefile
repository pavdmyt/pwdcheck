OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

help:
	@echo "---------- Code Style ----------"
	@echo "flake            - check code style with flake8"
	@echo "lint-all         - check code style with pylint"
	@echo "lint-recent      - check code style in recently modified files"
	@echo "isort-all        - sort imports in whole project (be careful!)"
	@echo "isort-recent     - sort imports in recently modified files"
	@echo ""
	@echo "---------- Manage Deps ---------"
	@echo "req-check        - check requirements.in contents are up to date"
	@echo "req-check-dev    - check requirements-dev.in contents are up to date"
	@echo "compile-req      - compile: requirements.in -> requirements.txt"
	@echo "compile-req-dev  - compile: requirements-dev.in -> requirements-dev.txt"
	@echo "install          - install minimal deps set to run Project"
	@echo "install-dev      - install all deps including development"
	@echo ""
	@echo "----------- Testing ------------"
	@echo "test             - run all tests"
	@echo ""
	@echo "------------ Misc --------------"
	@echo "clean-pyc        - remove Python file artifacts"

#
# Code style
#

flake:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@flake8 .

lint-all:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@pylint --rcfile=.pylintrc pwdcheck/ --reports n --output-format=colorized

lint-recent:
	@./scripts/lint_recent.sh

isort-all:
	isort -rc --atomic --verbose .

isort-recent:
	@./scripts/isort_recent.sh


#
# Manage dependencies
#

# PyPIup checks
req-check:
	@echo "$(OK_COLOR)==> Checking dependencies are up to date...$(NO_COLOR)"
	@pypiup -r requirements.in

req-check-dev:
	@echo "$(OK_COLOR)==> Checking dev dependencies are up to date...$(NO_COLOR)"
	@pypiup -r requirements-dev.in


# Compile requirements
compile-req:
	pip-compile requirements.in

compile-req-dev:
	pip-compile requirements-dev.in


# Install basic dependencies
install:
	pip install -r requirements.txt

# Install basic + development dependencies
install-dev:
	@echo "$(OK_COLOR)==> Installing pip-tools $(NO_COLOR)"
	pip install pip-tools
	@echo "$(OK_COLOR)==> Sync requirements.txt with requirements-dev.txt $(NO_COLOR)"
	pip-sync requirements.txt requirements-dev.txt


#
# Testing
#

test: clean-pyc flake
	@echo "$(OK_COLOR)==> Runnings tests ...$(NO_COLOR)"
	@py.test -v


#
# Misc
#

clean-pyc:
	@echo "$(OK_COLOR)==> Cleaning ...$(NO_COLOR)"
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
