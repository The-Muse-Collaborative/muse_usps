.PHONY: help
help:
	@echo "Target      Description"
	@echo "=========== ==================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	 awk 'BEGIN {FS = ":.*?## "}; {printf "%-11s %s\n", $$1, $$2}'

.PHONY: test
test: ## Run unit tests and generate coverage.
	@bash -c "source test_env.sh && nosetests --with-coverage \
	                                          --cover-package=muse_usps \
                                                  --cover-tests \
                                                  --cover-erase \
                                                  --cover-min-percentage=95"

.PHONY: lint
LINT_TARGETS := setup.py muse_usps
lint: ## Run pep8 and pylint checks on python files.
	pep8 $(LINT_TARGETS)
	pylint $(LINT_TARGETS)

.PHONY: docs
docs: ## Create HTML documentation.
	@cd doc && $(MAKE) html

.PHONY: docs-publish
docs-publish: docs ## Publishes built documentation to GitHub Pages.
	@cd doc/build && \
	 rm -rf repo && \
	 git clone -b gh-pages $$(git config --get remote.origin.url) repo && \
	 cd repo && \
	 git rm -rf . && \
	 find ../html -mindepth 1 -maxdepth 1 -exec mv {} . \; && \
	 git add . && \
	 git commit -m "Publishing updated documentation." && \
	 echo $$(git config --get remote.origin.url) | grep -q '^git@' || \
	 git remote set-url origin $$(git config remote.origin.url | \
	   sed "s|https://|https://$${GITHUB_USERNAME}:$${GITHUB_TOKEN}@|" | \
	   sed "s|github.com:|github.com/|") && \
	 git push origin gh-pages

.PHONY: hooks
hooks: ## Installs git pre-commit hook for the repository.
	@rm -f .git/hooks/pre-commit
	@printf "#!/usr/bin/env bash\nmake pre-commit" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

.PHONY: pre-commit
pre-commit: test lint ## Run all pre-commit checks.
