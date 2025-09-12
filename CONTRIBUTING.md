# CONTRIBUTING.md

## Ground Rules

- **Code of Conduct**: Be respectful and constructive. Reports: `info@civicinterconnect.org`.
- **License**: All contributions are accepted under the repo's **MIT License**.

---

## DEV 1. Start Locally

Setup development environment (commands are for cross-platform PowerShell. Install on macOS/Linux as needed):

```pwsh
uv venv
.\.venv\Scripts\activate
uv pip install --upgrade pip setuptools wheel
uv pip install --only-binary=:all: -e ".[dev]"
pre-commit install
pytest -q
```

## DEV 2. Validate Changes

Run all checks and build verification:

```pwsh
ruff format .
ruff check --fix
ruff check
mkdocs build
pre-commit run --all-files
pytest -q
```

## DEV 3. Build and Inspect Package

```pwsh
py -m build

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
git push origin main
```

## DEV 8. Git tag and Push tag

```shell
git tag vx.y.z -m "x.y.z"
git push origin vx.y.z
```

> A GitHub Action will **build**, **publish to PyPI** (Trusted Publishing), **create a GitHub Release** with artifacts, and **deploy versioned docs** with `mike`.

> You do **not** need to run `gh release create` or upload files manually.
