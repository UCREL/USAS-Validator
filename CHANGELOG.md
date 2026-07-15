# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.1.0](https://github.com/UCREL/USAS-Validator/releases/tag/v0.1.0)

### Added

- `USASTag` and `USASTagGroup` Pydantic models for representing parsed USAS semantic tags.
- `parse_usas_token_group` for parsing raw USAS tag group strings into `USASTagGroup` objects.
- `load_usas_mapper` for loading the bundled USAS tag-to-description mapping.
- `keep_valid_usas_tags` for filtering a USAS tag string down to only the tags present in a
  given set of valid tags.
- `mwe_token_indexes_from_slices`, `mwe_token_labels_from_indexes`, and
  `mwe_labels_from_pymusas_indexes` for converting Multi Word Expression (MWE) index slices,
  including PyMUSAS's raw per-token index format, into per-token MWE labels.
