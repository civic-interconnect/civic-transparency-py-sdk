# Changelog

All notable changes to this project will be documented in this file.

The format follows **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

### Added
- (placeholder) Notes for the next release.

---

## [0.1.2] - 2025-10-23

### Changed
- Updated GitHub actions.

---

## [0.1.1] - 2025-10-11

### Changed
- Renamed repo from `civic-transparency-sdk` to `civic-transparency-py-sdk`
- PyPi package remains `civic-transparency-sdk` as specified in pyproject.toml name.

---

## [0.1.0] - 2025-09-11

### Added
- **Initial release** of the **Civic Transparency SDK**.
- Generators for simple civic transparency worlds producing JSONL windows.
- Utilities to convert JSONL worlds into DuckDB (`jsonl_to_duckdb`).
- Initial README with reproducible commands and seed values.
- Packaged schemas and OpenAPI reference (mirrors `civic-transparency-spec`) for downstream private verification work.

---

## Notes on versioning and releases

- **SemVer policy**
  - **MAJOR** - breaking API/schema or CLI changes.
  - **MINOR** - backward-compatible additions and enhancements.
  - **PATCH** - documentation, tooling, or non-breaking fixes.
- Versions are driven by git tags via `setuptools_scm`.
  Tag the repository with `vX.Y.Z` to publish a release.
- Documentation and badges are updated per tag and aliased to **latest**.

[Unreleased]: https://github.com/civic-interconnect/civic-transparency-py-sdk/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/civic-interconnect/civic-transparency-py-sdk/releases/tag/v0.1.2
[0.1.1]: https://github.com/civic-interconnect/civic-transparency-py-sdk/releases/tag/v0.1.1
[0.1.0]: https://github.com/civic-interconnect/civic-transparency-py-sdk/releases/tag/v0.1.0
