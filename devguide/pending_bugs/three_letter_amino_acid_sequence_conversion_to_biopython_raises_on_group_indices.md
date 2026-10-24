---
summary: Three-letter amino-acid sequence conversion to Biopython raises on group_indices
issue: uibcdf/molsysmt#443
status: open
opened: 2026-10-24
closed:
severity: medium
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Three-letter sequence conversion raises before producing Biopython output

**Reported:** 2026-10-24 during the uibcdf/molsysmt#439 source-group-map tests.
**Status:** open. The separate codec route remains unchanged by #439.

## What

`msm.convert('AlaGly', to_form='biopython.Seq')` recognizes the input as
`string:amino_acids_3`, then raises `TypeError: extract() got an unexpected
keyword argument 'group_indices'`. No sequence is returned. The intended
one-letter sequence is `AG`, with one letter per amino-acid group.

## How

The three-letter adapter's `to_biopython_Seq` imports
`string_amino_acids_1.to_string_amino_acids_1` instead of the three-letter
conversion. That identity helper delegates to an extractor using the wrong
keyword. Repairing only the unexpected keyword would still bypass the
three-to-one-letter interpretation. Both layers need independent guards.

```python
import molsysmt as msm
msm.convert('AlaGly', to_form='biopython.Seq')
```

**Reproduced:** Linux/Python 3.14.7 development checkout based on bae6d0101,
with unrelated #440/#442/#439 work preserved. The implicated string adapters
are unchanged from that checkpoint. No installed package matrix was run.

## Why

A declared direct conversion edge fails on a minimal supported source.
Callers of the public alignment function can reach the same codec route.
Static edge registration does not prove that it executes; this is relevant
to uibcdf/molsysmt#181's conversion witnesses.

## Acceptance criteria

- Guard direct adapter and public conversion against independent expected
  `Bio.Seq('AG')`, not merely output type or self-round-trip.
- Exercise explicit format prefix, selected source group indices, order and
  repetitions, caps, empty selections and conversion to SeqRecord as applicable.
- Verify that the one-letter identity/extraction route remains correct.
- Preserve declared alphabet, group source correspondence and lazy Biopython.

## Scope

The native source-group projection correction under #439 does not repair this
independent string codec. No extra release gate or format expansion is implied.
