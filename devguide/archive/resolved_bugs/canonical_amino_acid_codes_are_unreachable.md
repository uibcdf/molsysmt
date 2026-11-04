---
summary: Canonical amino-acid code lookup cannot reach XLE and XAA.
issue: uibcdf/molsysmt#545
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [attribute, topology]
guard: tests/element/group/amino_acid/test_codes.py
normative:
blocked_by: []
supersedes: []
---

# Canonical ambiguity code lookup

## What and how

On main be2f3fb7cb6ac0e52170669edea165166899ad3c, `get_1_letter_code_from_name`
raises KeyError for both XLE and XAA despite their declared J/X entries in the
canonical code table. It first indexes the separate variant mapping, which has
neither name. Both failures reproduce in the initial canonical-table guard.

Resolve canonical names directly through the existing shared code authority,
then use the unchanged variant mapping for other labels. Do not add a competing
mapping, modify the imported variant catalogue or normalize case implicitly.

## Why and evidence

The public one-letter alphabet must be reachable. The primary
[DDBJ code table](https://www.ddbj.nig.ac.jp/ddbj/code-e.html) includes XLE/J
for leucine/isoleucine ambiguity and XAA/X for unknown identity. These are
sequence symbols, not new atomic builder templates or a choice of chemical state.

The initial all-variant parameter sweep was a compatibility check, not scientific
validation of every imported catalogue assignment. Final durable tests use the
canonical reachability invariant plus explicit representative modified,
protonation, unknown and case-sensitive examples. A separate before/after
catalogue-output snapshot checks preservation of all existing variant results.

## Scope and acceptance

All 26 declared canonical symbols must resolve, including SEC/PYL and all four
ambiguity symbols. Existing variants and explicit errors must remain unchanged.
Update help, tutorial/course and relevant sequence conversion tests. Generic
amino-acid classification, variant catalogues and atomic construction are unchanged.

## What was refuted

The failure is not limited to XLE: XAA has the same missing variant-route entry.
Adding just XLE to an unrelated variant table would leave canonical availability
dependent on duplicated declarations.

## Provenance

Local Linux/Python 3.14.7 and review basis be2f3fb7c. The shared initial run recorded
in #547's report has two canonical-code failures. Final receiving passes; see below.

## Completed receiving — 2026-11-03

All 26 canonical entries resolve. Literal assertions independently protect J/X/U/O,
representative variants keep their expected letters and case-sensitive failures
remain explicit. All **817** pre-existing variant outputs match a captured prior
snapshot; the variant table itself is unchanged. This is compatibility evidence,
not scientific certification of every legacy interpretation. An initial test
selection assumed HID and GLH/E under a force-field dialect, failing two newly
authored expectations; that separate mismatch is now #549. These expectations
are not replaced with claims that GLH/Q is scientifically correct.

The final shared focal selection passes **77 cases**, no warnings; the broader
source selection passes **430**, and final documentation/doctests **570**, with
zero failures/omissions. Exact commands, warnings, original failures and the
later focal-assertion scope are recorded in the
[cap receiving record](terminal_cap_end_labels_are_inverted.md) and the
[shared receipt](../../../devtools/data/group_label_receiving_545_547_20261103.json).
All 14 fast gates and applicable style/docstring checks pass. Public signatures,
case policy, variant catalogue and chemical preparation behavior are preserved.
