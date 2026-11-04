---
summary: Reference bond helpers do not consistently validate atom-index maps.
issue: uibcdf/molsysmt#554
status: open
opened: 2026-11-04
closed:
severity: medium
verification: reproduced
area: [argdigest, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reference bond input-map validation

## What and how

On source 93d29bf23e2c54f238f7ada984a4b23420b4b3b0, saccharide,
small-molecule, terminal-capping and water reference bond helpers accept an
atom_indices list of strings and return string endpoints. A six-family probe
also finds that extra explicit indices are ignored while short maps fail with
incidental KeyError/IndexError. Those inputs violate the intended parallel
integer mapping contract; this is not evidence that stored bond tables are
chemically wrong.

```python
import molsysmt as msm
msm.element.group.saccharide.get_bonded_atom_pairs(
    'NAG', ['C1', 'C2', 'C3'], atom_indices=['a', 'b', 'c'])
# [['a', 'b'], ['b', 'c']]
msm.element.group.water.get_bonded_atom_pairs(
    ['O', 'H1', 'H2'], atom_indices=[100, 10, 20, 999])
# [[100, 10], [100, 20]]; the extra index is ignored
```

## Why

The documentation-only correction #548 defines successful outputs and supported
input preconditions. It does not enforce every malformed map. #550 fixes flat
atom-name containers, not this separate argument. Native consumers and PR #543
must not create their own string-to-index coercion or silently guess alignment.
The related consumer is uibcdf/molsysviewer#264.

## Scope and acceptance

Use ArgDigest at the public native boundary and existing SMonitor catalog errors
to enforce a flat integer map aligned to the supplied names. Decide scalar
single-atom compatibility, booleans, negative and duplicate indices, empty input
and readonly/strided arrays explicitly before implementation. Preserve valid
mapping outputs, family ordering, reference data, caller ownership and the
unknown/None/empty/error distinctions for valid queries. Add rejection guards
before reference-database access and verify diagnostic fields as well as type.
Coordinate any public signature or skip_digestion change with the addon.

No optional engine is needed for these bundled reference lookups; DepDigest
remains responsible for actual optional-engine boundaries. No new dependency,
Rust kernel, competing chemical store or scientific method is proposed here.

## Provenance

2026-11-04, Linux x86_64, shared Python 3.14.7, NumPy 2.4.6. The first bounded
48-call six-family probe ran from the root checkout; the four-family string-map
probe independently ran from the isolated #548 worktree at the same source.
Their raw records are under `.pytest_cache/template-bond-contracts-548-550/`.
No runtime fix or complete input-enforcement qualification is claimed.
