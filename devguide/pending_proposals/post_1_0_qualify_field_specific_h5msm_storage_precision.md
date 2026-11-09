---
summary: 'Post-1.0: qualify field-specific H5MSM storage precision'
issue: uibcdf/molsysmt#664
status: open
opened: 2026-11-09
closed:
verification: inspected
area: [form, performance, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualifying storage precision by field

**Status:** Post-1.0 capability study, not a new initial-release blocker.

## What

Evaluate smaller storage encodings for explicitly selected H5MSM fields with
physical numerical-error budgets and explicit fidelity/binding behavior. No API
name, new dtype, schema version or automatic casting is selected by this proposal.

## How

Start from the fixed modular contract clarified by #663: structural floating
series use float64, while typed domain payloads retain their declared encodings.
Compare justified alternatives on synthetic and representative data. Measure
error in declared physical units, large coordinate origins, periodic boxes,
nonconsecutive selected reads, time/energy observables, nullability and mixed
dtypes. Keep original source values, labels, reports, units and producer identity.
Choose an API and compatible root/layer encoding only after reviewing evidence.

## Why

Reducing coordinate storage could benefit large systems, but one global
single/double label cannot describe a mixed typed snapshot. Rounding geometry
can invalidate coordinate-bound observations or replay evidence. Mechanical
assignments, typed report arrays, quantities and indices must not be cast merely
because a geometry-storage policy is selected.

## What is measured and what is assumed

**Inspected:** the modular structural codec currently declares float64 series;
chemistry and mechanics have their own typed payload contracts. #663's executable
controls demonstrate exact sub-float32 geometry and float32 mechanical values
coexisting in the same file. The existing #256 three-case storage study reports
its actual source/dtypes and bounded regular-data limitations.

**Assumed:** some real workloads may obtain useful storage or I/O gains at an
acceptable field-specific error budget. No such gain or generally safe error
threshold is measured or accepted by this proposal.

## What was refuted

Silently accepting a legacy global precision label does not implement a storage
policy. Casting every numeric payload can truncate indices or change scientific
and provenance values unrelated to geometry. Successful storage alone does not
revalidate evidence bound to the original coordinates.

## Scope and exclusions

Post-1.0 provider-owned storage/fidelity work. Preserve the ordinary no-override
route. Keep original scientific producers; affected evidence must be explicitly
retained as stale, invalidated or refused under an agreed contract, never rebound
or recalculated implicitly. No speculative API, current default change, runtime
implementation, stable-schema claim, package or release is introduced here.

## Acceptance criteria

- Review scientific field-specific error budgets in physical units, including
  nondefault unit policies, large origins and periodic boxes.
- Specify source preservation, fidelity/loss reports, strict refusal and the
  treatment of coordinate-bound observations, assignments and their histories.
- Retain nullable/typed chemistry and mechanics, units, indices, mappings and
  original evidence independently of a geometry policy.
- Measure real and synthetic disk size, process RSS, write/read/query time and
  actual numerical errors; distinguish resident and scoped reads and cache state.
- Qualify explicitly supported old readers, root/layer versions, backends and
  platforms. Refuse unsupported combinations before publishing output.

## Dependencies and risks

The #256 whole-format/default freeze and #334 release gates retain their own
acceptance. This proposal does not block them or infer a storage-precision API
from the #663 correctness repair. Any future schema/API changes require their
normal compatibility, documentation and consumer review.
