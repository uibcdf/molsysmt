---
summary: mutate misroutes selection syntax and interprets atom masks as group indices.
issue: uibcdf/molsysmt#568
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, selection]
guard: tests/build/mutate/test_mutate_selection_contract.py
normative:
blocked_by: []
supersedes: []
---

# Mutation masks mix syntax and atom/group axes

**Reported:** 2026-11-05 with explicit maintainer authorization, from independent
2026-11-04 reproductions during PR #543 / uibcdf/molsysviewer#264 receiving.
**Status:** resolved by published native 27ccb1b6d; consumer receiving remains a separate scope.

## What

`build.mutate` does not consistently apply its public selection/syntax contract when resolving name/ID-keyed targets. On canonical native AlaValPro, a MolSysMT expression selecting group 1 works, its MDTraj equivalent is parsed as MolSysMT, and the atom-index list returned by `msm.select` is treated as group indices. This is independently reproduced without Viewer.

## How

```python
import molsysmt as msm
molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
args = dict(mutations={"VAL": "GLY"}, keys="group_name")
msm.build.mutate(molsys, selection="group_index==1", **args)
# Positive: ALA, GLY, PRO.
msm.build.mutate(molsys, selection="resid 1", syntax="MDTraj", **args)
# ArgumentError: selection could not be parsed with MolSysMT syntax.
indices = msm.select(molsys, selection="group_index==1")
msm.build.mutate(molsys, selection=indices, **args)
# ArgumentError: mask contains out-of-range group indices 10..25; valid [0, 3).
```

Source native basis `5f3af9374f2bf4ce9c3598450e22d43ca14509ae`, retained in PR #543 source `7bd844fa5e05570c013a8b8fdd59507fbcf48bbb`; Python 3.14.7. `mutate.py` SHA-256 `0a85b50a079604a5f2a3d18972ce2d989aaf05c4b574583575833e62df389ebc` matches the current owner checkout. The function calls `get(element="group", mask=selection)` without forwarding syntax or first resolving the public atom selection. This identifies a normalization boundary for owner review; no consumer translation is proposed.

## Why

Please define and normalize the public selection/mask axis consistently for every mutation specification and both engines. Preserve source indices, explicit source-name validation, group IDs as labels, original source independence and bounded reconstruction warnings. Audit index/ID/name keys and string specifications, including whether selection restricts index-keyed requests. Add native pytest coverage for equivalent MolSysMT/MDTraj/numeric masks, partial/empty masks, repeated/out-of-range indices, disjoint requests, duplicate group IDs and pre-write rejection. Compare selected targets and retained atoms independently rather than only comparing output shapes. Do not add implicit preparation or a fallback parser.

Consumer: MolSysMT#421 and uibcdf/molsysviewer#264, expert `view.addons.molsysmt.build.mutate` receiving. Successful canonical/native-expression routes can be received separately while unsupported masks preserve the native diagnostic.

## What is measured and what remains unverified

The canonical positive and both ArgumentError paths were executed directly in
MolSysMT, without Viewer or a digestion bypass. The reproduction covers the
MolSysMT engine and name-keyed targets. Similar ID/string and PDBFixer branches
are source-inspected; the owner must qualify their complete behavior. No wrong
numerical result or source corruption is demonstrated by these two failures.
The public numeric selection axis and index-keyed masking behavior need an
explicit owner contract; do not invent group/atom conversion in the consumer.

## What was refuted

This is not a Viewer request-emission error: direct native calls reproduce it.
It is not caused by missing molecular groups: the canonical source has three
explicit groups and the positive expression succeeds. It is not the group-free
MDTraj adapter defect #495. The native mutate.py file digest matched between
the contribution and owner checkout when reproduced.

## Acceptance criteria

Resolve the public selection/syntax/axis contract before changing the normalizer.
Native pytest must exercise index/ID/name keys and mutation strings, both engines
where available, equivalent supported expression/numeric selections, complete,
partial, empty, repeated, disjoint and out-of-range masks, duplicate group IDs
and pre-write failure. Assert actual target identities and retained atoms/geometry
independently. Preserve source independence, naming validation, warnings and
provider prerequisites. Select an addressable native pytest guard at closure;
consumer rejection-parity tests are not a native correctness guard.

## Scope and exclusions

This report concerns selection-mask normalization, not a new reconstruction
engine, selector translation, implicit preparation or naming-profile correction.
The separate naming contract stays under #549. The addon receives canonical
success and unsupported-mask diagnostics separately, with no scientific repair.

## Provenance

Observed on Linux, Python 3.14.7, Pandas 2.3.3 and NumPy 2.4.6, native basis
5f3af9374 and PR source 7bd844fa5. Sanitized reproduction and tracebacks are
retained in Viewer `.pytest_cache/mutate-selection-native-20261104.json`; review
resources by 2026-11-11. The owner handoff records its SHA-256. Existing consumer
coverage is in `tests/molsysviewer_molsysmt/test_build_sequence_tools.py`, with
its original source/JUnit receipt retained; no native fix or new science run
is claimed by filing this issue.


## Resolution — 2026-11-05

The native owner resolved #568 in 27ccb1b6d640b7e2087a86dea06f6e666dc73fe1.
The addressable native guard tests/build/mutate/test_mutate_selection_contract.py
protects atom-axis selection across specifications, masks/syntaxes and engines,
pre-write target validation and independent no-op behavior. This original
consumer evidence is archived separately from the owner's resolution report;
its original reproductions retain their earlier source. The addon receives
the public native skip flag and repaired selection contract without a scientific
workaround. Installed qualification and full reconstruction coverage are separate.
