---
summary: SMARTS readers reject external syntax for the default reference state.
issue: uibcdf/molsysmt#488
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, topology, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# SMARTS readers reject external syntax for the default reference state

**Reported:** 2026-10-26 during expert addon feature-reader receiving.
**Status:** open; independent follow-up to resolved #482.

Follow-up to #482 for an omitted consumer of the same default-reference normalization: `topology.get_substructure_matches`, and therefore `physchem.get_hydrophobic_sites` and `physchem.get_halogen_bond_sites`, still reject valid MDTraj syntax on `8346db49566bc09f771db5d927342ab7d4f95a69`. The repaired aromatic/ring routes retain their earlier qualification.

## What and how

```python
import molsysmt as msm
from rdkit import Chem
from rdkit.Chem import rdDepictor

molecule = Chem.MolFromSmiles('CCC.CCl.C=O')
rdDepictor.Compute2DCoords(molecule)
builder = msm.MolSysBuilder(msm.convert(molecule))
group = builder.add_group(list(range(builder.n_atoms)), group_name='LIG')
builder.add_chain([group], chain_id='A')
molsys = builder.build()
indices = msm.select(molsys, 'all and all', syntax='MDTraj')
assert indices == list(range(7))
for reader in [msm.physchem.get_hydrophobic_sites,
               msm.physchem.get_halogen_bond_sites]:
    reader(molsys, selection=indices)  # succeeds
    reader(molsys, selection='all and all', syntax='MDTraj')  # ArgumentError: syntax
msm.topology.get_substructure_matches(
    molsys, patterns='[#6]', selection='all and all', syntax='MDTraj')  # same error
```

The SMARTS reader's custom selection branch passes `chemical_state=state_index` into `basic.select` for nontrivial string selectors, including the user's default reference request. It has not adopted the repaired reference-preserving selection boundary. Native-only reproduction, full declared hierarchy/chemistry; actual imported PyParsing **3.3.2**, MDTraj 1.11.1, RDKit 2025.9.5, Python 3.14.7. Direct selection succeeds; this is separate from the parser failure in #484.

## Why and acceptance criteria

This prevents external-syntax receiving in the expert addon under #421 / uibcdf/molsysviewer#264. No downstream selector translation or chemistry compensation will be added. Please extend the native positive intended-population guards to SMARTS and both feature readers, including default/None reference, empty/subset selections and a nonzero declared reference; preserve explicit/associated-state restrictions, full-graph matching, ordered roles and match limits. Guard the shared native boundary rather than only the consumer facade.

The additional analysis is tracked in `devguide/pending_bugs/smarts_default_reference_external_syntax.md`; the original archived resolution remains historical evidence for the paths it actually repaired.


## What is measured and what is assumed

Direct `msm.select` returns the intended seven atoms. SMARTS, hydrophobic and
halogen readers all reject the same default-reference string and accept the
identical numeric selection. Full traceback reaches the explicit state/syntax
safety check in `basic.select`. The source diagnosis identifies the SMARTS
reader's remaining custom `selection_state = state_index` branch.

## What was refuted

The complete group/chain hierarchy excludes the earlier incomplete-ligand
fixture. The independently successful `all and all` selector and imported
PyParsing 3.3.2 exclude #484's symbolic-comparison regression. No Viewer code
is imported in the reproduction. Earlier aromatic/ring repairs are retained;
this report does not revoke those qualified paths.

## Scope and exclusions

No provider monkeypatch, selector rewrite, automatic preparation or consumer
scientific repair. Explicit and structure-associated state safety remains native.
This is source receiving, not a clean installed or compatibility-range result.

## Provenance

Linux, Python 3.14.7, RDKit 2025.9.5, MDTraj 1.11.1, actual imported PyParsing
3.3.2, fixed source 8346db49566bc09f771db5d927342ab7d4f95a69 with the retained
ABI3 backend. The shared environment contains stale 3.3.3 distribution metadata
alongside 3.3.2; the executed module and Conda record are 3.3.2. No claim of clean
package metadata is made. Raw audit evidence remains local; this record preserves
the complete native-only reproduction and observed outcomes.

The first state transition reopened #482. Its archived resolution and this active
follow-up require different issue identities under the local validator. #482 was
restored to its original resolved scope; #488 owns this remaining custom branch.
