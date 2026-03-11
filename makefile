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

.PHONY: live-docs
live-docs:
	@cd docs && uv run sphinx-autobuild source build --port 9000 --open-browser --host 127.0.0.1

.PHONY: build-docs
build-docs:
	@echo "Building documentation to directory ./docs/build"
	@cd docs && uv run sphinx-build -W -b html source build