---
summary: Native MolSys shortcuts bypass argument validation
issue: uibcdf/molsysmt#377
status: open
opened: 2026-10-10
closed:
severity: medium
verification: reproduced
area: [api, argdigest, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native MolSys shortcuts bypass argument validation

**Reported:** 2026-10-10, renewed review of deferred issues requested by the
maintainer; source inspection of the separate optimization request #128.
**Status:** Reproduced; admitted to pre-1.0 stabilization, not yet repaired.

## What

`MolSys.get`, `MolSys.info` and `MolSys.to_form` unconditionally delegate with
`skip_digestion=True` without validating/normalizing their own arguments. Their
documented default `skip_digestion=False` does not take effect.

```python
import molsysmt as msm
from molsysmt.native import MolSys
system = MolSys(n_atoms=2)
system.get(output_type='garbage', n_atoms=True)  # None
msm.get(system, output_type='garbage', n_atoms=True)  # ArgumentError
system.get(element='atoms', atom_index=True)  # NotWithThisFormError
msm.get(system, element='atoms', atom_index=True)  # [0, 1]
```

The same element-normalization failure occurs with `element='ATOM'`.
`system.get(skip_digestion='yes', n_atoms=True)` returns 2, while `msm.get`
rejects that nonboolean flag. Invalid `get_missing_bonds='yes'` and
`n_atoms='no'` likewise pass through the native route.

`system.info(skip_digestion='yes')` returns a Styler and
`system.to_form('molsysmt.MolSys', skip_digestion='yes')` returns a MolSys.
Their public `msm.info`/`msm.convert` equivalents raise `ArgumentError`.

## How

In `molsysmt/native/molsys.py`, the three methods have no argument decorator and
replace the caller's flag with True. The downstream decorated operations and
converters therefore receive unvalidated input as trusted. Missing normalization
can be misreported as absent attribute delivery; an invalid output selector can
fall through to a successful `None` return.

Restore one genuine validation boundary using the existing provider contracts.
Forwarding the caller's flag to the decorated delegate is a possible bounded
repair; alternatively validate fully before trusted delegation. Avoid a second
parallel attribute catalog or ad hoc checks for the reproduced examples.
Retain signatures, deliberate boolean trusted delegation and lazy imports.

## Why

These are existing advertised entry points. Both valid heterogeneous input and
invalid arguments behave differently from the public operation being proxied.
This qualifies as a correctness defect under the frozen admission rule. The
performance redesign in #128 remains separate and need not be implemented.

## What is measured and what is assumed

The calls above executed on source
`a54dd36889e90d8cd4c3a04b3a2ce01acc0f004a`, Linux/Python 3.14.7, using a local
two-atom native fixture without external files. No numerical kernel, benchmark,
browser or installed candidate qualification was executed. No mutation/loss of
scientific observations was demonstrated; the failure concerns the public boundary.

## What was refuted

The attribute exists: its canonical public query succeeds. Exposing a
`skip_digestion` parameter alone does not establish that its default is honored.
Forwarding to a decorated function does not validate input when the wrapper
unconditionally disables that decorator's digestion.

## Acceptance criteria

- Default native calls normalize valid element aliases and return independently
  expected atom positions/counts, selections and typed values.
- Reject invalid skip flags, output selectors, attribute booleans, ordinary
  options and unknown attributes at the supported public boundary.
- Exercise info and conversion forwarding, including converter selections and
  explicit trusted calls; preserve source data and existing signatures.
- Add an addressable regression guard, document the validation boundary in
  docstrings/User Guide/course material and run the affected public contracts.

No native dispatch optimization, new query attribute or scientific method is
required. Final candidate qualification remains owned by #334.
