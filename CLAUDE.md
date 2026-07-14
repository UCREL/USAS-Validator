# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A Python library that validates and parses USAS (UCREL Semantic Analysis System) semantic tags — the tag scheme output by the USAS tagger for tokens/MWEs (e.g. `Z2/S2mf E3-`). It parses raw tag strings into structured Pydantic models and can load the full USAS tag-to-description mapping from a bundled YAML file.

## Commands

This project uses [`uv`](https://docs.astral.sh/uv/) for all environment/dependency management. **Never invoke `python` or `pip` directly — always go through `uv`**, and prefer `make` targets over calling the underlying tools directly.

```bash
uv sync --all-extras       # install deps (incl. docs extras) into .venv
make lint                  # ruff (fix-only pass, then check) + ty type check on src, tests, coding_style_format_example.py
make test                  # pytest via `uv run coverage run` + `uv run coverage report`
```

Dependency management:
```bash
uv add <package>           # runtime dependency
uv add --dev <package>     # dev dependency
uv remove <package>
uv run <script.py>
```

Run a single test (pytest args pass through `coverage run`, configured via `[tool.coverage.run] command_line = "-m pytest"` in pyproject.toml):
```bash
uv run coverage run -m pytest tests/test_utils.py::test_parse_usas_token_group -v
```

Docs (Sphinx, source in `docs/source`, built output in `docs/build`):
```bash
make live-docs              # live-reload docs server at http://127.0.0.1:9000, watches ../src
make build-docs              # one-off html build
make build-docs-gh           # strict (-W) build for GitHub Pages
```

## Architecture

- `src/usas_validator/usas_tag.py` — Pydantic models. `USASTag` represents a single parsed tag with its markers (positive/negative counts, rarity `%`/`@`, gender `m`/`f`, `c` antecedent, `n` neuter, idiom placeholder always `False`). `USASTagGroup` wraps a `list[USASTag]` — multiple tags in one group (joined by `/` in the raw text, e.g. `G1.2/S2mf`) represent a token with equal membership across all listed semantic categories.
- `src/usas_validator/utils.py` — the two public entry points:
  - `parse_usas_token_group(text, strict=False)`: splits whitespace-separated USAS tag groups, then `/`-separated tags within each group, and regex-matches each tag against `TAG_RE` (`^[A-Z](\d+)((\.\d+)+)?`), `PUNCT_RE` (`^PUNCT`), or `DF_RE` (`^Df`) before stripping marker suffixes. When `strict=False` (default) unparsable tags are silently dropped rather than raising — this is intentional, since production USAS tagger output can contain occasional junk.
  - `load_usas_mapper(usas_tag_descriptions_file, tags_to_filter_out)`: reads the bundled `data/usas/usas_mapper.yaml` (or a custom path) and recursively flattens its nested `title`/`description` structure into a flat `{tag: "title: ... description: ..."}` dict. Raises `KeyError` if a node has only one of `title`/`description` (malformed YAML), or a duplicate tag name is found across the tree.
- `src/usas_validator/data/usas/usas_mapper.yaml` — the canonical tag→description source data, packaged with the library via `importlib.resources`.
- `test/Multilingual-USAS/` — a vendored/external reference repo (upstream USAS lexicon resources across many languages); it is not part of this package's test suite (pytest `testpaths` is scoped to `tests/`) and generally shouldn't need editing for changes to this library.

## Code style (see @AGENTS.md for full detail)

- `match`/`case` over `if`/`elif`/`else` chains.
- Modern type hints only: built-in generics (`list`, `dict`), `X | None` unions — no `typing.Optional`/`Union`/`Dict`/`List`.
- Written for strict `ty` type checking; avoid `type: ignore` unless truly unavoidable.
- `pathlib.Path` for filesystem work, never `os.path`.
- All public functions/classes get Google-style docstrings with doctest-style `Examples:` blocks — `coding_style_format_example.py` is the canonical reference for the expected format (Args/Returns/Raises/Examples sections, no `self` in Args, etc).

## Claude settings in this repo

`.claude/settings.json` is generated, not hand-edited — regenerate it with:
```bash
cd .claude/hooks && uv run generate_settings.py > ../settings.json
```
It's built from the deny-list in `.claude/hooks/sensitive_patterns.py` plus a pre-tool-use hook (`.claude/hooks/block_sensitive_files.py`) that blocks reads/writes/edits to sensitive files (env files, credentials, etc.) even via indirect access like `Bash` calling Python. If you add new sensitive file patterns, edit `sensitive_patterns.py` and regenerate rather than hand-editing `settings.json`.
