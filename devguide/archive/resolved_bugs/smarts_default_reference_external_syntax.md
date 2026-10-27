---
summary: SMARTS readers reject external syntax for the default reference state.
issue: uibcdf/molsysmt#488
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, topology, selection]
guard: tests/topology/get_substructure_matches/test_reference_selections.py::test_default_reference_external_smarts_population
normative:
blocked_by: []
supersedes: []
---

# SMARTS readers reject external syntax for the default reference state

**Reported:** 2026-10-26 during expert addon feature-reader receiving.
**Status:** resolved; independent follow-up to #482, with shared-boundary regression guards.

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


## Viewer addon receiving — 2026-10-26

A frozen pre-repair source snapshot (5b5aaeeb4 plus the three new expert
wrappers) passed its one 2,812-case applicable regression, preserving the known
native rejection rather than translating selections. The subsequent provider
working repair was copied into the isolated snapshot by file SHA-256, without
changing the main checkout. A targeted follow-up passes 390 cases with zero
failures/errors/skips and 18 legacy H5MSM warnings. It includes 81 consumer
feature-reader cases, native reference-selection cases and existing aromatic/
topology receiving. Positive numeric-versus-MDTraj populations now cover all
three feature readers, default/None reference, a nonzero reference independent
of structure associations, and preserved explicit SMARTS state restrictions.

Executed matching code SHA-256:
`molsysmt/topology/get_substructure_matches.py` =
`8e21c26586cbdfc79675144c0bb3b37d7e851a5e22d2aeb5f44d02038227b0c5`.
The 390-case observation is local working-source receiving, not a committed or
installed-candidate gate. The scientific owner retains the fix and closure;
the addon introduces no selector or state workaround.

## Resolution — 2026-10-26

The remaining SMARTS-specific selection branch now delegates to the existing
`select_chemical_atoms` boundary, preserving whether the original request was
default/None reference. The helper returns sorted, unique int64 source indices.
Explicit integer/structure-associated state requests keep their existing syntax
restrictions; no downstream rewrite or provider patch is introduced. Numeric
selections use the shared read-only chemistry view instead of another deep copy.

Source inspection also traced every other caller: hydrophobic, halogen, metal
and water site readers pass their original request through; internal hydrogen
bond directions, H-bond sites and pi/cation-pi recognition intentionally request
resolved chemistry with the default all-atom selection. Their scientific rules
and state behavior are not modified.

The guard declares intended populations independently: five carbons in the
SMARTS example, the central nonterminal hydrophobic CH2, the ordered donor pair
[3,4] and reversed-index acceptor/reference pair [6,5]. It tests full/empty/subset
and single-atom selections, source-axis retention, typed empties, full-graph
context, unchanged native chemistry and byte-preserving file reads. Matching
limits remain checked on the entire source before selection. Three readers
cover native/complementary/H5MSM inputs and standalone Topology; nonzero reference
indices are checked against conflicting structure associations on all three
structural source forms. Explicit-state and associated-state failures remain
positive safety controls, with numeric alternatives still executable.

## Qualification

The initial 117-case matrix fails before the repair (105 failures, twelve safety
controls pass; 15.57 seconds) and passes afterward (117 passes; 14.22 seconds).
Twelve more nonzero-reference complementary/H5MSM cases extend the final matrix
to 129. The complete scoped topology, four site readers and seven interaction
family regression passes **970 tests in 44.93 seconds**, with twenty expected
legacy-H5MSM and fifteen deliberate memory-pressure warnings. The existing
network-backed sequence-alignment control is excluded from that offline command
and passes separately with network access (one pass, 13.93 seconds).

All three changed public doctests pass (5.34 seconds), and all 492 raw notebook
schema cases pass (9.13 seconds). Selected Ruff check/format, 252 public docstrings,
zero unauthorized signature drift and all fourteen fast release gates pass.
The User Guide tutorials, Foundations, Cookbook and shared/four-path course
clarify reference semantics; nine notebooks change only prose, retaining code,
outputs and metadata. Incremental HTML compilation has zero errors and 51
warnings under existing uibcdf/molsysmt#144 debt.

The matching/budget/filtering/output AST after selection is identical to the
parent, and both feature wrappers retain identical executable AST. This is a
selection-contract repair, not a new scientific method or certification of
chemical/geometric criteria. Commands, source hashes, runtime module versions
and bounds are retained in
[the evidence receipt](../../../devtools/data/smarts_reference_selection_20261026.json).
No full scientific/platform/installed-package-pair or publication qualification
is asserted for this local development checkpoint.
