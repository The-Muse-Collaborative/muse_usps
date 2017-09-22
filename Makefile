.PHONY: help
help:
	@echo "Target     Description"
	@echo "========== ==========="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	 awk 'BEGIN {FS = ":.*?## "}; {printf "%-10s %s\n", $$1, $$2}'

.PHONY: test
test: ## Run unit tests and generate coverage.
	@bash -c "source test_env.sh && python setup.py -q nosetests"

.PHONY: lint
LINT_TARGETS := setup.py muse_usps
lint: ## Run pep8 and pylint checks on python files.
	pep8 $(LINT_TARGETS)
	pylint $(LINT_TARGETS)

.PHONY: docs
docs: ## Update HTML documentation.
	@cd docs && $(MAKE) html

.PHONY: hooks
hooks: ## Installs git pre-commit hook for the repository.
	@rm -f .git/hooks/pre-commit
	@printf "#!/usr/bin/env bash\nmake pre-commit" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

.PHONY: pre-commit
pre-commit: test lint ## Run all pre-commit checks.
