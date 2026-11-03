---
summary: Hydrogen-bond site structure bounds differ between resident and H5MSM.
issue: uibcdf/molsysmt#509
status: resolved
opened: 2026-10-27
closed: 2026-11-03
severity: medium
verification: reproduced
area: [interactions, selection, molsysviewer]
guard: tests/interactions/hbonds/test_site_structure_scope.py
normative:
blocked_by: []
supersedes: []
---

# Hydrogen-bond site structure bounds differ between resident and H5MSM.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** resolved with native source-form/state/selection guards and bound-addon
receiving. Full-matrix, installed-package and release qualification remain separate.

## What

`interactions.hbonds.get_hbond_sites()` validates explicit source structure indices differently across equivalent forms. For a one-structure native resident MolSys, reference-state recognition accepts [-1] and [1]; the H5MSM 0.5 copy of the same system rejects both. Direction characterization already validates these indices explicitly.

## How

Independently reproduced without Viewer, basis 40a8ac2ea4042f807c7897459183b5533126781d, Python 3.14:

```python
from pathlib import Path
import tempfile
import molsysmt as msm
from rdkit import Chem
molecule=Chem.MolFromSmiles('C#N');conformer=Chem.Conformer(2)
conformer.SetAtomPosition(0,(0,0,0));conformer.SetAtomPosition(1,(1,0,0));molecule.AddConformer(conformer)
molsys=msm.convert(molecule)
with tempfile.TemporaryDirectory() as d:
 path=str(Path(d)/'sites.h5msm');msm.convert(molsys,to_form=path)
 for label,source in [('resident',molsys),('h5msm',path)]:
  for frames in [[-1],[1]]:
   try:
    result=msm.interactions.hbonds.get_hbond_sites(source,structure_indices=frames)
    print(label,frames,'accepted',result['acceptor_atom_indices'].tolist())
   except Exception as e:print(label,frames,type(e).__name__,str(e).splitlines()[0])
```

Observed: resident queries accept both and report acceptor [1]; H5MSM queries raise ArgumentError naming structure_indices. Resident reference chemistry bypasses frame validation in chemical_graph_context, whereas the modular H5MSM route validates against stored dimensions. Selection is nonspatial and the chemistry is otherwise unchanged.

## Why

The public structure/state scope should be consistent for equivalent source forms. Please define and implement explicit bounds behavior for coordinate-bearing resident systems, preserving genuine coordinate-free site recognition and any documented no-structure exceptions. Reuse the owner's general validated-frame tools where applicable; the consumer must not introduce a second policy.

Add native pytest covering MolSys and H5MSM equivalence, valid nonconsecutive/repeated axes, negative/out-of-range/malformed requests, reference/explicit/structure-assigned states, all/None/empty requests, spatial selections and coordinate-free sources. Preserve source chemistry, ordinary recognition and full-source-before-filtering semantics. This is related in mechanism to the earlier ring-reader bounds report #481/#483 but a different public reader, not a request to reopen a completed ring fix.

Consumer: uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. No range rejection or scientific workaround has been added to the addon. Record: devguide/pending_bugs/hbond_site_structure_bounds_differ_between_resident_and_h5msm.md, to land with receiving. Closure requires an addressable native pytest guard and documented coordinate-free behavior.

## What is measured and what is assumed

The standalone native reproducer runs without Viewer. The provider source basis
is 40a8ac2ea; its scientific implementation matches the earlier 667f03b9a basis.
These are contract/shape/form observations, not new scientific methods or a
claim of universal input validity.

## What was refuted

This does not require a GUI callback, a molecular edit or consumer selection
translation. Existing reports named above have different failure mechanisms;
no duplicate was found before filing. The positive expert fixtures use supported
chemistry and valid axes; this excluded native limit stays independently visible.

## Scope and exclusions

The native helper and direct expert consumer are in scope. No wrapper graph
algorithm, index cast, result reshaping or frame policy is introduced here.

## Acceptance criteria

Resolve the public semantics and add mechanically addressable native pytest
coverage for the matrix above. Preserve source chemistry and original source
indices. Receive the owner repair separately in the addon before changing its
documented limitation; a source wrapper is not blanket scientific qualification.

## Dependencies and risks

The native scientific owner chooses and implements the contract. Consumer
compensation would hide disagreement across ordinary source forms and calls.

## Current-source reassessment — 2026-11-03

A direct public-API probe on
`3920346fb4126ec28f15f5ea6edc7e944f7b2589` builds a three-structure explicit-water
system and its complete H5MSM 0.5 copy. Reference-state site recognition now
rejects both negative `[-1]` and out-of-range `[3]` requests on both forms,
including all, numeric, ordinary-string and spatial-string atom selections.
The shared source-axis validation introduced during the native-domain work
therefore already addresses the original nonspatial range bypass. No additional
consumer-side validation is needed for that case.

This is not yet sufficient for closure:

- A nonconsecutive/repeated `[2, 0, 2]` request returns the same full-source sites
  for numeric and ordinary-string selections on both forms.
- Nonspatial `structure_indices=None` succeeds on resident MolSys but raises
  TypeError on H5MSM when the graph context compares None against dimensions.
- A valid spatial selection succeeds on the resident source but raises
  NotImplementedFormError on the H5MSM source. The inspected modular chemistry
  helper deliberately omits the structural domain; this loses the coordinates
  needed by a subsequent spatial selector.
- Spatial empty/None requests also need explicit, consistent semantics. The
  probe records errors rather than assuming these must mean all structures or
  an evaluated empty result. Structure-assigned state resolution must preserve
  its requirement for one known state across the requested structures.

The 40-case probe receipt and command are retained in ignored
`.pytest_cache/stabilization-539/probe_509.json` and `probe_509.py`; it is
exploratory receiving, not the final addressable pytest guard. Its full source
connectivity yields oxygen acceptor `[0]` and donor-H pairs `[[0, 1], [0, 2]]`
before atom filtering; a numeric `[0, 1]` selection retains only `[[0, 1]]`.
The current probe does not certify every chemical-state, malformed-index or
coordinate-free case from the acceptance matrix.

Next, add the complete source-form/state/selection regression matrix and repair
normalization and spatial-domain retention in the shared chemical context.
Keep graph-only reads free of coordinate materialization and read only requested
structures when spatial context is needed. Do not patch the Viewer wrapper or
change scientific recognition rules. No runtime change is made by this
reassessment, and #509 stays open.

## Resolution — 2026-11-03

The shared chemical graph context now normalizes None to all and validates the
original source structure axis before resolving any chemical state, including
rich string selections. Its H5MSM chemistry reader retains only the requested
structural rows when rich selection context is requested; numeric/all atom
queries still omit structural reads. Associations and chemical state validity
are checked before loading coordinates. Empty row requests retain int64 shape.
No selected-atom conversion truncates the full source covalent graph.

The common structure-index digester rejects booleans before integer coercion;
this also protects basic get/select/convert. The ordinary spatial selector
reports missing coordinates through MolSysMT's ArgumentError instead of passing
None into a quantity backend. Missing structures for assigned-state chemistry
raise StructuralInconsistencyError. Empty structure scopes remain valid for
reference/explicit chemical inventories, but cannot evaluate a spatial selection
or resolve an assigned state. Existing spatial semantics use the first requested
structure, without a new union or temporal rule.

The corrected baseline matrix has **53 failing / 196 passing cases** before the
repair. Final combined receiving passes **1,279 tests**, zero skips/failures,
exit 0, 111.30 seconds, using two workers. It includes the expanded 256-case site
scope matrix, 15 general boolean-index controls, other hydrogen-site/direction
and chemistry readers, native selection/digestion, H5MSM association/structure
readers and real bound-addon receiving. Nine new addon cases preserve scene and
named-analysis identity while checking native results and error classes.
The scope guards include nonconsecutive/repeated indices, scalar/all/None/empty,
malformed/bool/negative/out-of-range requests, distinct reference/explicit/
structure-assigned chemistry, unknown associations, coordinate-free sources,
nondefault angstrom policy and source-table/coordinate/reference preservation.
A negative structural-reader sentinel protects graph-only reads; an observed
reader verifies the exact requested row list. Ambiguous states reject before
any structural read.

The 16 disclosed warnings are 12 deliberate legacy-H5MSM warnings and four
memory-pressure controls from the existing bounded-execution tests; the latter
exercise a deliberately tiny configured budget, not a new memory measurement.
Documentation/doctest receiving passes **518 cases**, zero skips/failures,
exit 0, 11.92 seconds, with 142 existing Sphinx deprecation warnings. All 246
public docstrings and 14 fast gates pass. Full-tree Ruff, dependency/import,
API/signature and devguide checks pass. The new native guards are added to both
aligned routine smoke commands; the existing addon module is already selected.

Linux source receiving uses the existing Python 3.14.7 development environment
and Viewer ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. Raw logs and JUnit receipts
are retained in ignored `.pytest_cache/stabilization-509/`. Foundations, Toolbox,
Cookbook, addon guidance and all four advanced-HBonds course modules reflect the
contract. Six notebook edits preserve code cells, stored outputs, cell identity
and notebook metadata. No new detector, scientific profile, chemical inference,
public signature, dependency floor, schema or format version is introduced.
These local receiving counts do not certify a hosted full matrix or installed pair.
