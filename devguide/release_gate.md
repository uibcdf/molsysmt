# Release Gate

The single normative checklist for tagging a MolSysMT release (in particular 1.0.0).
It consolidates what was previously scattered across workflow comments and the 1.0
audit. Closes audit risk **R2** in
`archive/release_1_0/release_1_0_independent_gate_audit.md` and supports blocker **B1**.
The current pre-release work order is maintained in
[`release_1_0_execution_plan.md`](pending_proposals/release_1_0_execution_plan.md).
Current completion, active stage, and evidence are recorded in
[`release_1_0_status.md`](release_1_0_status.md).

A release is cut **only** when every gate below is green **on the exact commit being
tagged**. Green gates on an earlier commit or a dirty tree do not count.

## 0. Preconditions (the tree and the commit)

- **Clean working tree.** `git status --porcelain` is empty on the tag commit. A release
  cannot be cut from a tree with uncommitted work (audit blocker B1).
- **The tag commit must actually run CI.** Day-to-day commits use `[skip ci]`; the release
  candidate commit (and the tag) **must not** carry `[skip ci]`, or the smoke/weekly
  workflows are silently skipped and nothing is validated. Trigger CI explicitly if
  needed.
- **Version metadata is consistent** with the intended tag (versioningit derives it from
  the tag; `pyproject.toml` `requires-python` and classifiers already list 3.11–3.13).

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
| Scientific evidence registry | `validate_scientific_evidence.py` |
| No top-level soft-dependency imports | `validate_dependencies.py` |
| Developer-guide integrity | `validate_devguide.py` |
| Four Paths course structure | `validate_course.py` |
| Demo assets / H5MSM fixtures | `validate_demo_assets.py` |
| Resource manifests | `validate_resources.py` |
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

## 2. Heavy gate — the full test matrix (`ci-full.yaml`)

The fast gates do not run the test suite. Before tagging, the **full pytest matrix must
be green on the exact committed candidate**:

- `ci-full.yaml` (manual `workflow_dispatch`): ubuntu-latest + macos-latest ×
  {3.11, 3.12, 3.13} = 6 combinations, `pytest -q` (doctests included via `pytest.ini`).
- Equivalently, a green `ci-weekly.yaml` run pinned to the candidate commit.

Do not substitute a partial or single-platform run. `ci-full.yaml` should be extended to
run `release_gate.py` as an early step so the fast gates are enforced in CI too (today it
runs only `pytest`).

## 3. Documentation build

- `sphinx_docs_to_gh_pages.yaml` builds the docs (`nb_execution_mode = "off"`). The build
  must be warning-clean for the course tree (no "toctree contains reference to nonexistent
  document"); `validate_course.py` guards the structure statically, the build confirms it.

## 4. Sign-off checklist (all must hold on the tag commit)

- [ ] Working tree clean; tag commit does **not** carry `[skip ci]`.
- [ ] `python devtools/scripts/release_gate.py` → all fast gates PASS.
- [ ] `ruff check molsysmt` → clean.
- [ ] `ci-full.yaml` (or candidate-pinned `ci-weekly.yaml`) → green on all 6 combos.
- [ ] Docs build → green, course toctree warning-clean.
- [ ] No open **blocker** in `pending_bugs/`; open items are accepted debt or post-1.0.

Only then tag the release.

## Notes

- This gate is a checklist plus one runnable aggregator; it does not replace human review
  of `pending_bugs/` severity or the accepted-debt ledger.
- The fast-gate list is intentionally explicit in `release_gate.py` (not globbed): adding
  a gate is a deliberate act, and every gate here is expected to stay at zero debt.
