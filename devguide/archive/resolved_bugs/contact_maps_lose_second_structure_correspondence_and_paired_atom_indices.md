---
summary: Contact maps lose second-structure correspondence and paired atom indices.
issue: uibcdf/molsysmt#446
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, selection, contacts]
guard: tests/structure/test_distance_family_contract.py
normative: docs/content/user/tools/structure/distance_family.md
blocked_by: []
supersedes: []
---

# Contact endpoint and label correspondence

**Reported:** 2026-10-24 in the maintainer-authorized distance-family review.
**Initial status:** Active, alongside uibcdf/molsysmt#444 and uibcdf/molsysmt#445.

## What

Explicit second structure lists can fail with ambiguous NumPy truth values;
an omitted second atom population can cause the cell-list route to ignore its
independent structure axis. Paired output with atom selection expressions can
return characters from those expressions instead of resolved atom indices.
Empty flat selections can be misclassified as grouped centers.

## How

The independent NumPy matrix in `tests/structure/test_distance_family_contract.py`
first reproduces 64 failures and 24 passes in the new contact subset: 54
ambiguous-array errors, six empty-center errors and four paired-label errors.
Sources are synthetic native domains and H5MSM. Coordinates are deliberately
structure-dependent, using primary `[2, 0, 2]` and secondary `[0, 2, 1]` axes.
Both dense CPU and forced cell-list routes are checked against lattice-image
enumeration, rather than against each other. No GPU device was qualified.

## Why

A boolean map is scientifically wrong if its endpoint structures are silently
changed. Contact pairs must carry resolved endpoint indices, not characters or
uninitialized labels. The maintainer explicitly added get_contacts to this
family review after the Viewer-discovered defects.

## Scope and acceptance

Keep inclusive thresholds, paired/Cartesian shapes, independent endpoint frames,
flat/group centers, weights, units, periodic boxes and supported output labels.
Require defined empty outputs and explicit errors for unsupported combinations.
Retire disk intermediates and reject resident boolean output beyond its budget.
Preserve user arrays and configuration. General two-system contacts are not a
new API in this correction; get_contacts has no molecular_system_2 argument.
Actual GPU execution remains outside this CPU qualification.


## Resolution — 2026-10-24

Contacts now retain explicit secondary structure lists, including index zero and
an implicit second atom population. Atom labels come from resolved selections;
directed cross-structure pair lists retain every observed endpoint. Empty maps/
pairs are defined, inclusive thresholds validate, and the resident boolean map
has an output-budget guard. Internally created disk distances are retired.
Coordinate workspace remains resident and actual GPU devices are unqualified.
No second molecular-system argument is introduced.

The [shared family qualification and contract-to-test inventory](minimum_distances_reuses_first_population_weights.md#resolution-and-qualification--2026-10-24)
is the single source for executed commands/scopes, 686 Python tests, public
doctests, Rust checks, documentation execution and coverage limits. These
guards run in the source smoke and matching local tier. Consumer migration and
installed/release qualification remain separate.
