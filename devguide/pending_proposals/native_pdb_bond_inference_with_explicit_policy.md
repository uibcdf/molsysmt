---
summary: Add native PDB bond inference with explicit policy while retaining OpenMM
issue: uibcdf/molsysmt#304
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [form, build]
guard: tests/form/file_pdb/test_connectivity_policy.py
normative:
blocked_by: []
supersedes: []
---

# Explicit PDB connectivity policy

**Reported:** 2026-10-03 by DockingMT; provider triage on 2026-10-05.
**Status:** Direct-file disabled-inference policy corrected and contract-tested;
native inference and explicit engine/failure provenance remain proposed.

## What

Honor explicit PDB connectivity policy consistently through direct-file and
handler conversion, then qualify a selectable native inference route while
retaining OpenMM. Distinguish declared file edges, inferred candidates, absent
engines and failed calculations. Connectivity does not establish bond orders,
protonation, force-field parameters or docking readiness.

## How

### Reproduced direct-file defect

At source `31ec38171f39922a9ae006746c7fd45ce44fc2da`, with OpenMM 8.6.1:

```python
import molsysmt as msm
path = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
direct = msm.convert(path, to_form="molsysmt.MolSys",
                     get_missing_bonds=False)
handler = msm.convert(path, to_form="molsysmt.PDBFileHandler")
try:
    explicit = msm.convert(handler, to_form="molsysmt.MolSys",
                           get_missing_bonds=False)
finally:
    handler.close()
print(msm.get(direct, n_bonds=True), msm.get(explicit, n_bonds=True))
# 1322 13
```

Both direct-file native converters omit `get_missing_bonds` from their signatures.
The generic conversion route therefore discards that option, and the delegated
handler uses its default `True`. The handler already implements disabled inference.
Correct the form boundary and forward the validated option; do not change the
generic conversion policy or the existing reader defaults for unrelated forms.

### Native inference design boundary

Reuse general tools in their owning modules: `build.get_missing_bonds` already
provides native candidates, `element.group` owns residue/component reference
connectivity, `topology` owns graph validation, `structure` and `pbc` own geometry.
Parsing remains in the PDB adapter. A reusable scientific inference contract must
be implemented as a general provider tool and consumed by the reader.

The legacy native operation combines named templates with distance fallback for
unknown groups. Its peptide adjacency/chain defects were corrected in
uibcdf/molsysmt#328; it still does not expose a per-edge method/coverage report or
establish PDB chain-segment and alternate-location constraints. Directly making it a reader
default would admit unqualified covalent inference and obscure unresolved chemistry.

The proposed stages are:

1. Correct explicit-only file/handler parity, including selection and evidence.
2. Design a supported candidate/report boundary over declared source atoms and
   one selected structure, with explicit template, polymer-link, disulfide and
   geometric policies. Incomplete or unsupported groups remain inspectable.
3. Qualify a bounded native-template method independent of OpenMM installation,
   preserving explicit CONECT/LINK/SSBOND edges and rejecting contradictions.
   TER, chain identity, insertion codes and alternate locations constrain links.
4. Expose selectable reader engines only after those methods have executable
   coverage. Retain OpenMM, use narrow lazy dependency guards, distinguish failure
   from absence, and record original method/software evidence.
5. Qualify original Vina inputs and analytical controls with source maps, physical
   units, independent edge inventories and workload measurements.

No new engine selector or implementation is claimed by this design.

## Why

DockingMT's preparation coverage depends on the graph produced by the reader.
Ignoring an explicit disabled-inference option makes reproducibility depend on
whether OpenMM is installed. Its published reference profile now explicitly
includes OpenMM, but the provider still owns consistent policy and native inference.
Related consumer requirements are uibcdf/dockingmt#33 and uibcdf/dockingmt#5.

## What is measured and what is assumed

**Reproduced locally:** the command above returns 1,322 versus 13 bonds in the
same source/env/input. Inspection confirms the identical option omission for
direct-file Topology conversion. No source bytes were changed.

**Consumer-reported, not rerun at this checkpoint:** the original 1IEP PDB has
zero stored edges without OpenMM and 4,469 with it. Existing native candidates
match all 1,309 selected 181L protein edges in the OpenMM comparison; original
1IEP has two native-only and sixteen OpenMM-only edges, and 224 stdout warnings.
The #304 issue links the published raw maps, probe and consumer source. Comparison
with OpenMM is not independent chemical ground truth.

**Assumed:** a bounded template method can cover some reference proteins without
OpenMM. No complete 1IEP coverage, native default, performance improvement or
chemically complete receptor is established.

## What was refuted

- Equal edge counts alone do not establish identical atom pairs.
- A dependency-sensitive default does not justify ignoring a caller's explicit
  request to disable inference.
- Existing native candidate generation is not automatically a qualified PDB
  reader method; universal distance fallback must not declare unknown ligands,
  metals or nearby nonbonded groups covalently connected.
- Inferring connectivity does not assign bond orders or select a chemical state.

## Scope and exclusions

Consistent existing explicit-only policy, an additive native inference method
and inspectable provenance. Do not change OpenMM or reader defaults without a
separate compatibility decision. No automatic template preparation, missing atom
generation, pH search, parameter assignment, docking execution or CCD download.
The preparation contract uibcdf/molsysmt#298 and geometry proposals
uibcdf/molsysmt#327/#323 remain separate.

## Acceptance criteria

- Direct file and handler honor disabled inference for MolSys and Topology,
  preserve literal declared edges/evidence and coordinates/identity, and do not
  import or execute an optional inference engine when disabled.
- Retain existing default behavior and qualify enabled OpenMM comparison with
  the same explicit atom population. Validate options at the public boundary.
- A selected native method has deterministic pairs, original maps, parameters,
  reference/software evidence, unresolved groups and strict coverage boundaries.
- Independent real/synthetic controls cover missing H, naming, modified residues,
  chain breaks, alternate locations, insertion codes, disulfides, ligands, waters,
  metals and contradictory declarations. Source remains unchanged on failure.
- Original 181L/1IEP differences remain explained and retained. Record cold/warm
  timing and memory before making performance claims.
- Public docstrings, User Guide, Cookbook and applicable course lessons reflect
  the implemented policy. Close only after all approved inference scope is covered.

## Provenance

Linux local source review/reproduction on 2026-10-05, Python 3.14.7 with released
ArgDigest 0.13.0 source override, OpenMM 8.6.1, NumPy 2.4.6 and pandas 2.3.3.
Source HEAD is recorded above. No consumer checkout was modified or full source/
installed-artifact qualification claimed. Consumer measurements retain their
original source identities in uibcdf/molsysmt#304.

## Direct-file policy checkpoint — 2026-10-05

**Implemented and contract-tested.** Both direct-file native converters now
accept keyword-only `get_missing_bonds=True` and forward it to the existing
handler. The original positions/defaults, including positional `skip_digestion`,
are retained. The existing argument digester validates the Boolean policy at
the public boundary. No default engine or generic conversion dispatch changes.
Reader-owned handlers close in a finally block after delegated success/failure;
caller-owned handlers remain open.

The finalized initial 12-control selection produced **2 failed, 10 passed in
6.18 s** before the correction. Both failures detected an inference call through
the direct file route despite `False`; handler/text controls passed.
The final focused selection adds import-blocking, invalid arguments, positional
compatibility, cleanup and the two converter doctests: **26 passed in 6.50 s**.
The enabled/default routing controls use an injected deterministic engine result;
they check dispatch and evidence retention, not chemical validity of that result.
Disabled controls compare exact pairs and physical coordinates against independent
fixed-field reads of the unchanged bundled 181L source, including pm unit policy
and source selection.

The full affected public-route regression is:

```bash
conda activate molsyssuite@uibcdf_3.14
env PYTHONPATH=/tmp/molsysmt-consumer-298-kr3fq23_/public_support:$PWD \
    python -m pytest --receptor=llm \
    tests/form/file_pdb/test_connectivity_policy.py \
    tests/form/file_pdb/test_to_molsysmt_native.py \
    tests/form/file_pdb/test_b_factor.py \
    tests/form/molsysmt_PDBFileHandler/test_to_molsysmt_native.py \
    tests/form/string_pdb_text \
    --doctest-modules \
    molsysmt/form/file_pdb/to_molsysmt_MolSys.py \
    molsysmt/form/file_pdb/to_molsysmt_Topology.py \
    --junitxml=/tmp/molsysmt-304-policy.xml
```

**406 passed in 206.95 s, no warnings or skips reported.** This includes the
focused controls; the two run totals must not be added as unique tests. The
activated-env spelling is equivalent to the actual run's explicit interpreter.
Linux/Python 3.14.7, released ArgDigest 0.13.0 source override, OpenMM 8.6.1,
NumPy 2.4.6 and pandas 2.3.3, based on clean HEAD `31ec38171` plus this patch.
This is source contract evidence, not a full suite or installed-artifact gate.

The additive signatures are declared in the existing API waiver registry with
the exact owning functions, #304 rationale and executable guard. Ruff lint/format,
API classification/signature checks, public docstrings (240 functions), dependency
imports, developer-guide and course checks (156 notebooks) pass. Sphinx HTML
builds in the existing Python 3.13 documentation environment, with 777 warnings
from the accepted #144 debt; it is not a clean documentation build. No warning
names the new connectivity anchor or its edited User Guide pages.
Foundations, the PDB Toolbox page, chemical-template Cookbook and Module 01
describe the policy. Notebook code cells and executed outputs remain unchanged.

### Remaining provider work

The direct-file defect is corrected; #304 stays partial for the requested native
method and explicit provenance/diagnostics. Do not equate the forwarding fix with
native inference qualification. The legacy handler still attempts OpenMM by
default and catches inference failure; no new engine selection, failure evidence
record or automatic native fallback is introduced.

Next, define the general candidate/coverage report and qualify the native
template/known-polymer subset before exposing it through the reader. Preserve
unknown groups, actual chain segments and declared alternative sites; compare
literal expected edges and retain original 1IEP disagreements. Keep geometric
fallback and modified chemistry as explicit scientific policies rather than
calling the current mixed heuristic a chemically complete reader.

### Native candidate prerequisite — 2026-10-05

Review of the general build tool reproduced peptide candidates across declared
chains, selected source-group gaps and nearby nonadjacent groups. Integer atom
selections also reached the nested group query on the wrong axis. This is tracked
as uibcdf/molsysmt#328 with public regression controls in
`tests/build/get_missing_bonds/test_peptide_candidates.py`. That tool was
corrected and published in `d6a7ded29`, with 28 focused tests and five exact-commit
CI checks passing. This remains a prerequisite correction; it does not add a
reader engine selector, coverage/provenance report or file-segment/alternative-site policy.


## Bounded template candidate report — 2026-10-05

**Implemented and contract-tested.** `build.get_covalent_bond_candidates()` is a
new experimental general tool. Its first method, `exact_heavy_group_templates`,
consumes `build.get_residue_chemical_coverage()` rather than copying reference
chemistry into a parser. It returns a detached `molsysmt.covalent_bond_candidates@1`
report with typed source pairs, aligned source group indices and a missing-edge
mask, original software versions, template identity/hashes and explicit exclusions.
It does not alter the source or append inferred edges.

Integer selections refer to atom indices, with both candidate endpoints selected;
whole containing groups are assessed. Duplicate/unexpected names, unsupported
or conflicting heavy elements, unresolved states and contradictory stored
intra-group chemistry block the affected group. Missing endpoint names can leave
a partial set of mapped edges. `assessed` qualifies this bounded candidate
comparison, not stored-graph validity or biological preparation.

The implementation delegates numeric/all H5MSM 0.5 atom-axis discovery to the
public `h5msm.read_layers(..., layers=['topology'])` route, then uses the auditor's
bounded selected-structure coordinate access. A guard rejects any attempt to
materialize the full trajectory. Rich selections retain source behavior and may
require broader access. PDB normalization disables reader inference explicitly;
OpenMM import blocking is exercised by a public candidate-generation control.
Legacy files and caller-owned legacy handlers retain their existing adapter
route. The handler remains open after the query. The 0.5 layer reader is not
used for legacy sources.

There is no new optional engine boundary or dependency. No Ackredit tracking
boundary is introduced; existing detached template source provenance remains
available without inventing citations for the legacy database. Public defaults
and the legacy `get_missing_bonds()` output are unchanged. The root maintainer
instructions now explicitly distinguish general structures/groups from external
frames/residues, and distinguish source indices from IDs.

### Executed controls

```bash
python -m pytest --receptor=llm \
    tests/build/test_get_covalent_bond_candidates.py \
    tests/build/test_get_residue_chemical_coverage.py \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    --doctest-modules molsysmt/build/get_covalent_bond_candidates.py \
    --junitxml=/tmp/molsysmt-304-candidates.xml
```

Final receipt: **76 passed in 27.99 s**, with eleven legacy H5MSM deprecations
and one existing pandas setter FutureWarning retained. This supersedes the
earlier overlapping 74-test combined and 31-test subset checkpoints; their
counts are not additional unique tests. The added controls prove
literal ALA/MSE edge sets, partial inventory, conflict rejection, source
immutability, non-default pm policy, topology-only input, typed empties, source
structure indices, state association/ambiguity, bounded H5MSM 0.5 access,
legacy file compatibility and caller-owned handler lifetime.

Public docstring, signature/classification, dependency, Ruff and 156-module
course controls pass. Foundations, Toolbox, Cookbook and Common Core 12 now
explain the same bounded contract. Notebook executable cells and saved outputs
are unchanged. Incremental Sphinx HTML completes with 27 existing warnings;
no new warning message is introduced relative to the earlier #304 build.

### Original-source probe

```bash
MSM_CANDIDATES_VINA_ROOT="$HOME/repos@others/AutoDock-Vina"
python devtools/scripts/probe_covalent_bond_candidates.py \
    molsysmt/data/pdb/181l.pdb \
    "$MSM_CANDIDATES_VINA_ROOT/example/basic_docking/solution/1iep_receptorH.pdb" \
    --output /tmp/native_covalent_candidate_profile.json
```

The source checksums match the original inputs in #304. The retained receipt is
[`native_covalent_candidate_profile_20261005.json`](../../devtools/data/native_covalent_candidate_profile_20261005.json).
On 181L (1,441 atoms / 302 groups), the method returns **1,148 heavy intra-group
candidates**: 162 assessed groups and 140 unassessed groups. Original 1IEP
(4,412 atoms / 274 groups) returns **2,015 heavy intra-group candidates** with
274 assessed group mappings. The explicit-only input coordinates and source
bytes are unchanged. These counts are not complete covalent graphs, OpenMM
parity or independent chemical truth; hydrogen and inter-group edges are excluded.
The pair hash retains output identity without vendoring a second PDB fixture.

Linux x86_64, Python 3.14.7 / NumPy 2.4.6, released ArgDigest 0.13.0 source
overlay. The scientific source is based on `d6a7ded29` plus this change; the
receipt preserves the active editable installation's declared software version,
which is distinct from source commit identity. No installed-release or full-suite
qualification is claimed. This probe measures coverage, not time or memory.

### Work still required for #304

Qualify polymer links separately, including source chain segments, TER,
insertion codes and alternative sites. Hydrogen edges need an explicit supported
naming/template policy. Water/ion/small-molecule coverage and disulfide policies
remain separate from the initial amino-acid heavy-template method. Then compose
those supported reports in a selectable native PDB reader route with explicit
engine absence/failure diagnostics and persisted provenance; retain the OpenMM
route and the existing reader default. Timing/memory measurements and explained
original-source edge disagreements remain pending. #304 is still partial.
