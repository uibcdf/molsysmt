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
| `make test` | Run the full suite (tests + doctests in `molsysmt/basic/`). Excludes `peptide_parity` tests by default. |
| `make coverage` | Same as `test` with a compact `--cov-report=term-missing:skip-covered` output. |
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

The `-m "not peptide_parity"` flag is baked into `PYTEST_FLAGS` so the
40-sequence LEaP parity suite does not run in routine `make test` or `make coverage`.
To run it explicitly:

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

### Cleanup

```bash
make clean     # removes htmlcov/, .coverage, coverage.json, summary files
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

## Planned CI (not yet active)

The following describes the intended automated CI setup once MolSysMT is ready
for a public release gate. It is **not** currently active.

Planned gate:
- Push/PR: fast tier on Ubuntu, Python 3.13.
- Full matrix (weekly + manual dispatch): Ubuntu + macOS, Python 3.10–3.13.
- Documentation builds must not introduce warnings.
- Optional dependencies must be guarded and skipped when unavailable.

Release validation scripts (run manually until CI is active):
- `scripts/validate_dependencies.py`
- `scripts/validate_resources.py`
