# Devtools and CI

## Local developer toolbox (`devtools/tests/`)

The primary local workflow lives in `devtools/tests/`. It wraps `pytest` and
`coverage` with a `Makefile` designed for interactive analysis.

Run from that directory:

```bash
cd devtools/tests
make help           # full target + variable reference
```

### Core test and coverage targets

| Target | Description |
|--------|-------------|
| `make test` | Run the full suite (tests + doctests in `molsysmt/basic/`). `peptide_parity` tests are auto-deselected. |
| `make coverage` | Same as `test` with terminal output + writes `coverage.json` and `coverage.xml`. |
| `make coverage-html` | Run tests with coverage and generate `htmlcov/index.html`. |
| `make coverage-open` | Generate the HTML report and open it in the browser. |
| `make coverage-json` | Force a fresh run: deletes `coverage.json` and regenerates it. |
| `make slowest` | Show the slowest pytest items (`--durations=25`). |

Key variables (overridable on the command line):

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_DIR` | `../../tests` | Unit test root |
| `DOCTEST_DIR` | `../../molsysmt/basic` | Doctest source root |
| `NPROC` | `14` | Workers for `pytest-xdist` (`-n`) |
| `DIST_MODE` | `loadfile` | `pytest-xdist` distribution mode |
| `PACKAGE` | `molsysmt` | Package passed to `--cov` |

`peptide_parity` tests are auto-deselected at collection time by
`tests/conftest.py` (via `pytest_collection_modifyitems`) unless the mark is
explicitly requested with `-m`.  No flag needs to be added to the command line
— the deselection is transparent.  To run the parity suite explicitly:

```bash
pytest -m peptide_parity tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py
# or via the shell helper:
devtools/tests/run_tiers.sh peptide_extended
```

### Coverage analysis targets

All analysis targets reuse an existing `coverage.json` if present (with a
notice printed to the terminal). Use `make coverage-json` to force a fresh run
first.

| Target | Description |
|--------|-------------|
| `make coverage-hotspots` | Show the N lowest-coverage files. `HOTSPOT_TOP=15`, `SUBPACKAGE=` |
| `make coverage-packages` | Aggregate coverage by subpackage. `PACKAGE_DEPTH=1` |
| `make coverage-top` | Print total (depth 0) then depth-N breakdown. |
| `make coverage-map` | Hierarchical textual coverage map. `MAP_DEPTH=2`, `SORT=coverage\|name` |
| `make coverage-markdown` | Generate `coverage_summary.md` + `coverage_summary.json`. |

Common workflows:

```bash
make coverage-hotspots SUBPACKAGE=molsysmt.form   # worst files in form/
make coverage-packages PACKAGE_DEPTH=2            # e.g. molsysmt.form.file_pdb
make coverage-top PACKAGE_DEPTH=2
make coverage-map MAP_DEPTH=3 SORT=name
make coverage-markdown HOTSPOT_TOP=20
```

### Threshold checking and history

| Target | Description |
|--------|-------------|
| `make coverage-check` | Validate against thresholds in `coverage_thresholds.json`. |
| `make coverage-diff` | Compare current `coverage.json` against a baseline file. |
| `make coverage-history` | Append the current summary to `coverage_history.json`. |
| `make coverage-history-report` | Print the last N rows from `coverage_history.json`. |

The thresholds in `coverage_thresholds.json` are aspirational targets for the
1.0.0 stabilization pass (75% overall, 80–85% for core subpackages). They are
**not** enforced automatically — use `make coverage-check` manually to gauge
progress.

### Module/test association analysis

```bash
make module-test-map    # produces module_test_map.json
make module-test-gaps   # print modules with no associated tests (heuristic)
```

The matching is heuristic (path/name similarity). Use this to find areas that
have no test file at all — not as a proof of full coverage.

### CI pipeline target

```bash
make ci NPROC=12
```

Runs `coverage.json → coverage-markdown → coverage-check → coverage-history →
module-test-map` in sequence. Intended for manual periodic snapshots, not as an
automated gate.

### CI mirror targets

These targets reproduce locally what the GitHub Actions workflows do:

| Target | Description |
|--------|-------------|
| `make smoke` | Run the smoke tier (~4 tests). Mirrors `ci-smoke.yaml`. |
| `make weekly` | Full suite with coverage — produces `coverage.xml` and `junit.xml`. Mirrors `ci-weekly.yaml`. |
| `CODECOV_TOKEN=<token> make upload-codecov` | Upload `coverage.xml` to Codecov manually. See procedure below. |

### Manual Codecov upload procedure

Use this when you want to update the Codecov report without waiting for the
weekly CI run (e.g. after a significant coverage improvement).

**Requirements:**
- `codecov-cli` installed: `pip install codecov-cli`
- The org-level token stored in LastPass under `"codecov/token"`

**Step 1 — generate coverage.xml from the repo root:**

```bash
make weekly
```

`make weekly` runs pytest from the repo root so that paths in `coverage.xml`
are repo-root-relative. **Do not use `make coverage`** for this — it can
produce absolute local paths that Codecov cannot map to GitHub files.

**Step 2 — push any pending commits:**

Codecov must be able to find the commit SHA on GitHub before it can associate
the report with it.

```bash
git push
```

**Step 3 — upload:**

```bash
CODECOV_TOKEN=$(lpass show --password "codecov/token") make upload-codecov
```

The target runs `codecovcli upload-process` with:
- `--sha` / `--branch` auto-detected from the local git state
- `--git-service=github`
- `--network-root-folder=.` — normalises any residual absolute paths in the XML
- `--disable-search` — only uploads `coverage.xml`, ignores other files

**Step 4 — verify:**

The command prints a URL such as:

```
https://app.codecov.io/github/uibcdf/molsysmt/commit/<sha>
```

Allow ~30 seconds for Codecov to process the upload. Open the URL to confirm
the report appears.

**Why the local number differs from Codecov:**

Codecov blends line coverage and branch coverage into its reported percentage.
The local `make coverage-top` shows line coverage only. A ~5% gap between the
two is normal. Running `make weekly` after adding `relative_files = True` to
`.coveragerc` further reduces the gap by ensuring paths map correctly.

### Cleanup

```bash
make clean     # removes htmlcov/, .coverage, coverage.json, coverage.xml,
               # junit.xml, and summary files.
               # coverage_history.json is intentionally kept (persistent record)
```

---

## Tiered test helpers (`devtools/tests/run_tiers.sh`)

A lightweight shell script for focused test subsets:

```bash
devtools/tests/run_tiers.sh smoke            # 4-file fast gate
devtools/tests/run_tiers.sh build_topology   # peptide build + topology logic
devtools/tests/run_tiers.sh peptide_extended # 40-sequence LEaP parity suite
```

The `peptide_extended` tier is equivalent to running:
```bash
pytest -m peptide_parity tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py
```

---

## Active CI (GitHub Actions)

The repository currently contains these testing and validation workflows:

### `ci-devguide.yaml` — developer-guide changes

- Trigger: changes to `devguide/`, its validator, or the workflow itself.
- Runs: `python devtools/scripts/validate_devguide.py` without installing
  scientific dependencies.
- Purpose: reject broken local links, machine-specific paths, and references to
  retired developer-guide filenames.

### `ci-smoke.yaml` — on every push / PR to `main`

- Trigger: push or PR to `main` (skipped if commit message or PR title contains
  `[skip ci]`, or PR branch contains `skip-ci`). Also dispatchable manually.
- Matrix: `ubuntu-latest`, Python `3.13` only.
- Timeout: 15 minutes.
- Runs: `devtools/tests/run_tiers.sh smoke` (~4 tests).
- Also runs: `python devtools/scripts/validate_form_adapters.py`, including the
  explicit-tier completeness check and attribute-delivery debt ratchet.
- Purpose: fast signal that nothing is catastrophically broken.
- Concurrency: cancels in-progress runs on the same ref.

### `ci-weekly.yaml` — every Monday at 09:00 UTC

- Trigger: weekly schedule + manual dispatch.
- Matrix: `ubuntu-latest` × `{3.11, 3.12, 3.13}`.
- Timeout: 180 minutes per combination.
- Runs the Scientific Truth Suite as an explicit early gate after importing and
  reporting the resolved MDTraj and MDAnalysis versions. The test environment
  includes both external oracles, so this gate must not rely on optional skips.
- Runs: full suite with `--cov=molsysmt --cov-report=xml --junitxml=junit.xml`.
- Coverage and test results uploaded to Codecov from the Python `3.13` run only.
- Supported Python versions: `3.11`, `3.12`, and `3.13`.

### `ci-full.yaml` — manual dispatch only (pre-release gate)

- Trigger: `workflow_dispatch` only.
- Matrix: `(ubuntu-latest + macos-latest)` × `{3.11, 3.12, 3.13}` = 6 combinations.
- Timeout: 180 minutes per combination.
- Runs: `pytest -q --color=yes --junitxml=junit.xml` (no coverage upload).
- Purpose: validate all supported platforms before release candidates.

### `ci-rust-wheels.yaml` — native distribution gate

- Trigger: manual dispatch for the complete release matrix; pull requests that
  affect the native build run the Linux x86_64 boundary.
- Builds one `cp311-abi3` wheel for Linux x86_64 immediately. Its artifact
  starts the Python 3.11–3.13 public installed-runtime smokes and NumPy-floor
  checks without waiting for slower portability runners.
- Builds Linux aarch64, macOS x86_64/arm64, and Windows x86_64 in parallel.
  Their installed-extension checks complete the five-platform matrix.
- Runs Rust formatting, Clippy, unit, security, dependency, and license checks,
  plus a source-distribution round trip.
- Keeps normal pytest and the installed public-runtime validator authoritative;
  Conda publication is a separate delivery track.

Before dispatching the complete matrix, build a clean local wheel and run
`devtools/scripts/validate_installed_molsysmt.py` from outside the checkout in
an isolated environment containing the controlled hard sibling sources. The
environment should deliberately omit optional packages such as OpenMM. This
preflight exercises form discovery as well as representative conversion,
selection, geometry, PBC, PCA, SASA, and topology operations. It cannot replace
the platform matrix, but it detects shared installed-runtime defects before
the slowest native runner completes.

### Other validation and delivery workflows

- `ruff.yaml` runs the configured Ruff correctness checks on Python changes.
- `benchmarks.yml` compares a benchmark run with the stored baseline on pull
  requests. Because hosted runners are noisy, investigate a failure before
  treating a 15% delta as a deterministic regression.
- `test_import.yaml` provides a manually dispatched import check.
- `sphinx_docs_to_gh_pages.yaml` builds and publishes documentation.
- `build_and_upload_conda_packages.yaml` builds Conda packages when dispatched.
- `pr_agent.yaml` is repository automation, not a software validation gate.

### Python version policy

Package metadata and release workflows support Python **3.11–3.13**. Python
3.10 is outside the package contract and must not be reintroduced into package
classifiers, `requires-python`, Conda build matrices, or support badges.

### Skipping CI

Add `[skip ci]` to the commit message or PR title to suppress `ci-smoke.yaml`
on documentation-only or bookkeeping commits. Weekly and full-matrix workflows
ignore this tag.

### Release validation scripts (run manually)

- `devtools/scripts/validate_dependencies.py`
- `devtools/scripts/validate_devguide.py`
- `devtools/scripts/validate_resources.py`
