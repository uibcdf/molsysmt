---
summary: Classic hydrogen-bond detectors mishandle precomputed donor shapes.
issue: uibcdf/molsysmt#511
status: resolved
opened: 2026-10-27
closed: 2026-11-03
severity: medium
verification: reproduced
area: [interactions, molsysviewer]
guard: tests/interactions/hbonds/test_precomputed_donors.py
normative:
blocked_by: []
supersedes: []
---

# Classic precomputed-donor shape contract

**Reported:** 2026-10-27 during expert-addon detector receiving.
**Status:** resolved with native, bound-addon and documentation receiving.

## What

`interactions.hbonds.get_buch_hbonds()` and `get_luzard_chandler_hbonds()` cannot consume their supplied `donors` consistently. Documented one-dimensional donor atom indices reach code expecting donor-H pair rows and raise internal errors; two-column donor-H pairs are rejected as a 2D atom mask. Automatic role recognition works on the same source.

## How

Independent native reproduction without Viewer, source basis 050375083518a88bc08d2ed9a31d50c8fb2fa575, Python 3.14:

```python
import molsysmt as msm
import numpy as np
from rdkit import Chem
puw=msm.pyunitwizard
molsys=msm.convert(Chem.AddHs(Chem.MolFromSmiles('O.O')))
molsys.structures.append(coordinates=puw.quantity([[[0,0,0],[.28,0,0],[.1,0,0],[0,.1,0],[.28,.1,0],[.28,0,.1]]], 'nm'))
for name in ['get_buch_hbonds','get_luzard_chandler_hbonds']:
 method=getattr(msm.interactions.hbonds,name)
 print(name,'automatic',method(molsys,pbc=False)[0].tolist())
 for donors in [np.array([0],dtype=np.int64),np.array([[0,2]],dtype=np.int64)]:
  try:print(name,'donors',donors.tolist(),method(molsys,donors=donors,acceptors=[1],pbc=False)[0].tolist())
  except Exception as error:print(name,'donors',donors.tolist(),type(error).__name__,str(error).splitlines()[0])
```

Observed:

- Automatic roles: both return `[[[0, 2, 1]]]`.
- Buch, `donors=[0]`: AttributeError, list has no attribute shape.
- Luzard–Chandler, `donors=[0]`: TypeError, list indices must be integers/slices, not tuple.
- Both, `donors=[[0, 2]]`: ArgumentError, mask must be a one-dimensional integer collection.

Both paths filter supplied donors with `basic.select(mask=donors)` and later use two-column donor-H indexing. The current documentation calls donors precomputed atom indices; the automatic helper returns pairs. Precomputed acceptors with automatic donors work independently.

## Why

The expert addon mirrors these explicit scientific inputs and must not flatten pair rows or invent donor-H assignments in a consumer. Please define/document the intended representation and validate it at the native boundary, using the owning chemical/connectivity tools. Preserve actual covalent donor-H membership and source atom indices.

Native pytest should cover both detectors and both donor sides, automatic/precomputed roles, valid and invalid 1D/2D input under the chosen contract, empty/noncontiguous/read-only arrays, selection and nonconsecutive structures, unchanged caller arrays/source, equivalent observed triples and measurements. Unsupported forms should reject explicitly rather than leak internal indexing/container errors. Keep the existing optional sparse-output restrictions distinct; this issue does not require widening that output contract.

This differs from #506 (rule-list mutation), #507 (internal rule syntax), #508 (empty graph paths) and #509 (resident frame bounds). Consumer: uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Record: `devguide/archive/resolved_bugs/classic_hbond_precomputed_donors_have_inconsistent_shapes.md`, to land with receiving. Closure requires an addressable native pytest guard. No native scientific correction or shape workaround was added to the addon.

## What is measured and what is assumed

The standalone native proof at 050375083 uses declared RDKit water chemistry,
indexed hydrogens and deterministic coordinates. Both automatic paths return
one expected donor-H-acceptor observation. Supplied 1D donor indices and 2D
pairs produce the quoted errors. The expert facade is not needed to reproduce
it, and supplied acceptors with automatic donors work separately.

## What was refuted

This is not a missing chemical graph, unsupported result type, empty covalent
path (#508), caller rule mutation (#506) or external rule language (#507).
The optional analysis already deliberately rejects supplied-role/secondary-axis
combinations; that distinct limitation does not explain the default tuple route.

## Scope and exclusions

Both classic public detectors and their primary/secondary donor inputs are in
scope. The modern explicit-site API has a separate validated pair contract.
No facade flattening, donor reconstruction or scientific rule is implemented.

## Acceptance criteria

Define and document the accepted donor representation, add addressable native
pytest guards for the requested matrix and preserve correct covalent donor-H
membership. Keep default automatic results, units, source indices and current
sparse-output restrictions explicit. Invalid representations must not leak
internal container/indexing errors. Receive the owner correction separately.

## Dependencies and risks

The native owner chooses any representation/migration semantics. Changing the
facade alone would fork the chemical/index contract and hide the actual defect.

## Accepted correction — 2026-11-03

The tuple route accepts either integer donor anchors (one dimension, including
one scalar) or explicit `(n, 2)` donor-H pairs. Anchors expand only through
stored covalent paths to indexed H atoms; supplied pairs remain a subset. No
automatic donor rule is rerun for a declaration, no hydrogen is reconstructed,
and no source bond/state is changed. Selection filters the donor anchor, as in
`get_donor_atoms`; the attached H can lie outside it. Validate every pair before
filtering, then deduplicate/sort rows without independently sorting columns.

ArgDigest now rejects malformed shapes, ragged lists, boolean/string/fractional
indices and overflow before coercion. Native resolution checks bounds, heavy/H
roles and stored covalent membership through the existing public
`chemical_states.get_covalent_paths` tool. Both classic detectors share only
private orchestration; no competing bond store or new scientific criterion is
introduced. `donors_2` follows the same contract and reports its own argument
name. Unsupported optional sparse-output combinations remain unsupported.

The initial 86-case regression selection produced 32 failures, reproducing the
list/pair/ragged errors independently of Viewer. A first expanded checkpoint
passes 171 cases, including the classic regressions, external role syntax and
new native/H5MSM/composite/RDKit, two-sided, readonly and unit controls. The
source-immutability assertion compares table values independently of Pandas
subclass identity: native table `.copy()` already returns a plain DataFrame
before any calculation. This correction does not weaken value comparisons.

Docstrings, both classic tutorials, the sparse-query recipe and the four
advanced-hydrogen-bond course modules describe the input contract. Notebook
code, outputs, cell IDs and metadata are preserved; only prose is changed.
Existing Ackredit attribution remains attached to the same executed scientific
methods; validation and covalent-path reuse add no external scientific method.

## Final receiving — 2026-11-03

The final combined selection passes **2,021 tests**, zero failures or skips,
254.79 seconds, two workers: all interaction tests, both bound detector receiving
modules, bound hydrogen-site tools, covalent-path and reference-SMARTS controls,
structure-index types and the hosted-command guard. It includes 114 final
supplied-donor cases and 238 aromatic-reference cases. Numerical 2 MB budget
controls retain seventeen memory-pressure warnings; legacy H5MSM reads retain
fifteen warnings. These are not process-RSS benchmarks or installed qualification.

Final documentation receiving passes **569 tests/doctests**, zero failures or
skips, 77.24 seconds. Its 531 warnings are 514 Sphinx/MyST deprecations, ten
legacy-H5MSM reads, six headless-display notices and one deliberate structural
attribute-drop control. Full-tree Ruff lint/format, public docstrings and all
fourteen fast readiness gates pass. The new native guard is explicitly selected
by hosted smoke. Earlier checkpoint counts overlap; they must not be added as
unique coverage.

Linux source receiving uses the shared Python 3.14.7, NumPy 2.4.6 and Pandas 2.3.3
environment, the unchanged compiled backend, and Viewer source
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. No environment, dependency floor,
scientific threshold, attribution branch, H5MSM schema or publication route
changes. The frozen metadata candidate a24b14f3d is separate and does not contain
these later corrections. Its queued full/Rust gates remain its own evidence.
