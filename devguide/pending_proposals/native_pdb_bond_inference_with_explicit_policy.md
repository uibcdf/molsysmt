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
heavy-template, observed-H parent consensus and two bounded peptide candidate
policies are contract-tested. A bounded native application tool, explicit reader
engine selection, failure diagnostics and persisted per-edge inference provenance
are implemented and contract-tested. Complete chemical coverage and independent
scientific/performance qualification remain pending.

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

This initial design did not deliver an engine selector. The dated checkpoints
below distinguish the subsequent implementations and their remaining boundaries.

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


## Bounded peptide-link report — 2026-10-05

**Implemented and contract-tested.** `build.get_peptide_bond_candidates()` adds
an independent experimental report rather than changing the heavy-template
report or the PDB reader. Its descriptive method `adjacent_backbone_distance`
requires consecutive source group indices, one defined chain and compatible
exact heavy templates. It preserves directional carbon/nitrogen roles alongside
sorted pairs, typed empty results, original producer versions, unit-bearing
parameters/distances and inspected exclusions. Existing edges remain unchanged;
conflicting peptide types/orders or an already externally linked backbone
endpoint block the proposal. Unknown chemical quantities remain unknown.

Native PDB TER segments keep separate chain indices even when labels repeat.
Insertion-code groups keep separate source group indices even with equal group
IDs. Alternate-site evidence at either backbone endpoint blocks this first
policy; side-chain alternates do not block a unique backbone pair. Outgoing OXT
is excluded. These are explicit conservative policies, not sequence completion,
conformer selection or certified peptide chemistry. File evidence discarded by
another adapter cannot be recovered from its labels.

The positive finite C-N distance must obey both the requested length ceiling
(default 2 angstroms) and the existing protein reference plus tolerance
(**0.153 nm**). PBC is disabled by default. Explicit PBC requests use a valid
available box; invalid boxes remain unassessed. A missing box retains Cartesian
geometry. Distances use the existing paired geometry tool and its Rust primitives;
no new compiled routine, empirical criterion citation or optional engine is
invented. The legacy threshold's original reference is not independently
qualified here. No new Ackredit attribution boundary is introduced.

Normalization is shared privately behind the two supported build tools. Numeric
H5MSM 0.5 reads use topology/chemical layers and a single coordinate structure,
box and sparse alternate-site evidence. The general 0.5 form iterator now reads
requested alternate structures with source atom-index keys, reusing its codec.
A guard rejects full-coordinate materialization while selecting nonconsecutive
structures and source atoms. Rich selections retain existing broader access.
Stored-edge collision checks use an atom-to-incident-edge index built once;
geometry evaluates eligible pairs, never a Cartesian atom-pair matrix. These
are algorithmic properties, not measured throughput or RSS claims.

Two independent adapter/query findings were reported. uibcdf/molsysmt#329 corrected
public `get` stringification of alternate mapping indices as though they were IDs.
The candidate tool continues using source-preserving native/form iterators for
bounded geometry access. uibcdf/molsysmt#330 fixes legacy iterator reads
of an absent box and is recorded in the
[resolved report](../archive/resolved_bugs/legacy_h5msm_iterator_indexes_an_absent_periodic_box.md).
Legacy alternate-label arrays unsupported by the sparse-site contract remain
unassessed rather than being ignored. Caller-owned handlers stay open.

### Executed controls

```bash
python -m pytest --receptor=llm \
    tests/build/test_get_peptide_bond_candidates.py \
    tests/build/test_get_covalent_bond_candidates.py \
    tests/build/test_get_residue_chemical_coverage.py \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    tests/form/file_h5msm/test_structures_v05_probe.py \
    --doctest-modules molsysmt/build/get_peptide_bond_candidates.py \
        molsysmt/build/get_covalent_bond_candidates.py \
    --junitxml=/tmp/molsysmt-304-peptide-final.xml
```

Receipt: **147 passed in 32.68 s**, with 28 legacy deprecations and two existing
pandas setter FutureWarnings. Controls include chain and repeated-label TER
boundaries, insertion codes, IDs versus indices, selection gaps, reordered atom
roles, existing CONECT evidence, contradictory chemistry, empty/no-coordinate
inputs, state associations, OXT, alternate backbone/side-chain evidence, Cartesian
and MIC geometry, non-default pm policy and legacy filenames/handler lifetimes.
This overlaps prior checkpoints; their counts are not additional unique tests.

The docstring, public classification/signature, course and Ruff controls pass.
Foundations, Toolbox, Cookbook and Common Core 12 describe the bounded contract;
notebook executable cells and outputs are unchanged. Incremental Sphinx HTML
completes with 27 existing warnings and no new warning message.

### Original-source probe

```bash
MSM_CANDIDATES_VINA_ROOT="$HOME/repos@others/AutoDock-Vina"
python devtools/scripts/probe_covalent_bond_candidates.py \
    molsysmt/data/pdb/181l.pdb \
    "$MSM_CANDIDATES_VINA_ROOT/example/basic_docking/solution/1iep_receptorH.pdb" \
    --include-peptide --output /tmp/native_peptide_candidate_profile.json
```

The retained receipt is
[`native_peptide_candidate_profile_20261005.json`](../../devtools/data/native_peptide_candidate_profile_20261005.json).
Original input hashes and heavy-template candidate hashes match the previous
probe. 181L returns **161 peptide candidates**, in addition to its 1,148 heavy
intra-group candidates. Original 1IEP returns **271 peptide candidates**, in
addition to 2,015 heavy intra-group candidates. Its selected source boundaries
[0, 1] (C atom 3425, N atom 1, **45.8397588 angstroms**) and [213, 214]
(C atom 3408, N atom 3431, **3.9893169 angstroms**) are rejected by distance.
These are source group/atom indices, not IDs. Their physical distances, rather
than label adjacency or a wish to match OpenMM's graph, explain exclusion.
The rejected groups are SER 438 / MET 225 and MET 437 / PRO 439 respectively,
all in source chain index 0. These labels are observed metadata, not inferred
sequence links. SER 438 is the first group encountered on the source axis despite
its biological sequence position. This demonstrates that source group order is
not always polymer sequence order; the bounded method cannot propose its
nonconsecutive sequence neighbors. A qualified native reader therefore still
needs an explicit source polymer-order policy before claiming full coverage.
No complete chemical graph, hydrogen coverage, timing/memory benchmark or
independent chemical ground truth is established. Source bytes and coordinates
remain unchanged.

Linux x86_64, Python 3.14.7 / NumPy 2.4.6, released ArgDigest 0.13.0 source
overlay, source base `c2f16cbc2` plus this change. Original editable installation
version strings remain in the receipt; they are distinct from source commit
identity. No installed-release qualification is claimed.

### Remaining #304 work

Source polymer-order policy, hydrogen naming/template policy, terminal caps,
other supported groups, disulfide
composition and unknown-group geometry remain separate qualifications. A native
reader engine selector, precise optional-engine absence/failure diagnostics and
persisted inference provenance are still pending. Retain the current reader
default and OpenMM route. Compare original-source edge inventories and measure
representative time/memory workloads before claiming native receptor preparation.
The separately reported public alternate-index defect in #329 and the MolSys
system-query structure-selection defect in uibcdf/molsysmt#331 are corrected.
The corresponding 147-control checkpoint includes peptide candidates, real PDB
alternate sites and alternate-conformer resolution. The subsequent
uibcdf/molsysmt#332 checkpoint preserves physical alternate-site quantities in
Structures YAML 0.2 with explicit field/unit validation; uibcdf/molsysmt#333
remaps sparse keys in supported selected structural conversions. Its 107 focused
controls include full YAML geometry, not only labels. #304 remains partial:
source polymer order, hydrogen handling and native-reader integration are still
pending.

## Source-order-independent peptide candidates — 2026-10-05

**Implemented and contract-tested.** The public form-agnostic
`build.get_peptide_bond_candidates()` accepts the optional keyword-only
`method='unique_backbone_distance'`. Existing positional arguments, defaults and
the `adjacent_backbone_distance` policy are retained. Argument digestion validates
the named method; the signature extension and its guard are declared in the API
registry. No reader policy or stored graph is changed.

### Policy and ownership

The method discovers close named C/N endpoints in the same defined source chain
without sorting group IDs, relabeling source axes or requiring adjacent storage
positions. It delegates threshold search to the existing public
`structure.get_neighbors(..., output_type='csr')` Rust cell-list route, then uses
the existing paired distance tool and shared chemical eligibility checks. There
is no new compiled primitive, geometric utility or parser-local inference engine.
The scientific orchestration remains private behind the supported build tool.

Discovery examines all existing named backbone endpoints before restricting the
output selection. Several incoming groups near one carbon, or several outgoing
groups near one nitrogen, block the affected proposals. Unselected and chemically
unassessed groups still participate in this conservative competition test;
restricting an output selection cannot manufacture uniqueness. The method retains
the exact heavy-template, OXT, stored-edge conflict, positive finite distance and
effective 0.153 nm ceiling checks. Same-group pairs and different chain segments
are excluded. Native TER boundaries retain their established adapter semantics.

Non-finite or alternate backbone geometry blocks uniqueness assessment throughout
the affected source chain, including sites outside the output selection. This is
an explicit conservative first policy, not alternate-conformer reconstruction.
Side-chain alternate sites do not block it. Discovery reports its examined source
atom indices, assessed/partial/unassessed status, reason codes, blocked chains
and groups with missing/ambiguous chain membership. An assessed empty search is
distinct from absent coordinates, unsupported alternate evidence or an invalid
requested periodic box. The nested group-coverage report audits the full source
for this method; the outer atom indices still identify the requested output scope.
Discovery also records whether its search used PBC, including an assessed search
with zero output candidates; the outer PBC flag describes eligible-pair geometry.

Uniqueness among existing named endpoints is geometric candidate evidence. It
does not certify polymer sequence, missing atoms, valence, bond order, protonation
or a complete chemical graph. The method is descriptively named and uses the
existing heuristic distance ceiling; no independently qualified literature origin,
new attribution boundary or scientific validation is claimed.

### Executed controls

```bash
python -m pytest --receptor=llm \
    tests/build/test_get_peptide_bond_candidates.py \
    tests/build/test_get_covalent_bond_candidates.py \
    tests/build/test_get_residue_chemical_coverage.py \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    tests/form/file_h5msm/test_structures_v05_probe.py \
    --doctest-modules molsysmt/build/get_peptide_bond_candidates.py \
        molsysmt/build/get_covalent_bond_candidates.py \
    --junitxml=/tmp/molsysmt-304-unique-final.xml
```

Receipt: **184 passed in 36.29 s**, with 32 expected legacy H5MSM deprecations
and three existing pandas setter FutureWarnings. Earlier overlapping 77/173/182
controls are not additional unique tests. Literal controls cover reordered source
groups and nonsequential labels, incoming/outgoing competition, unselected and
unassessed competitors, chain/TER boundaries, full-scope incomplete geometry,
typed empty selections, unknown methods, absent coordinates, invalid boxes,
stored types/orders, OXT, side-chain alternatives, unresolved states, blocked
OpenMM imports and one-structure H5MSM 0.5 access. A guard rejects a Cartesian
distance-product call during sparse discovery. PBC and pm output policy are
executed for both methods. These are contract controls, not RSS/throughput
benchmarks or complete scientific validation.

Docstring, API signature, dependency, Ruff and 156-module course checks pass.
Foundations, Toolbox, Cookbook and Common Core 12 describe the same boundaries;
notebook executable cells and outputs are unchanged. The first incremental
Sphinx HTML build completes with 58 warning entries, including existing course
directives, heading levels and undefined labels. The final incremental build
completes with **17 warning entries** after the discovery-PBC documentation update.
No clean documentation build or equal
warning count with a differently rebuilt prior checkpoint is claimed.

### Original-source probe and pair comparison

```bash
python devtools/scripts/probe_covalent_bond_candidates.py \
    molsysmt/data/pdb/181l.pdb \
    "$HOME/repos@others/AutoDock-Vina/example/basic_docking/solution/1iep_receptorH.pdb" \
    --include-peptide --peptide-method unique_backbone_distance \
    --output /tmp/native_unique_peptide_candidate_profile.json
```

The retained receipt is
[`native_unique_peptide_candidate_profile_20261005.json`](../../devtools/data/native_unique_peptide_candidate_profile_20261005.json).
Original source checksums and heavy intra-group candidate hashes match the prior
probe. 181L retains **161** peptide candidates. Original 1IEP produces **273**,
retaining all 271 previous candidates and adding these directional source pairs:

| Source atom pair | Source group pair (C group, N group) | Observed group labels | C-N distance |
| --- | --- | --- | --- |
| [3408, 3421] | [213, 0] | MET 437 / SER 438 | 1.3294882474 angstroms |
| [3425, 3431] | [0, 214] | SER 438 / PRO 439 | 1.3434381266 angstroms |

These are indices; the observed group IDs remain labels. Directly comparing with
`msm.convert(original_path, to_form='molsysmt.MolSys', get_missing_bonds=True)`
in the existing OpenMM-enabled environment yields 4,469 stored edges. Every one
of the 273 peptide candidates, including the two new pairs, occurs in that edge
inventory. The compared atom IDs, names, elements, group/chain indices and
coordinates are equal. This is parity with the existing enabled-reader route,
not independent chemical ground truth or hydrogen coverage. Source bytes and
the explicit-only input coordinates remain unchanged.

Linux x86_64, Python 3.14.7 / NumPy 2.4.6, released ArgDigest 0.13.0 source
overlay and the installed locally built PyUnitWizard 0.28.1 minimum-provider
wheel, based on `2bb60b304` plus this change. The enabled-reader comparison uses
the existing OpenMM 8.6.1 environment. The original editable MolSysMT version in
the receipt is retained; source commit identity is separate. No installed
MolSysMT release, full-suite or complete platform qualification is claimed.

### Remaining #304 work

The optional geometric policy covers this observed source-order disagreement;
independently declared polymer sequence remains unassessed. Next qualify
hydrogen naming/template edges, then compose supported reports in the selectable
native reader route with explicit absence/failure diagnostics and persisted
inference provenance. Terminal caps, other supported groups, disulfide composition,
unknown-group geometric policy and representative time/memory measurements remain
separate work. Retain the current reader default and the OpenMM route. #304 stays
partial; this checkpoint does not claim complete native receptor preparation.

## Observed hydrogen parent consensus — 2026-10-05

**Implemented and contract-tested.** The public form-agnostic
`build.get_covalent_bond_candidates()` now accepts the keyword-only
`method='observed_hydrogen_template_consensus'`. It returns only candidate
H-parent edges for H atoms already present. All existing positional arguments
and the `exact_heavy_group_templates` default are preserved. Argument digestion
and the API registry cover the extension. Neither method modifies the graph,
coordinates, chemical assignments or named interaction analyses.

### Scientific scope and reusable ownership

The tool reuses the existing whole-group chemical coverage audit and exact group
reference owner. Each observed H name is compared with **every heavy-compatible
reference variant containing that exact name**. All those variants must declare
one identical heavy parent, and both observed elements must be known and match
the reference. The parent must exist. Missing/ambiguous names, unsupported
modified-group H references, nonstandard stored H assignments and contradictory
incident H edges remain indexed exclusions. Incident edges outside the output
selection are checked too. No name alias, nearest-atom inference, first-variant
selection, pH or terminal assignment is introduced.

Local parent consensus is deliberately separate from joint H inventory evidence.
The reference study found mixed naming conventions within observed groups:
requiring one variant to contain all recognized names would discard otherwise
unambiguous local parent evidence. The implemented method instead retains both
answers. A group can supply useful local candidates while its inventory remains
`unassessed` and its status `partial`. Even a `compatible_subset` inventory does
not certify missing H atoms, protonation, terminal state, valence or H placement.
These candidates are not a hydrogen-complete receptor or chemical-state assignment.

The optional `groups[*]['hydrogen_coverage']` records parallel typed H/parent
arrays, local eligibility and output-selection masks, CSR reference-variant
membership, joint inventory indices and sparse failed-H issues. A missing parent
uses `-1`, not an invented atom index. Stored field arrays are shared with the
already detached audit inside the private implementation; source atom/bond row
maps, incident edges and reference-parent lookups are indexed once per report.
No new external dependency or compiled primitive is needed for this bounded
template lookup. Representative memory/throughput qualification is still pending.

### Executed controls and documentation

```bash
python -m pytest --receptor=llm \
    tests/build/test_get_covalent_bond_candidates.py \
    tests/build/test_get_peptide_bond_candidates.py \
    tests/build/test_get_residue_chemical_coverage.py \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    tests/form/file_h5msm/test_structures_v05_probe.py \
    --doctest-modules molsysmt/build/get_covalent_bond_candidates.py \
        molsysmt/build/get_peptide_bond_candidates.py \
        molsysmt/build/get_residue_chemical_coverage.py \
    --junitxml=/tmp/molsysmt-304-H-final.xml
```

Receipt: **216 passed in 47.15 s**, with 32 expected legacy H5MSM deprecations
and three existing pandas setter FutureWarnings. The earlier overlapping
61-test run is not additional coverage. Literal tests check exact H-parent
roles, both-endpoint selections, typed empty arrays, unknown names/elements,
missing parents, modified heavy-only references, stored external partners and
conflicting H types/orders/assignments. Synthetic reference variants disagreeing
on a parent or lacking the H edge reject a first-variant shortcut; they do not
claim that the packaged provider contains those defects. Mixed recognized names
exercise local consensus with no compatible joint inventory. PDB controls reject
OpenMM imports for both methods. A selected H5MSM 0.5 structure/state query rejects
full-trajectory materialization and runs with pm output policy; an unassociated
state remains unassessed.

After adding the optional-method docstring example, its doctest is repeated:
**1 passed in 4.11 s**, with 13 legacy H5MSM warnings. This overlaps the combined
run rather than increasing its unique count. Ruff, public signature, dependency,
242-function docstring and maintained 156-module course checks pass. The old
`docs/content/course/devtools/validate_course.py` was also tried and rejects its
obsolete section template (0/156); it is not the maintained release gate.
Foundations, Toolbox, Cookbook and Common Core 12 describe the same bounded
contract. Notebook executable cells and outputs are unchanged. Incremental
Sphinx HTML completes with **27 warning entries**, including existing heading,
directive, toctree and reference debt; no clean build or equal warning count
with a differently rebuilt checkpoint is claimed.

### Unchanged original-source evidence

```bash
python devtools/scripts/probe_covalent_bond_candidates.py \
    molsysmt/data/pdb/181l.pdb \
    "$HOME/repos@others/AutoDock-Vina/example/basic_docking/solution/1iep_receptorH.pdb" \
    --include-peptide --peptide-method unique_backbone_distance \
    --include-hydrogen --output /tmp/native_hydrogen_candidate_profile.json
```

The retained receipt is
[`native_hydrogen_candidate_profile_20261005.json`](../../devtools/data/native_hydrogen_candidate_profile_20261005.json).
181L has no observed H and returns a typed empty H candidate result. Original
1IEP has **2,183 observed H atoms** and yields **2,157 H-parent candidates**.
The remaining 26 names lack an exact reference in their own group: HN1 (1),
HN3 (1), HN (17), HB1 (6) and HC (1). Names are group-specific: HN is a legitimate
ALA reference name, so an initial synthetic unknown-name test was corrected to
HN1 rather than excluding that valid reference. 156 groups have a compatible
joint naming subset, while 118 remain partial with an unassessed joint inventory.
Heavy and peptide candidate counts/hashes match the previous receipt. Original
file bytes and coordinates are unchanged.

The separate
[`native_hydrogen_reader_comparison_20261005.json`](../../devtools/data/native_hydrogen_reader_comparison_20261005.json)
compares these pairs with the existing enabled-reader graph (4,469 edges).
**2,156 of 2,157 candidates occur in that graph.** The disagreement is source
pair `[0, 3427]`, HB2-CB in source group index 0, SER with group ID `438`.
The enabled reader gives source H index 0 no incident edge; the reference
consensus proposes CB and the observed distance is 1.1150762306 angstroms.
This difference is retained rather than forcing either candidate inventory to
match the other. Compared source atom IDs, names, elements, group/chain indices
and coordinates are equal. Enabled-reader parity and a plausible distance are
not independent chemical ground truth. The unresolved names and inventory
disagreement still require explicit handling before native-reader qualification.

Linux x86_64, Python 3.14.7 / NumPy 2.4.6, released ArgDigest 0.13.0 source
overlay and installed locally built PyUnitWizard 0.28.1 minimum-provider wheel;
source base `a8f567c82c348bb003475e8b608721d1e51a9e07` plus this change.
The reader comparison uses the existing OpenMM 8.6.1 environment. Original
editable MolSysMT producer versions remain in both receipts; source commit
identity is separate. No installed MolSysMT release, full-suite, platform or
complete native-preparation qualification is claimed.

### Remaining #304 work

Compose the supported heavy, peptide and observed-H reports behind an explicit
native-reader engine policy, including diagnostics for absent/failed optional
engines and persisted inferred/declared edge provenance. Define the permitted
application policy for local H consensus, unresolved names, mixed inventories
and the recorded enabled-reader disagreement; do not silently complete them.
Terminal caps, other supported groups, disulfide composition, unknown-group
geometry and representative performance measurements remain separate work.
Retain the current reader default and OpenMM route. #304 remains partial.

## Explicit native application and reader engines — 2026-10-05

**Implemented and contract-tested.** The public form-agnostic
`build.infer_covalent_bonds(..., method='supported_group_templates')` composes
the existing heavy-template, observed-H local parent consensus and
`unique_backbone_distance` tools. It returns a detached MolSys, optionally with
its report. Scientific criteria remain in the general candidate tools; the PDB
adapter selects policy and consumes this general application tool.

### Application, state and historical evidence

Both endpoints must belong to the output selection, while whole-group chemistry
and source backbone competitors are assessed first. No source atom, coordinate
or label is changed. Existing edges and their assignments retain precedence;
only missing eligible edges are appended as inferred covalent bonds with unknown
orders. One chemical state must resolve, and one structure supplies geometry when
coordinates exist. All source structures remain in the output. Topology-only input
can still supply heavy and observed-H evidence without fabricated geometry.

Application explicitly permits the previously qualified local H-parent consensus,
including groups whose joint H inventory remains unassessed. It does not resolve
aliases, choose a protonation state or certify hydrogen completeness. Unresolved
names and mixed inventory evidence remain in the report. Added bonds mark graph
completeness partial and invalidate all named interaction occurrence coverage in
the output; a no-addition result preserves its analyses. Source systems remain
unchanged in both cases.

The owning state's preparation history retains `molsysmt.covalent_inference@1`
evidence, software producer, original axes, selected scope, candidates, additions,
method codes, exclusions and source-to-result bond indices. Method membership uses
parallel int8 indices into three method names, rather than a Python string per
edge. Peptide distances and thresholds use explicit nm QuantityRecord payloads;
there are no coordinate snapshots. Added edges refer to the local history entry
through `provenance_index`. H5MSM 0.5 retains these references and the producer
version. Extraction preserves historical operation axes while remapping live
bond rows; merging offsets references to these known local history schemas while
preserving unrelated opaque origins and the original historical reports.

### Reader policy

The six file/handler/text-to-MolSys/Topology converters accept the keyword-only
`bond_inference_engine` without changing previous positional arguments or defaults:

- `get_missing_bonds=False`: declared PDB edges only; an explicit engine conflicts.
- `get_missing_bonds=True, bond_inference_engine='MolSysMT'`: the native tool above,
  with no OpenMM import or fallback. Geometry uses source structure index 0 before
  extraction; parsed models share the inferred graph.
- `get_missing_bonds=True, bond_inference_engine='OpenMM'`: lazily guarded OpenMM
  calculation; an explicitly requested engine's error propagates.
- `get_missing_bonds=True, bond_inference_engine=None`: the existing optional
  OpenMM policy. Absence or failure preserves declared edges, emits structured
  `MSM-WARN-PDB-001` diagnostics and archives the cause instead of swallowing it.

Text-to-MolSys still defaults to disabled inference, so an explicit engine also
requires `get_missing_bonds=True`. There is no automatic native fallback or reader
default change. `molsysmt.pdb_connectivity@1` records disabled, inferred, unavailable
or failed outcomes, requested/attempted/actual engines, producer, inferred bond
indices and aggregate unresolved/repeated declaration flags. Complete per-record
declaration diagnosis remains pending. Only handles opened by the conversion are
closed, including failure paths.

### Executed controls and documentation

```bash
python -m pytest --receptor=llm \
    tests/build/test_infer_covalent_bonds.py \
    tests/form/file_pdb/test_connectivity_policy.py \
    tests/form/file_pdb/test_to_molsysmt_native.py \
    tests/form/file_pdb/test_pdb_parser_regression.py \
    tests/build/test_get_covalent_bond_candidates.py \
    tests/build/test_get_peptide_bond_candidates.py \
    tests/build/test_get_residue_chemical_coverage.py \
    tests/test_argument_contract.py \
    tests/native/test_preparation_history.py \
    tests/_private/test_smonitor_catalog_integrity.py \
    tests/_private/smonitor/test_xdist_warning_reconstruction.py \
    --doctest-modules molsysmt/build/infer_covalent_bonds.py \
        molsysmt/form/file_pdb/to_molsysmt_MolSys.py \
        molsysmt/form/file_pdb/to_molsysmt_Topology.py \
    --junitxml=/tmp/molsysmt-304-reader-qualified.xml
```

Receipt: **532 passed in 105.65 s**, with 18 legacy H5MSM deprecations,
14 existing H5MSM pandas downcast FutureWarnings, two existing topology setter
FutureWarnings and one expected cross-chain declaration warning. The final
invalid-`skip_digestion` boundary guard is then checked with the inference test
module and its doctest: **15 passed in 7.73 s**, receipt
`/tmp/molsysmt-304-reader-boundary.xml`. These runs overlap; their counts must not
be summed as unique coverage. The temporary boundary guard names its removal
condition, a public ArgDigest floor containing uibcdf/argdigest#17.

Literal controls cover appended pairs and retained bond orders/evidence, detached
source/report ownership, typed method codes, selected/empty scope, unresolved
states, selected nonreference states, topology without coordinates, interaction
invalidation, six PDB conversion routes, blocked OpenMM imports, declared-edge
precedence, handler lifetime, explicit versus legacy engine failures, historical
H5MSM persistence and merge reference offsets. An intermediate diagnostic gate
correctly rejected missing QA/agent catalog fields and the absent reconstruction
sample; those omissions were fixed before the combined receipt.

Ruff, lazy-dependency, 243-function docstring and public API checks pass, with six
intentional converter signature waivers. The form audit passes 96/96 structural
checks and its delivery ratchet; its 78 accepted unreachable attributes remain
existing debt, not new delivered capability. Foundations, Toolbox, Cookbook and
Common Core 12 describe the application and reader policies. The maintained
course validator passes for 156 notebooks; edited notebook executable cells and
outputs are unchanged. Final incremental Sphinx HTML completes with **17 warning
entries** and no warning naming the new tool. Existing heading, directive,
toctree and reference debt remains; no clean documentation build is claimed.

### Original-source reader and storage probe

```bash
MSM_NATIVE_VINA_ROOT="$HOME/repos@others/AutoDock-Vina"
python devtools/scripts/probe_native_pdb_connectivity.py \
    molsysmt/data/pdb/181l.pdb \
    "$MSM_NATIVE_VINA_ROOT/example/basic_docking/solution/1iep_receptorH.pdb" \
    --compare-openmm \
    --output devtools/data/native_pdb_reader_profile_20261005.json
```

The retained
[`native_pdb_reader_profile_20261005.json`](../../devtools/data/native_pdb_reader_profile_20261005.json)
records original source checksums, axis/coordinate/pair hashes, producer versions,
source base commit and six implementation file fingerprints. Source bytes and
coordinates remain unchanged; compared source atom axes match. Native runs reject
all OpenMM imports. Native H5MSM round trips retain graph, geometry and producer.

| Original input | Declared edges | Native edges | OpenMM edges | Native-only / OpenMM-only |
| --- | ---: | ---: | ---: | ---: |
| 181L | 13 | 1,322 | 1,322 | 0 / 0 |
| 1IEP receptorH | 0 | 4,445 | 4,469 | 1 / 25 |

The 181L application adds 1,309 edges. 1IEP combines 2,015 heavy edges,
273 peptide edges and 2,157 observed-H edges. Its native-only HB2-CB pair and
26 unresolved group-specific H names remain the observed consensus checkpoint's
explicit scientific qualifications. OpenMM parity is not independent ground truth.

Each route runs in a fresh process, imports MolSysMT, then performs two conversions.
The first and repeated conversions are individual observations without a warm-up
series, replication or statistical summary; timings exclude interpreter/package
startup. RSS is the whole-process high-water mark, including startup, both
conversions and, for the native route, H5MSM write/read verification. It is not
incremental inference memory or an isolated serialization comparison.

| Input / route | First conversion (s) | Repeated conversion (s) | Process peak RSS (MiB) |
| --- | ---: | ---: | ---: |
| 181L / disabled | 3.473 | 0.147 | 387.0 |
| 181L / native | 4.523 | 1.146 | 433.2 |
| 181L / OpenMM | 3.936 | 0.303 | 462.9 |
| 1IEP / disabled | 3.697 | 0.100 | 391.1 |
| 1IEP / native | 5.034 | 1.618 | 446.6 |
| 1IEP / OpenMM | 4.027 | 0.587 | 479.7 |

Native H5MSM files occupy **3,174,095 bytes** for 181L and **6,518,360 bytes**
for 1IEP. Their observed write/read times are respectively 1.025/0.990 s and
0.947/1.141 s. Typed history contains many small arrays; HDF5 dataset overhead
still contributes substantial storage. The native route is slower than OpenMM
in these observations, although its whole-process RSS is lower under the stated
different measurement scopes. Neither result establishes scalability or a global
performance advantage. Packing and representative workloads need further study.

Linux x86_64, Python 3.14.7, NumPy 2.4.6, released ArgDigest 0.13.0 source
overlay, installed locally built PyUnitWizard 0.28.1 minimum-provider wheel and
OpenMM 8.6.1; source base `29a3817854de14db0b1076263e189a1e7c5dbebf` plus the
fingerprinted implementation. The actual editable MolSysMT producer version
`0.22.4+60.g7a8350f76.dirty` is retained separately from source identity. No installed
MolSysMT release, full-suite, platform matrix or independent chemical qualification
is claimed.

### Remaining #304 work

The explicit bounded reader/application contract and failure provenance are now
delivered. Next qualify H naming aliases and terminal conventions without hiding
the original-input exclusions or forcing OpenMM parity. Terminal caps, additional
supported groups, disulfide composition, unknown-group geometry, full declaration
diagnosis, independently established chemical inventories and larger time/memory/
storage workloads remain pending. The native application currently materializes
and copies the complete system; it is not a streaming preparation route.
Retain the reader defaults and the optional OpenMM route. **#304 stays partial.**
