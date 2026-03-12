.PHONY: lint
lint:
	@echo "Linting with Ruff:"
	@uv run ruff check --fix-only src tests coding_style_format_example.py
	@uv run ruff check src tests coding_style_format_example.py
	@echo "Type checking with Ty"
	@uv run ty check src tests coding_style_format_example.py

.PHONY: test
test:
	@echo "Testing with coverage"
	@uv run coverage run
	@uv run coverage report

.PHONY: remove-built-docs
remove-built-docs:
	@echo "Removing any pre-built documentation from ./docs/build"
	@rm -rf docs/build

.PHONY: live-docs
live-docs: remove-built-docs
	@echo "Building live documentation to directory ./docs/build"
	@cd docs && uv run sphinx-autobuild source build --port 9000 --open-browser --host 127.0.0.1 --watch ../src

.PHONY: build-docs
build-docs: remove-built-docs
	@echo "Building documentation to directory ./docs/build"
	@cd docs && uv run sphinx-build -M html source build

.PHONY: build-docs-gh
build-docs-gh: remove-built-docs
	@echo "Building documentation for GitHub Pages to directory ./docs/build"
	@cd docs && uv run sphinx-build -W -b html source build