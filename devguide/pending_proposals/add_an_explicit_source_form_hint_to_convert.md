---
summary: Add an explicit source-form hint to convert.
issue: uibcdf/molsysmt#151
status: open
opened: 2026-08-13
closed:
verification: inspected
area: [convert, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Add an Explicit Source-Form Hint to `convert()`

**Reported:** 2026-08-13, after separating a bounded form-detection fix from
the larger expert-interface proposal that originally accompanied it.
**Status:** open and explicitly post-1.0 unless new correctness evidence raises
its priority.

## What

Add an explicit public `from_form=` argument to `molsysmt.convert()` for callers
that know an input representation by construction:

```python
msm.convert(
    pdb_text,
    from_form='string:pdb_text',
    to_form='molsysmt.MolSys',
)
```

`None` preserves automatic detection. A supplied value must identify and
validate one catalogue form; an incorrect declaration must fail without a
silent fallback.

## How

Make `from_form` an explicit argument consumed by `convert()` rather than a
member of its converter `**kwargs`. Canonicalize it through the form catalogue,
ask only that form's `is_form()` predicate to verify compatibility, and skip
the global detection sweep. Design list-input semantics before enabling the
hint for heterogeneous collections.

Keep this independent from `skip_digestion`: a source hint chooses a detector;
it is not permission to trust malformed scientific data.

## Why

Protocol-aware infrastructure can avoid heuristic form detection and private
adapter imports. The motivating MolSysViewer benchmark generated PDB text by
construction and had no public way to convey that fact.

The correctness and memory defect in generic detection is already resolved by
uibcdf/molsysmt#149. Therefore this proposal is an expert API improvement, not
a prerequisite for safe ordinary conversion and not a reason to delay 1.0.

## What is measured and what is assumed

Measured evidence for the original 95,000-atom PDB benchmark and the resolved
bounded detector is retained in
`../archive/resolved_bugs/known_source_form_and_large_string_detection.md`.

Assumption: avoiding all detection work can still benefit trusted integration
protocols. No post-fix end-to-end speedup has yet been measured.

## What was refuted

Treating `skip_digestion=True` as a source-form hint was rejected because
`convert()` still needs to choose an adapter and validation bypass is a
different responsibility. Exposing direct imports from
`molsysmt.form.string_pdb_text` was rejected because form adapters are internal
implementation modules, not a stable integration API.

## Scope and exclusions

This proposal covers one explicit source-form hint and its diagnostics. It does
not add new converters, alter automatic detection, weaken adapter verification,
or define heterogeneous multi-input behavior by accident.

## Acceptance criteria

1. `from_form=None` is behaviorally identical to current autodetection.
2. A valid hint invokes only the declared form detector and converter path.
3. An unknown or incompatible hint raises a catalog-backed public diagnostic.
4. `from_form` is never forwarded accidentally to an adapter.
5. Homogeneous and heterogeneous list-input semantics are explicit and tested.
6. Public docstrings, User Guide, Cookbook where relevant, and the Four Paths
   course satisfy lifecycle integrity in the same change.

## Dependencies and risks

This is a public-signature addition and therefore requires API-registry and
documentation-lifecycle updates. Incorrectly treating the hint as trusted input
could hide representation errors; adapter compatibility confirmation is
mandatory.
