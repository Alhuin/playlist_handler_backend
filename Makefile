NAME := dslr
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)
PY := python
.DEFAULT_GOAL := help

.PHONY: help

#	Utils

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     		install packages and prepare environment"
	@echo "  clean       		remove all temporary files"
	@echo "  fclean       		clean and remove poetry virtual environment"
	@echo "  lint        		run the code linters"
	@echo "  format      		reformat code"
	@echo "  test        		run all the tests"
	@echo "  pre-commit     	run pre-commit config"
	@echo ""
	@echo "To give arguments to a target threw make, please use 'make <target> -- <arguments>'"
	@echo "	eg: make describe -- -h"

.PHONY: install
install: $(INSTALL_STAMP)

$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage

.PHONY: fclean
fclean: clean
	$(POETRY) env remove $(shell $(POETRY) env list | grep -E '(.*?) \(Activated\)' | awk '{print $$1}')

.PHONY: lint
lint: install
	$(POETRY) run isort --profile=black --lines-after-imports=2 --check-only .
	$(POETRY) run black --check --diff .
	$(POETRY) run flake8 --max-line-length=120

.PHONY: format
format: install
	$(POETRY) run isort --profile=black --lines-after-imports=2 .
	$(POETRY) run black .

.PHONY: test
test: install
	$(POETRY) run coverage run --source='.' manage.py test $(filter-out $@,$(MAKECMDGOALS))
	$(POETRY) run coverage report --show-missing

.PHONY: pre-commit
pre-commit: install
	$(POETRY) run pre-commit run --all-files

.PHONY: run
run: install
	$(POETRY) run $(PY) manage.py runserver

%:
	@:
