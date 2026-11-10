---
summary: Peptide-terminus additions leave namespace and warning-roundtrip controls stale.
issue: uibcdf/molsysmt#704
status: active
opened: 2026-11-10
closed:
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
