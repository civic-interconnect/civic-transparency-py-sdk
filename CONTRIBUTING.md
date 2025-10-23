# CONTRIBUTING.md

This repo hosts the **Civic Transparency Python SDK** under the **MIT License**.
Goals: clarity, privacy-by-design, easy collaboration.

> tl;dr: Open an Issue/Discussion first for non-trivial changes, keep PRs small, and run the quick local checks.
---

## Ground Rules

- **Code of Conduct**: Be respectful and constructive. Reports: `info@civicinterconnect.org`.
- **License**: All contributions are accepted under the repo's **MIT License**.
- **Single Source of Truth**: The definitions are in `src/ci/transparency/spec/schemas/`. Documentation should not contradict these files.

---

## Before You Start

**Open an Issue or Discussion** for non-trivial changes so we can align early.

---

## Making Changes

- Follow **Semantic Versioning**:
  - **MAJOR**: breaking changes
  - **MINOR**: backwards-compatible additions
  - **PATCH**: clarifications/typos
- When things change, update related docs, examples, and `CHANGELOG.md`.

---

## Local Dev with `uv`

### Prerequisites

- Python **3.12+** (3.13 supported)
- Git, VS Code (optional), and **[uv](https://github.com/astral-sh/uv)**

### One-time setup

```bash
uv python pin 3.12
uv venv
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
```

## Validate Local Changes

```bash
git pull
git add .
uvx ruff check . --fix
uvx ruff format .
uvx pyright
uv run deptry .
uv run pytest
uv run mkdocs build --strict
```

Run the project hooks (twice, if needed):

```bash
pre-commit run --all-files
```

## DEV 3. Build and Inspect Package

```pwsh
uv build

$TMP = New-Item -ItemType Directory -Path ([System.IO.Path]::GetTempPath()) -Name ("wheel_" + [System.Guid]::NewGuid())
Expand-Archive dist\*.whl -DestinationPath $TMP.FullName
Get-ChildItem -Recurse $TMP.FullName | ForEach-Object { $_.FullName.Replace($TMP.FullName + '\','') }
Remove-Item -Recurse -Force $TMP
```

## DEV 4. Preview Docs

```pwsh
mkdocs serve
```

Open: <http://127.0.0.1:8000/>

## DEV 5. Clean Artifacts

```pwsh
Get-ChildItem -Path . -Recurse -Directory -Filter "*__pycache__*" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Directory -Filter ".*_cache"  | Remove-Item -Recurse -Force
Get-ChildItem -Path "src" -Recurse -Directory -Name "*.egg-info" | Remove-Item -Recurse -Force
Remove-Item -Path "build", "dist", "site" -Recurse -Force
```

## DEV 6. Update Docs & Verify

Update `CHANGELOG.md` and `pyproject`.toml dependencies.
Ensure CI passes:

```shell
pre-commit run --all-files
pytest -q
```

## DEV 7. Git add-commit-push Changes

```shell
git add .
git commit -m "Prep vx.y.z"
git push -u origin main
```

## DEV 8. Git tag and Push tag

```shell
git tag vx.y.z -m "x.y.z"
git push origin vx.y.z
```

> A GitHub Action will **build**, **publish to PyPI** (Trusted Publishing), **create a GitHub Release** with artifacts, and **deploy versioned docs** with `mike`.

> You do **not** need to run `gh release create` or upload files manually.
