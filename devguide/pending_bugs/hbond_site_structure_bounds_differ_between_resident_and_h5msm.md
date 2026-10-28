---
summary: Hydrogen-bond site structure bounds differ between resident and H5MSM.
issue: uibcdf/molsysmt#509
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [interactions, selection, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Hydrogen-bond site structure bounds differ between resident and H5MSM.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** open; native correction pending.

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
