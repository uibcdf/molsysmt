---
summary: Live build tests access PDB downloads during offline selection.
issue: uibcdf/molsysmt#577
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [tests, build]
guard: devtools/tests/test_live_build_test_selection.py
normative:
blocked_by: []
supersedes: []
---

# Classifying live build downloads

## What

Seven missing-group tests and one disulfide test access remote PDB data while
selected by `-m 'not network'`. Missing DNS produces seven setup errors and one
call failure instead of an offline scientific run. Local missing-group controls
must remain in that offline selection.

## How

During #568 receiving, `python -m pytest --receptor=llm -n 4 tests/build
 tests/_private/argdigest tests/documentation/test_mutation_examples.py -m
 'not network'` exits 1 with 1,475 passes, two failures and seven setup errors.
The eighth live-download failure is the disulfide test. The other failure is a
separate old reinsertion expectation after #556 restored CIF occupancy; it is
not attributed to network selection. JUnit: `.pytest_cache/mutate-568-affected.xml`.

The seven cases use module fixtures that download 181L PDB/BCIF. Disulfide
conversion downloads 5XJH and retries four formats. No marker classifies these
items as network-dependent. This extends the classification review from #573;
that resolved conversion-only patch did not cover these build modules.

## Why

The offline scientific gate must not depend on a live service. It must still
exercise the three local missing-group cases and retain all eight live cases in
the online lane, without deleting assertions or substituting reference data.

## Correction and guard

Mark the seven actual fixture consumers individually, and the one-item live
disulfide module. `devtools/tests/test_live_build_test_selection.py` invokes
native pytest collection only, with no fixtures or scientific computations,
then checks exact offline and online node sets. This protects actual selection
behavior rather than matching marker spelling. The outer test uses published
Pytest Receptor. Collect-only checks are not live-provider qualification.

## Provenance and scope

2026-11-05, existing Linux/Python 3.14.7 development environment, NumPy 2.4.6 and
Pandas 2.3.3; Pytest Receptor 1.2.1 published overlay. Main before this fix:
ccff2557f576f004461c96950d36a8b6e465e91f. No runtime/scientific formula, optional
provider, dependency floor or release gate is changed.


## Final receiving

The corrected broader selection exits 0: **1,478 passes**, including the exact
online/offline collection guards and the real occupancy/reinsertion assertion.
The failed first attempt remains in the receipt, with download failures separate
from the stale expectation. Documentation/API-registry receiving has 593 passes;
these overlapping runs are not additive. See
[the receiving receipt](../../../devtools/data/mutation_selection_receiving_568_577_20261105.json)
for commands, identities, counts and limits. Hosted, installed-platform and live
provider qualification remain separate.
