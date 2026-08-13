---
summary: The reported boundary-digestion cost is absent from the measured viewer workflow.
issue: uibcdf/molsysmt#147
status: withdrawn
opened: 2026-08-12
closed: 2026-08-13
severity: high
verification: measured
area: [digestion, form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Withdrawn diagnosis: internal predicates carry boundary-grade digestion

**Withdrawal decision — 2026-08-13:** a new instrumented run distinguished ordinary
digestion from ArgDigest's `skip_digestion=True` fast path. All 510 form-level
`has_attribute` calls in the reported MolSysViewer workflow already use the fast path;
none performs molecular-system assessment. Forcing the same bypass produces no timing
improvement. The original causal diagnosis and its estimated 29 ms cost are therefore
refuted, not fixed.

The two real findings have independent owners and records:

- uibcdf/molsysviewer#32 proposes reusing one attribute inventory within a scene-summary
  synchronization; a controlled operation-local cache reduced the measured median from
  46.71 ms to 26.62 ms;
- uibcdf/molsysmt#154 proposes simplifying the smaller public-boundary path, where one
  direct `msm.has_attribute()` call currently performs four assessments.

The original report is retained below as historical evidence of the hypothesis that was
tested. It must not be cited as an active defect or as evidence that the viewer performs
boundary-grade digestion in its attribute loop.

## Withdrawal audit

The instrumentation wrapped every decorated callable before importing MolSysViewer and
classified calls by the actual `skip_digestion` keyword. On
`demo['dialanine'].regions.add(selection='atom_index < 3')`:

| observation | measured current value |
| --- | ---: |
| decorated calls | 589 |
| ordinary digestion | 21 |
| fast-path calls | 568 |
| form-level `has_attribute` calls | 510 |
| form-level `has_attribute` calls with ordinary digestion | **0** |
| molecular-system assessments in the workflow | **0** |
| distinct `(form, attribute)` pairs | 229 |

The 510 calls are 256 `molsysmt_MolSys`, 178 `molsysmt_Topology`, 40
`molsysmt_Structures`, and 36 `molsysmt_MolecularMechanics` calls. The original total of
434 omitted the last family.

An alternating 50-operation timing probe measured medians of 46.71 ms for the unchanged
workflow and 26.62 ms with operation-local attribute-query reuse. In contrast, forcing
`skip_digestion=True` at every form-level predicate measured 46.62 ms versus 46.82 ms
for the unchanged workflow, which is no improvement within the observed dispersion.

## Original report — 2026-08-12

**Severity:** high — it is the dominant cost of at least one common user-facing
operation, and it is paid on every call.
**Locations:** `molsysmt/form/*/has_attribute.py`, `molsysmt/_private/argdigest/argument/molecular_system.py`
**Found from:** MolSysViewer, while attributing a reported 24.9% ArgDigest slowdown.

## Symptom

One `view.regions.add(selection="atom_index < 3")` on the `dialanine` demo dispatches
**587 decorated calls** across 43 distinct callables. 434 of them are `has_attribute`:

```
 256x  molsysmt.form.molsysmt_MolSys.has_attribute
 178x  molsysmt.form.molsysmt_Topology.has_attribute
  40x  molsysmt.form.molsysmt_Structures.has_attribute
```

Each one pays full argument digestion:

| `molsysmt_MolSys.has_attribute` | µs per call |
| --- | ---: |
| digested | 65.6 |
| `skip_digestion=True` | 7.5 |
| **digestion overhead** | **58.1** |

The body of `has_attribute` is a dict lookup and a couple of branches. It wears a
boundary-grade digestion machine roughly nine times its own weight, 434 times, for one
user action — on the order of **29 ms** of avoidable work.

## Cause

`digest_molecular_system` calls `assess_molecular_system` and
`validate_molecular_system_argument` — real form assessment. It runs **434 times on the
same `MolSys` object**, which does not change between calls.

The placement is the defect, not the cost of validating. `molsysmt_MolSys.has_attribute`
is not an API boundary: it is MolSysMT calling itself, with an argument MolSysMT
constructed. ArgDigest's own guidance puts digestion at boundaries.

## Reproduction

```python
from molsysviewer.demo import demo
from molsysmt.form import molsysmt_MolSys
import timeit

view = demo["dialanine"]; view.widget.send = lambda _m: None
sys_ = view._molsys
f = molsysmt_MolSys.has_attribute
g = dict(f=f, sys_=sys_)

print(timeit.timeit("f(sys_, 'n_atoms')", globals=g, number=5000) / 5000 * 1e6)
print(timeit.timeit("f(sys_, 'n_atoms', skip_digestion=True)", globals=g, number=5000) / 5000 * 1e6)
```

Counting the fan-out requires wrapping `argdigest.arg_digest` with a counter before
importing `molsysviewer`; the script used is recorded in the MolSysViewer note referenced
below.

## A second, independent finding in the same sweep

434 calls resolve to only **191 distinct `(form, attribute)` pairs** — a redundancy of
2.3x. Memoising within one operation removes that part. The remaining 191 distinct
attribute queries to answer "add a region" is an algorithmic question this report does
not settle, but even at the undigested 7.5 µs they are ~3.3 ms.

## Two smaller defects found in the same layer

**A dead passport branch.** `molsysmt/_private/argdigest/argument/coordinates.py`
contained two branches on `caller.startswith("molsysmt.lib.structure")`, one of
which issued an ArgDigest `ValidatedPayload`. The earlier reference here to
`molecular_system.py` was incorrect. No decorated callable lives under
`molsysmt.lib.*`, so both branches were unreachable. This independent defect is
resolved by uibcdf/molsysmt#153; the placement and repeated-cost problem tracked
here remains open.

**Canonicalization declared twice.** `molsysmt/_private/argdigest/_scientific_arrays.py`
calls `puw.fast_track.to_nanometers` and `np.asarray(..., float64)` by hand, duplicating
what `argdigest.contrib.pyunitwizard_support` provides. Two implementations of the same
unit canonicalization in two repositories is how units drift apart between libraries.
ArgDigest is reworking those pipelines; adopting them and deleting the local copy is the
follow-up.

## Recommended correction

1. Decide the boundary. `has_attribute` on a form is internal; the boundary is
   `molsysmt.basic.*`. Either drop the decoration, or have internal callers pass
   `skip_digestion=True` — measured 8.7x cheaper per call.
2. Memoise the `(form, attribute)` answers for the duration of one operation.
3. Keep the resolved dead-branch removal from uibcdf/molsysmt#153 guarded.
4. Adopt ArgDigest's canonicalization pipelines once reworked; delete `_scientific_arrays.py`.

## Acceptance

A test that fails if the defect returns: assert an upper bound on decorated-call count
for one representative operation. The count is the durable signal — a timing threshold
would be flaky, but "one `regions.add` must not dispatch more than N decorated calls"
fails loudly and for the right reason.

## Note on what this is not

The overhead is real and was correctly measured by MolSysViewer. Its diagnosis —
"validation is expensive, so bypass it in production" — does not follow from it, and a
bypass would have made the number disappear while leaving all three problems above in
place. That proposal was declined on this evidence.
