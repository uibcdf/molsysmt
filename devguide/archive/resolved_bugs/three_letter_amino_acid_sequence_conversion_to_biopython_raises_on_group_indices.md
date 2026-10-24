---
summary: Three-letter amino-acid sequence conversion to Biopython raises on group_indices
issue: uibcdf/molsysmt#443
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/string_amino_acids_3/test_biopython_codec.py
normative: docs/content/user/foundations/support/forms/strings.md
blocked_by: []
supersedes: []
---

# Three-letter sequence conversion raises before producing Biopython output

**Reported:** 2026-10-24 during the uibcdf/molsysmt#439 source-group-map tests.
**Initial status:** open. The separate codec route remains unchanged by #439.

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


## Resolution and qualification — 2026-10-24

The new codec guard initially fails 38 of 40 cases on the original provider.
The corrected sequence selection and conversion paths pass their focused guards
and the existing offline string/alignment/source-group tests. The final combined
686-case regression and documentation/source checks are recorded once in the
[family qualification](minimum_distances_reuses_first_population_weights.md#resolution-and-qualification--2026-10-24).
The unrelated marked AlphaFold network alignment is explicitly outside this
qualification. No new installed artifact or publication is authorized.

### Sequence ownership and preserved axes

Native recognition, extraction and one/three-letter translation remain independent
of Biopython. A subprocess denies every Bio import and still completes both
native public conversions. Seq/SeqRecord are explicitly requested optional
outputs, enforced lazily through DepDigest. Their three-letter route now calls
the actual three-to-one interpreter, not a one-letter identity converter.

Shared private string selection validates the original group axis before caps
are omitted. One-letter extraction gains only the keyword-only group_indices
alias already passed by its converter; no old positional argument changes.
Its function-scoped signature waiver names this defect and its numerical/textual
guard. The helper preserves requested order/repeats, rejects invalid/conflicting
axes and unsupported structures, and keeps typed empty string targets. Prefix
markers are stripped before constructing Bio objects. Sequence alignment still
requires nonempty selections and retains original source-group maps. The public
IUPAC code lookup remains the chemical interpretation owner; no new mapping or
scientific method is invented here.
