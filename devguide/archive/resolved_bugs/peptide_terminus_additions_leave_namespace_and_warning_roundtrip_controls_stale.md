---
summary: Peptide-terminus additions leave namespace and warning-roundtrip controls stale.
issue: uibcdf/molsysmt#704
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: reproduced
area: [tests, api]
guard: tests/_private/smonitor/test_xdist_warning_reconstruction.py
normative:
blocked_by: []
supersedes: []
---

# Peptide-terminus additions leave namespace and warning-roundtrip controls stale

## What / How / Why

The frozen 5f241cfa7 default suite has three peptide-terminus coverage failures:
the exact chemical_states namespace omits the supported get_peptide_termini
export, and the warning round-trip inventory lacks sample fields for the new
UnassessedPeptideBackboneWarning. The behavioral code is already present;
these controls correctly report incomplete maintenance.

Add the intended public function to the exact canonical namespace oracle and
supply chain_index/reason values with a recognizable rendered fragment. Keep
full export-set equality, absence of a Topology facade, discovery of all warning
classes, and exact xdist reconstruction/pickle/deepcopy assertions. No warning
class may be excluded, no default-only sample substituted, and no public
function or diagnostic behavior changes are needed.

Receive both complete test modules and the related peptide-endpoint and build
assessment guards. Preserve the three original failures in the complete-session
receipt. This test-maintenance issue is distinct from hosted smoke inventory
#701; the latter is supplied by incoming PR #702.

## Resolution — 2026-11-10

Source **93b3a6ea6** and canonical Rust 1.97.1 release backend
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`
pass **133 directed cases**, **1,782 affected cases**, all **88 Rust tests**,
required library Clippy and **116 registered scientific cases / 74 nodes**.
Selections overlap and are not summed. Numerical outputs, original budgets,
refusal behavior, cutoff/MIC/order and complete warning/export assertions are
retained. No owned OOM or host-reserve stop occurs.

The [receiving record](../../../devtools/data/numeric_neighbor_budget_receiving_703_704_20261110.json)
retains the original complete default session: **33,519 pass, five failures and
two skips**. Its numerical-budget failures belong to #703; its three incomplete
peptide-control failures belong to #704. Targeted receiving corrects those
mechanisms; it does not turn that session green or replace a new full suite,
installed/platform or candidate qualification. The exact namespace remains
protected by `tests/chemical_states/test_namespace.py`; every catalog warning
remains protected by `tests/_private/smonitor/test_xdist_warning_reconstruction.py`.
No original plan credit, public scientific method or release authority changes.
