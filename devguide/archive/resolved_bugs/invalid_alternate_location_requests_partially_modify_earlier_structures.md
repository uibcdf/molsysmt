---
summary: Invalid alternate-location requests can leave earlier structures modified
issue: uibcdf/molsysmt#571
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [build, structure]
guard: tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py::test_invalid_later_structure_is_rejected_before_any_publication
normative:
blocked_by: []
supersedes: []
---

# Invalid alternate-location requests can leave earlier structures modified

## What

A valid first structure and missing B in a later structure modify earlier coordinates before raising TypeError. Atom labels remain old and analysis coverage can already be invalidated.

## How

The original writer publishes one structure at a time during selection. Its missing-location branch constructs ArgumentChoiceError without choices.

## Why

A rejected request leaves mixed observations and partial analysis invalidation; downstream code cannot safely retry it.

## Reproduction and acceptance

The new public regression module
`tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py`
reproduces the reports with small native systems. After correcting two fixture
setup errors (the required Interactions method and its read-only mapping), the
original runtime fails 24 of 30 controls. The five existing real-system tests
are retained. The first repaired receiving passed all 35 cases; final receiving is recorded
below.

Related #569/#570 share this bounded repair. No general backend/file transaction is introduced. Public input stays form-agnostic. Preserve alternate records and
unselected observations, selected interaction coverage and physical units.
Prevalidate every selected site and quantity before delegation; invalid requests
must preserve coordinates, labels, occupancy, B factors and analysis identities.
Ordinary mutable backend failures retain their existing conservative coverage
policy; this is not crash-transactional file I/O.

## Provenance

Linux/Python 3.14.7, existing shared development environment, owner source
`d3650cc09735ccfc7bf02d35ca4e0a746f83f96f` plus the bounded local repair.
Pytest Receptor 1.2.1, two workers. Local XML is under
`.pytest_cache/alternate-locations-569-571/`: `reproduced-before.xml` and
`first-repair.xml`. Initial fixture setup errors are not scientific reproductions.
No new native binary, environment or dependency is produced.


## Resolution — 2026-11-05

**Implemented and contract-tested.** Maximum selection uses finite known
occupancies without renormalization. A is preferred only in the documented
half-occupancy tie and only when it shares the maximum within rtol=1e-5,
atol=1e-8. Other ties retain source order. Unknown occupancy is ignored by the
criterion; all-unknown sites require an explicit label. Invalid probability
values are rejected before publication. Explicit selection can retain an
unknown occupancy as NaN.

The complete selected request is staged before writing: location choice,
aligned coordinate/B-factor quantities, occupancy, location-vector order,
selected index bounds, available writers and stable atom-label consistency.
Only then do ordinary mutable form adapters publish the sparse per-structure
updates. Missing later locations raise a proper catalog choice diagnostic
without changing coordinates, IDs, B factors, occupancy, alternate records or
analysis identities. Unexpected backend failures retain the existing adapter's
partial-write/conservative-invalidation policy, not a new general transaction.

Primary occupancy and B factor follow the chosen site, including unknown
measurements. Unselected observations and original alternate dictionaries are
preserved. Numeric IDs become strings and selected structures must agree on the
stable label. Location vectors follow the actual atom-selection order; repeated
atoms cannot choose conflicting labels. Repeated structures are processed once.
Empty selection and no alternate-site work remain no-ops. Successful native
geometry updates invalidate only affected interaction structures; old analysis
objects remain snapshots.

### Reusable observation assignments

Native Structures B-factor/occupancy setters initialize absent metadata through
one private assignment primitive, without reading coordinates. Missing positions
are NaN; integer storage is promoted before fractional assignment. An invalid
first subset does not publish an allocated empty series. Direct native values
now reach their existing ArgDigest B-factor/occupancy validators; the first
storage controls independently exposed the missing native occupancy dispatch.
No skip flag is forced or additional physical-unit parser invented.

The public resolver retains its original arguments/defaults and adds only
keyword-only skip_digestion=False. ArgDigest and SMonitor validate/diagnose at the
boundary; PyUnitWizard converts explicit units to native nm/nm**2. Angstrom input
under a pm/fs application policy is tested. No optional backend or external
scientific method is introduced, so no new DepDigest floor or Ackredit record
is applicable. Metadata planning is not a workload requiring a Rust kernel.
Optional-field creation still uses normal dense structure-by-atom storage; it
is not claimed to be sparse metadata or a whole-system memory benchmark.

### Receiving

Final affected receiving passes **4,639 cases**, without errors, failures or
omissions, in 186 seconds with four workers on Linux/Python 3.14.7. It covers
native objects, basic operations, all private digesters, H5MSM, public interaction
persistence, the resolver and current bound build diagnostics. Its 1,030 warnings
retain 977 legacy notices, fourteen pandas notices and existing structure,
parser/unit/GPU/drop diagnostics, including two observations of the already
tracked environment binary-size warning under #524. No warning is suppressed.

The focused module/native storage tests pass **50 cases**, as does the same
selection with published ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and
Ackredit 0.9.0 payloads. The previously verified floor harness uses only #524's
pytest-entry-point SMonitor plugin exclusion; no runtime assertion is omitted.
Documentation passes **533 controls** and the resolver doctest passes. The
revised tutorial executes eight code cells. Cookbook and four course notebooks
retain all executable cells, outputs and notebook metadata; only their narrative
is extended/corrected. The source manifest and microinstructions are aligned.

The first broader command used a nonexistent tests/basic/set directory and ran
no tests. The corrected wider run exposed two native occupancy-value failures;
it was interrupted at 2,261/4,240 cases to correct that native validator route.
That incomplete run is not receiving evidence. The later 4,639-case run above
uses the final code. A new Markdown cell initially violated the cookbook's older
notebook schema by carrying an ID; its unnecessary ID was removed without
upgrading the original schema or changing executable content. All guards and
negative controls remain intact. Earlier failed XML stays separate from final
receiving where retained; fixture setup errors are not scientific evidence.

The [receiving receipt](../../devtools/data/alternate_location_receiving_569_571_20261105.json)
retains final code/test hashes and local JUnit identities. Whole-tree Ruff,
docstring/signature/API/tier, dependency, devguide/index and diff checks pass.
Native binary and four unrelated human API-stub hashes remain unchanged. These
are source results, not an installed package, full platform matrix or release.


The final native command (in the existing environment with the previously
verified published Receptor overlay) is:

```bash
python -m pytest --receptor=llm -n 4 \
  tests/build/solve_atoms_with_alternate_location tests/native tests/basic \
  tests/form/file_h5msm tests/_private/argdigest \
  tests/interactions/test_public_molsys_h5msm_workflow.py \
  tests/molsysviewer_molsysmt/test_build_diagnostic_tools.py
```

The course-navigation check also exposed a #549 fixture omission: its miniature
Sphinx site copied the real foundation/index and selection labels but omitted
the real new naming-guide label. The fixture now copies that existing source
heading/anchor and asserts rendered naming links. It does not invent a label or
suppress undefined-reference warnings. The corrected course/schema run and its
original failure have separate XML. The course inventory now records the
resolver's Module 12 introduction and its one introductory hint.

The final course/navigation/schema selection passes 498 cases. Its intermediate
link assertion incorrectly treated saved notebook outputs as navigation;
the final guard uses only the Markdown navigation excerpt, requires the two
actual source modules to retain the naming reference, and checks their exact
rendered page/anchor destinations. Missing real targets still fail Sphinx.
