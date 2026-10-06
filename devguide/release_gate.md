# Release Gate

The single normative checklist for tagging a MolSysMT release (in particular 1.0.0).
It consolidates what was previously scattered across workflow comments and the 1.0
audit. Closes audit risk **R2** in
`archive/release_1_0/release_1_0_independent_gate_audit.md` and supports blocker **B1**.
The current pre-release work order is maintained in
[`release_1_0_execution_plan.md`](pending_proposals/release_1_0_execution_plan.md).
Current completion, active stage, and evidence are recorded in
[`release_1_0_status.md`](release_1_0_status.md).
The accepted [scope freeze](release_1_0_scope.md) defines what needs qualification;
it does not waive any gate below or itself authorize publication.

A release is cut **only** when every gate below is green **on the exact commit being
tagged**. Green gates on an earlier commit or a dirty tree do not count.

## 0. Preconditions (the tree and the commit)

- **Clean working tree.** `git status --porcelain` is empty on the tag commit. A release
  cannot be cut from a tree with uncommitted work (audit blocker B1).
- **The tag commit must actually run CI.** Ordinary direct pushes run the bounded
  smoke tier; maintainers may deliberately use `[skip ci]` during development.
  The release candidate commit (and the tag) **must not** carry `[skip ci]`.
  Run the full release matrix explicitly on the exact candidate commit.
- **Version metadata is consistent** with the intended tag (versioningit derives it from
  the tag; `pyproject.toml` `requires-python` and classifiers list 3.11–3.14).

## 1. Fast gates — `devtools/scripts/release_gate.py`

Run locally before triggering the heavy matrix:

```bash
python devtools/scripts/release_gate.py
```

It aggregates every cheap, deterministic gate into one PASS/FAIL verdict:

| Gate | Script |
|---|---|
| Public API stability registry | `validate_api_stability.py` |
| Public function support tiers | `validate_function_tiers.py` |
| Form adapter delivery contracts | `validate_form_adapters.py` |
| Tier 1 conversion fidelity (accepted-debt baseline) | `audit_conversion_fidelity.py` |
| Scientific evidence registry structure (does not execute tests) | `validate_scientific_evidence.py` |
| Runtime dependency floors, Conda/environment copies and CI source routes | `audit_dependency_contract.py` |
| No top-level soft-dependency imports | `validate_dependencies.py` |
| Developer-guide integrity | `validate_devguide.py` |
| Four Paths course structure | `validate_course.py` |
| Demo assets / H5MSM fixtures | `validate_demo_assets.py` |
| Resource manifests | `validate_resources.py` |
| Citation and Zenodo metadata | `validate_citation.py` |
| Rust kernel hot paths (no libm rounding calls) | `check_rust_hot_paths.py` |
| Public-API smoke (import + convert + get + select + get_center) | (inline) |

`ruff check molsysmt` must also pass. These gates are fast (seconds) and must be
**100% green**. They carry no unbaselined accepted debt. Tier 1 conversion
*coverage* may contain explicitly accepted non-exhaustive edges, but their
authoritative count belongs to the executable fidelity baseline and its report,
not to this normative guide.

The former fidelity WIP gap is
[archived as resolved](archive/resolved_bugs/conversion_fidelity_wip_contract_gaps.md).
The executable baseline remains authoritative: accepted non-exhaustive routes
are visible debt, while any new unclassified debt fails this gate.

The fast scientific-evidence validator certifies registry structure only. Its
`validated` counts are declarations backed by addressable, assertion-bearing
nodes, not a record that those nodes passed in the current environment.

## 2. Heavy gate — the full test matrix (`ci-full.yaml`)

The fast gates do not run the test suite. Before tagging, the **full pytest matrix must
be green on the exact committed candidate**:

- `ci-full.yaml` (manual `workflow_dispatch`): ubuntu-latest + macos-15 arm64 ×
  {3.11, 3.12, 3.13, 3.14} = 8 combinations. Each job runs the fast release gate,
  the registered scientific evidence through
  `execute_scientific_evidence.py --receptor=ci`, Ruff, and the full pytest suite
  through pytest-receptor's CI mode (doctests included via `pytest.ini`); pytest
  remains the result authority. The scientific step must emit a certificate with
  every registered node collected and zero failures, errors, or skips.

The four-minor Linux `ci-weekly.yaml` matrix recovers skipped-commit debt and
also tests macOS arm64 on the routine Python 3.14 minor at least weekly. It
does not replace the eight-cell release matrix.

Do not substitute a partial or single-platform run.

## 3. Native wheel artifacts

- `ci-rust-wheels.yaml` must pass for the supported Linux x86_64/aarch64 and
  macOS arm64 target, including Python 3.11--3.14, the declared NumPy
  floor/current checks, and installed public-runtime smoke.
- Windows x86_64 remains an experimental portability target. Its wheel build,
  audit, and installed-extension checks are retained, but are non-blocking for
  1.0 until Windows has a functional matrix comparable to Linux and macOS.
- A green Windows artifact is evidence of buildability, not a declaration of
  supported-platform status.

## 4. Native Conda artifacts

- A green build/upload job is not sufficient evidence that a Conda artifact is
  installable. Query the published channel records and inspect the runtime constraints
  for the one ABI3 artifact on every native platform. Each artifact must use the
  `pyabi3` build string, retain its native subdirectory with CEP 20's `noarch: python`
  relocation marker, declare `python >=3.11,<3.15`, and carry the `cpython >=3.11` and
  `_python_abi3_support` requirements without an exact `python_abi` constraint.
- `validate_conda_staging.yaml` must install the exact coordinated MolSysMT/MolSysViewer
  versions with normal CPython on all four native platforms crossed with Python
  3.11--3.14 for the Python 3.14 candidate. All four runtime cells for a platform
  must resolve the same MolSysMT
  artifact. The installed version, provenance, native extension, declared py-mmcif
  runtime, offline bundled-BCIF conversion and Viewer resources must pass before the
  release artifacts are published to `main`.
- A corrective staging build must increment the build number instead of overwriting the
  defective coordinate. A staged release promotes those exact digest-verified bytes to
  `main`; the GitHub Release event must not rebuild or upload another file for that
  version. The committed `devtools/conda-build/release_plan.toml` selects the route;
  a direct release is permitted only when the registry confirms the version is absent
  under every label. The manual promotion workflow retains a receipt for each native
  artifact and verifies the public record independently.

## 5. Documentation build

- `sphinx_docs_to_gh_pages.yaml` builds the docs (`nb_execution_mode = "off"`). The build
  must be warning-clean for the course tree (no "toctree contains reference to nonexistent
  document"); `validate_course.py` guards the structure statically, the build confirms it.

## 6. Sign-off checklist (all must hold on the tag commit)

- [ ] Working tree clean; tag commit does **not** carry `[skip ci]`.
- [ ] `python devtools/scripts/release_gate.py` → all fast gates PASS.
- [ ] Registered scientific evidence execution → every cited node passes with zero
      skips and its JSON certificate identifies the tag candidate.
- [ ] `ruff check molsysmt` → clean.
- [ ] `ci-full.yaml` → green on all eight Python 3.11--3.14 Linux/macOS
      combinations, with its manual input naming the exact MolSysViewer
      candidate SHA. The 16-cell installed Conda pair must also pass before
      claiming 3.14 support.
- [ ] `ci-rust-wheels.yaml` → supported Linux/macOS jobs green; Windows result recorded
      as experimental evidence and not treated as a release blocker.
- [ ] Native Conda channel metadata contains exactly one intended ABI3 artifact per
      platform, and those four exact artifacts install with the staged
      MolSysMT/MolSysViewer pair in all 16 Python 3.11--3.14 runtime cells when
      3.14 is claimed. Retain the full-matrix run ID and SHA-256 coordinates for
      exact-file promotion.
- [ ] Docs build → green, course toctree warning-clean.
- [ ] No open **blocker** in `pending_bugs/`; open items are accepted debt or post-1.0.
- [ ] **Citation metadata prepared for the tag.** `CITATION.cff` carries the stable
      concept DOI, intended version and release date; `.zenodo.json` agrees on shared
      metadata; and `validate_citation.py --expected-version <tag>` passes. See
      [`release_and_citation.md`](release_and_citation.md).

Only then tag the release.

After publishing the GitHub Release, F6 is complete only when Zenodo has archived the
tag and the shared verifier reports `verified`, with a distinct version DOI
inside the declared concept family and exact source file evidence. A green probe
with `ingestion_pending` does not complete F6. The DOI of a not-yet-published version
cannot be a pre-tag gate unless it was deliberately pre-reserved through the Zenodo API.

## Notes

- This gate is a checklist plus one runnable aggregator; it does not replace human review
  of `pending_bugs/` severity or the accepted-debt ledger.
- The fast-gate list is intentionally explicit in `release_gate.py` (not globbed): adding
  a gate is a deliberate act, and every gate here is expected to stay at zero debt.
