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
are implemented and contract-tested. Explicitly naming-scoped cap references
and their bounded amide endpoints are also contract-tested. Direct-reader
naming context is delivered before classification/inference.
Curated modified-group application and declared-only disulfide/coordination plus
disabled unsupported-group geometry policies are contract-tested. Final combined
qualification/integration is pending; none of these tools certifies complete chemistry.

**Scheduling — 2026-10-05:** the bounded engine/application contract is included
experimentally in the [frozen 1.0 scope](../release_1_0_scope.md). Remaining H-name,
terminal/group/disulfide/declaration and performance extensions stay owned by
#304 in the post-1.0 backlog. Correctness defects in the offered profile remain
admissible stabilization work; this scheduling decision does not close the issue
or certify complete native receptor preparation.

**Current scheduling — 2026-11-06:** the maintainer's
[ordered resolution objective](../release_1_0_status.md#maintainer-ordered-resolution-goal--2026-11-06)
explicitly resumes the remaining #304 work before closeout. The earlier
post-1.0 allocation is not a reason to stop that authorized work. This retains
the bounded connectivity scope and separate release authorization.

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

The first direct-push checkpoint `7b51c240f` passes smoke, Ruff and suite/Conda
governance, but its developer-guide CI rejects the stale generated API registry
view. The implementation registry already contains the new experimental tool;
the missing step was regenerating `api_stability_registry.md`. The follow-up
uses `validate_api_stability.py --write-doc`; the 263-symbol registry and generated
view then pass their local check. This correction changes documentation only;
scientific test and implementation-fingerprint receipts above remain applicable.

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

## CIF/BCIF disabled-inference correction — 2026-11-06

The maintainer's ordered goal starts with full resolution of #304. This section
receives PeptideMT's new wrapper observation; it does not close the earlier
chemical-coverage, declaration-diagnosis or workload requirements.

### What and reproduced mechanism

The DataContainer-to-Topology converter accepted `get_missing_bonds` without
reading or forwarding it. The native MolSys reader and CIF/BCIF/gzip/identifier
wrappers did not accept the flag, allowing public conversion to discard the
policy. Ten file/container/target controls reproduce a candidate-tool call with
inference disabled. An additional independent control reproduces loss of a
mapped explicit double bond when another source atom lacks a reference.

Initial draft assertions also assumed requested atom order and deposited model
labels were retained. The existing external conversion retains atoms in source
order, and does not populate native structure IDs. Policy assertions now check
actual selected coordinate/occupancy axes instead of inventing a label guarantee.
The declared-ID delivery mismatch is reported separately and is not fixed or
hidden by the connectivity correction.

### Implemented policy and ownership

Eleven native readers/wrappers add a keyword-only Boolean policy; the parsed
Topology reader forwards its existing positional flag. Every earlier positional
argument and enabled default survives. The established ArgDigest validator owns
Boolean admission. False disables local template, terminal-H, inferred peptide
and distance additions; mapped component-bond and supported connection evidence
remain explicit. A partial reference match no longer discards declared edges or
orders before an inference attempt. Existing general candidate operations and
BondAccumulator remain the chemistry/metadata owners; no scientific formula,
compiled kernel, dependency, unit policy or file schema is added.

An explicit-only output is partial: retaining declared edges does not establish
complete chemistry. True and omitted policy have matching real-source graphs
and observations. No OpenMM engine is imported for the supported disabled route.
Unsupported connection declarations and their broader diagnosis are not newly
qualified by this policy fix.

### Executed evidence and scope

- New policy module: 26 passed in 6.77 s, including five container/file variants,
  both native targets, offline identifier acquisition, invalid Boolean refusal,
  real 1VII BCIF without OpenMM imports, source preservation, explicit orders,
  three source structures selected as [2, 0], occupancy and noncanonical units.
- Affected CIF/BCIF/identifier/fidelity selection: 864 passed in 34.37 s.
- Signature guard against parent 282e8337e passes with eleven explicit
  maintainer-authorized additive signature entries. No existing parameter is
  renamed or reinterpreted.

These are local source controls, not full release/scientific qualification.
The work starts from 282e8337e04c14003622c19a359b7cd35d2b5e4b in a separate
ordered-work branch. The original PR candidate and its live full CI remain
unchanged. Linux/Python 3.14.7; shared development interpreter, four workers,
Pytest Receptor llm. Original course/tool notebook executable cells and metadata
are preserved. The new reader policy is documented in Foundations, form Toolbox,
the explicit-template Cookbook and Common Core 12.

Remaining before #304 closure: complete the earlier native-profile coverage,
source-declaration diagnostics, independent inventory/comparison explanations and
representative workload evidence. This forwarding correction alone is insufficient.

### Additional receiving evidence

The relevant inference/argument selection initially passes 278 cases and fails
one generated-inventory guard. The generator identifies four missing source-
naming keyword entries introduced by the earlier GRO receiving checkpoint;
this is pre-existing in parent 282e8337e, not a scientific inference failure.
The committed converter-argument inventory is regenerated from actual adapter
signatures instead of weakening the guard. The independent default/False
policy and mapped-edge controls remain unchanged.

The directed policy/occupancy controls also pass 51 cases against the published
ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads.
This is a four-provider floor profile using the existing interpreter and current
other dependencies, not a full clean installed-runtime minimum matrix.
Documentation/schema/source-boundary receiving passes 1,072 cases; retained
Sphinx/legacy/explicit-unassessed warnings are not suppressed. These suites
overlap with other selections and are not additive unique test counts.

Final source receiving after regeneration passes the full 279-case inference/
argument/doctest selection (18.07 s, twelve workers) and a 47-case final contract
selection (11.56 s). Structural form checks pass for 97 adapters without declaring
runtime-field fidelity; #600 is an explicit counterexample to treating that
structural result as scientific delivery proof. Ruff, formatting, dependency
imports/contracts and 247-function docstring validation pass. The
[policy receipt](../../devtools/data/cif_connectivity_policy_receiving_304_20261106.json)
retains source/test/backend hashes, actual four-provider public import origins,
individual overlapping JUnit results, draft failures and remaining issue scope.

## Typed deposited-declaration audit — 2026-11-06

### What and implementation

The reader's two coarse flags could not identify an unresolved declaration or
distinguish a missing endpoint from an ambiguous identity, self-reference,
symmetry image or conditional alternate mapping. The normalized handler now
retains LINK/SSBOND symmetry operators, original fixed-column record text and
1-based source line numbers. A format-private resolver is shared by native
construction and public conversion assessment. Symbolic and serial indexes are
built once when the corresponding record kinds exist; a source with no
declarations needs neither index. No general chemistry is duplicated in the
adapter, and no public signature, dependency or compiled routine changes.

The first `molsysmt.pdb_connectivity@1` report keeps its existing coarse keys and
adds a nested `molsysmt.pdb_declarations@1` typed table. Its rows identify record
kind/index, CONECT target ordinal, source line/text, directed canonical endpoint
indices, endpoint match counts, status, acceptance, conditional scope, alternate
labels and symmetry operators. Missing/ambiguous endpoint indices are -1.
Empty tables have defined dtypes and `(0, 2)` endpoint shapes; no occurrence
objects or object arrays persist. The preparation-history codec and H5MSM 0.5
retain these arrays without a new file schema. Historical indices stay on the
original first-model canonical-site axis after extraction.

### Scientific boundary and corrected draft assumptions

Interpretation follows wwPDB PDB 3.3 sections 6 and 10 (references retained in
the report). An unknown requested alternate is not silently matched to another
site; a nonidentity symmetry operation is not flattened onto the observed base
cell. Reciprocal/repeated declarations retain one pair without assigning order.
Multiple declared CYS sulfur partners are retained and explicitly flagged;
record order or distance does not select a supposedly valid disulfide state.
LINK/CONECT alone do not establish chemical bond kind, valence or completeness.

The first test draft assumed a nullable bond-order column must be physically
present; this reader legitimately represents an entirely unknown order by an
absent column. The guard now requires that no order be assigned, supporting both
representations. A later draft rejected all connections involving alternate
sites. The existing fidelity guard correctly rejected that narrowing: known
alternate serials already map to canonical sites. That public contract is
preserved; new conditional-scope evidence qualifies the claim instead of
discarding deposited connectivity. Full alternate-specific chemical states
remain unassessed. Neither failure is hidden by weakening the existing guard.

Public conversion reports now expose unresolved, conditional and contradictory
declarations through the existing adapter-limitation boundary; strict conversion
rejects those limitations. Complete chemical certification is not introduced.

### Executed evidence

- Nineteen new public controls cover file/handler/text parity, exact source
  record locations, redundancy, missing/self/empty endpoints, duplicate serials,
  repeated symbolic identities across TER, insertion codes, identity/nonidentity
  symmetry, known/missing alternate scope, conflicting sulfur partners, typed
  empty results, extraction and detached H5MSM persistence.
- The full affected reader/native/fidelity/application selection passes
  **637 cases in 66.69 s** with twelve workers. A subsequent index-allocation
  optimization is covered by **87 final directed cases in 11.85 s**.
- Four published-provider floor receiving passes **48 cases in 12.88 s**;
  actual ArgDigest/DepDigest/SMonitor/Ackredit origins and hashes are recorded.
  Other dependencies remain current; this is not a clean installed-floor matrix.
- Documentation/source-boundary receiving passes **1,072 cases in 43.23 s**.
  Retained warnings remain visible. Foundations, form Toolbox, Cookbook, course
  and the reader docstring agree. Both edited notebooks preserve all executable
  cells, outputs, IDs and metadata.
- Repeating the original-source reader probe preserves 181L's 13/1,322/1,322
  and original 1IEP's 0/4,445/4,469 disabled/native/OpenMM graphs, source axes and
  coordinates. Its two timing observations/process RSS are not a statistical
  performance qualification or an explanation of the remaining disagreements.

Ruff lint/format, dependency imports/contracts, public API stability and the
247-function docstring check pass. Linux/Python 3.14.7, existing development
environment and unchanged compiled backend. See the
[receiving receipt](../../devtools/data/pdb_declaration_receiving_304_20261106.json)
for exact source hashes, original-input probe, failure history, import origins,
notebook preservation and individual overlapping JUnit results.

**#304 remains partial.** Next complete the approved H-name/terminal and group/
disulfide/geometry policies, independently explain original-source differences,
and qualify representative cold/warm, memory and storage scaling. This audit
does not authorize a release or claim complete receptor preparation.

## Original pair diagnosis and repeated workload evidence — 2026-11-06

### What and independent source interpretation

All original 1IEP disagreements are now classified without modifying its bytes
or forcing parity. Direct fixed-column reads identify the 25 OpenMM-only pairs:
HN1 (1), HN3 (1), HN (17) and HB1 (6). The actual installed OpenMM 8.6.1
`pdbNames.xml` maps those source names to H, H3, H and HB3, respectively; the
installed resource's SHA-256 exactly matches inspected primary OpenMM source
`ba0aa236ac4d07241382869604c4d2ea58c4f3f5`. The current native method deliberately
uses exact names. These findings explain its exclusions; they do not implement
or qualify implicit alias application or a complete protonation inventory.

The native-only pair is source atom indices **[0, 3427]**, HB2–CB in SER A 438,
distance **1.1150762306 angstrom**. HB2 is the first ATOM record; the rest of that
group occurs later in the unchanged source. An independent actual OpenMM parse
places HB2 in group index 0 and CB in group index 214 despite identical deposited
group labels. Native canonical identity reunites the observed sites. A literal
synthetic guard now fixes the intended native pair inventory with noncontiguous
group records and preserves source coordinates and group membership. This is a
reader-policy difference, not a claim that geometric closeness alone proves
bond order, protonation, stereochemistry or the correctness of every source site.
No external OpenMM defect is asserted or published.

The [pair audit](../../devtools/data/native_pdb_disagreement_audit_304_20261106.json)
retains every differing source pair, labels, coordinates with explicit units,
distances, exact alias resource, installed software origin and parsed group
indices. The combined inference/benchmark-control selection passes **24 tests in
5.31 s**, including that independent inventory guard. An earlier benchmark test
omitted `get_missing_bonds=True` for text input and correctly hit the existing
False-default conflict; the test now declares its requested policy. Product
defaults are unchanged.

### How the benchmark is executed

`devtools/scripts/benchmark_native_pdb_connectivity.py` reuses the existing
isolated-process probe. Three fresh interpreters per input/engine give **45
processes**, **90 conversions** and **15 native H5MSM round trips** for the two
original sources and three synthetic heavy-alanine workloads. Synthetic chains
have analytically specified intra-group and peptide edges; TER boundaries forbid
cross-chain links even when displayed chain labels repeat. Both actual enabled
engines must reproduce those literal inventories. The coordinates are scale
fixtures, not experimental observations or force-field-quality conformers.

```bash
python devtools/scripts/benchmark_native_pdb_connectivity.py \
  molsysmt/data/pdb/181l.pdb <original-1IEP-PDB> \
  --compare-openmm --repetitions 3 --alanine-groups 64 512 2048 \
  --output <benchmark-receipt.json>
```

Use the existing qualified development interpreter and this source on PYTHONPATH.
This Linux run sets OMP_NUM_THREADS, OPENMM_CPU_THREADS, OPENBLAS_NUM_THREADS and
MKL_NUM_THREADS to 1. Processes run serially to bound aggregate memory. Kernel
threading not governed by those variables retains its actual defaults; this is
not a claim of universally single-threaded execution. No environment is created.
Eight tool guards validate literal synthetic graphs, TER constraints, coordinate
preservation, source size/field bounds and statistical summaries.

Cold conversion here means the first call after package imports, including lazy
adapter setup; it excludes interpreter/package startup. Warm conversion reuses
that process's caches after releasing the previous result. Collection is outside
the timer. Conversion RSS is the process high-water mark captured before query
and serialization checks; final RSS includes H5MSM verification for the native
route. Neither metric isolates graph allocations or a single coordinate buffer.
The fresh-process wall measurement includes startup and verification. All raw
observations, stderr summaries, exact graphs, hashes and producer/source context
are retained in the [benchmark receipt](../../devtools/data/native_pdb_benchmark_304_20261106.json).
Three replicates provide descriptive medians/ranges, not a statistical superiority
claim or qualification of arbitrary trajectories/platforms.

### Measured results and implications

Median timings below are seconds; conversion RSS is MiB and native H5MSM size is
MiB. Storage includes native domains and historical evidence, not only edges.

| Input | Atoms | Native bonds | Native cold | Native warm | OpenMM warm | Native conversion RSS | OpenMM conversion RSS | Native H5MSM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Original 181L | 1,441 | 1,322 | 2.226 | 1.147 | 0.291 | 233.2 | 252.9 | 3.071 |
| Original 1IEP | 4,412 | 4,445 | 2.762 | 1.719 | 0.631 | 252.9 | 267.1 | 6.191 |
| Synthetic ALA 64 | 320 | 318 | 1.420 | 0.377 | 0.158 | 218.5 | 246.6 | 0.831 |
| Synthetic ALA 512 | 2,560 | 2,544 | 3.123 | 2.024 | 0.551 | 250.9 | 258.9 | 5.441 |
| Synthetic ALA 2048 | 10,240 | 10,176 | 11.426 | 9.941 | 1.381 | 360.2 | 296.2 | 21.160 |

The native path is **slower on these workloads**. Its complete output includes
candidate/coverage/history evidence that is absent from the OpenMM comparison;
that is a scope distinction, not proof that the overhead is necessary. At 10,240
atoms, native H5MSM write/read medians are **7.207/6.160 s** and final process RSS
is **405.7 MiB**. Source parsing, group assessment and evidence representation
need profiling before attributing the cost to one layer. The two small real
inputs use less conversion high-water RSS natively, while the larger synthetic
input uses more; no blanket memory advantage follows. Keep the existing default
and explicit engine choices. The native method is not a faster replacement claim.

Historical two-conversion measurements remain intact. This probe now explicitly
releases the first result before its second call and records pre-verification
conversion RSS separately; older whole-process RSS is not interchangeable with
the new scoped measurement. No scientific production code or compiled kernel
changes in this benchmark/diagnosis checkpoint.

**Remaining #304 work:** implement/qualify the approved H-name and terminal/group
policies, disulfide composition and bounded unknown-group geometry policy, then
audit all acceptance criteria and integrate the qualified source. The original
edge disagreements and bounded repeated workload measurements are now explained
and retained. Larger structures/trajectory scaling and performance improvements
remain explicit limits; this checkpoint does not certify complete chemistry or
close #304.

## Explicit observed-H name alternatives — 2026-11-06

### What and reference ownership

The approved H-name extension now offers two explicit method choices through
the existing public tools:

- `build.get_covalent_bond_candidates(method='observed_hydrogen_alias_consensus')`
  inspects local observed-H parent evidence.
- `build.infer_covalent_bonds(method='supported_group_templates_with_hydrogen_aliases')`
  composes that report with the unchanged heavy-template and peptide tools.

Defaults, signatures and the PDB native reader's exact-name policy are unchanged.
Use an explicit-only read followed by the standalone build tool when selecting
this alternative. Both source atom names and group naming declarations survive;
this is not an implicit normalization or preparation operation.

A reproducible offline generator derives only canonical-protein H-name
alternatives from the inspected OpenMM PDB name resource. The unchanged primary
XML, source commit `ba0aa236ac4d07241382869604c4d2ea58c4f3f5`, SHA-256
`740c56071d092940ce386074447ce88ed2b07c77d0065f2bd0d1087e9ef76969`, MIT notice and
generated JSON are bundled. There are twenty canonical group labels, without
the source resource's group-name replacements or heavy-atom aliases. In
particular, CCD HID is not reinterpreted as histidine; declared Amber HID keeps
its own exact chemical reference. The H-parent helper now forwards the already
resolved template naming declaration instead of losing that context.

This is an adaptation using OpenMM **reference data**, not execution of OpenMM
or a claim that OpenMM invented local parent consensus. Optional Ackredit credits
the actually consulted dataset once per operation, including reused references
inside enclosing captures. Detached bibliography, original/derived hashes and
source revision accompany results/history regardless of provider availability.
The data helper imports no engine or Ackredit at module import time.

### How the evidence is decided

The existing whole-group prerequisites, heavy-element checks, stored H
assignments and incident-edge conflict checks still apply. The literal H name
and its declared alternative are examined against all compatible reference
variants. Every match must agree on one known, present heavy parent. There is no
nearest-atom guess, first-variant selection, H addition or coordinate placement.
Unknown names and conflicting partners remain unassessed.

Alias-mode CSR name arrays retain the strings examined per source H and a
Boolean alias mask. These fields are not added to default exact-mode history,
avoiding unnecessary small-array storage in the existing profile. Missing names
do not become literal "None" labels. Alias-assisted whole inventories stay
unassessed: local parent agreement is not a joint/stereochemical assignment of
H roles, terminal-state choice, valence or protonation certification. The new
application profile retains the same source/selected-state ownership,
interaction invalidation, unknown orders and typed historical persistence.

### Executed evidence

Nine baseline cases reject the previously unsupported named methods. Receiving
now passes **276 affected inference/argument/doctest cases in 18.84 s**, with
twelve workers. The new data/alias modules supply eighteen cases covering
literal positive/negative parents, source selection/ownership, H5MSM history,
stored conflicts, contradictory reference parents, declared naming context,
missing labels, independent states/nondefault units, optional provider absence/
failure, real repeated Ackredit captures, empty lookup attribution and exact
offline regeneration. A development-only warning-class import in the first
failure guard was corrected; no public diagnostic export was added for that test.

The same **18 cases pass in 6.11 s** with published ArgDigest 0.14.0, DepDigest
0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads, using current other
dependencies. This is a four-provider source floor profile, not a clean installed
runtime matrix. Documentation/source boundaries pass **1,072 cases in 43.35 s**;
retained warnings are not suppressed. The revised docstrings execute and the
Foundations, both Toolbox pages, Cookbook and course agree. Original course
code, outputs and metadata remain unchanged.

An unchanged-original 1IEP probe with OpenMM imports blocked yields **4,470
edges**, adding exactly the earlier 25 OpenMM-only H-parent pairs to the exact
native 4,445. No exact-native pair is lost; the explained noncontiguous-group
HB2–CB pair remains. Names, stable atom rows and physical coordinates are
unchanged. This does not make OpenMM parity a target or certify whole-source
chemistry. See the [receiving receipt](../../devtools/data/hydrogen_alias_receiving_304_20261106.json)
for exact source/assets, provider origins, raw JUnit results and the original
source probe. No dependency floor, compiled backend or H5MSM schema changes.

**#304 remains partial.** Complete terminal/cap and additional-group policies,
disulfide composition, the bounded unknown-group geometry policy and the final
acceptance/integration audit before closing. This H-parent extension does not
resolve those remaining chemical questions or authorize a release.

## Declared local terminal-cap references — 2026-11-06

### What and shared ownership

The existing public coverage/candidate/application tools now reuse the owning
`element.group.terminal_capping.get_group_db()` catalogue for **ACE, NME, NHE and
NH2**. No new parser-specific chemistry table, public function, dependency or
compiled routine is introduced. The private adapter supplies reference layouts
to the existing heavy-inventory, stored-connectivity and per-H consensus audits.
The public peptide tool consumes the same audited identity rather than inferring
cap roles from an atom's element or a new hard-coded list.

Only an explicit stored **amber or legacy** group naming declaration admits
this local cap interpretation. Bare labels, CCD and sequence declarations do
not authorize the historical cap catalogue. Every compatible layout must agree
on one heavy-name inventory. In particular, NME containing N but no observed
methyl name cannot choose the C versus CH3 layout by taking the first variant.
An ACE with one missing heavy atom can retain supported partial pairs while
reporting blocked endpoint names. Duplicate/unexpected names, incompatible or
unknown heavy elements and contradictory stored chemistry retain their existing
exclusions. No label, coordinate or stored assignment is repaired implicitly.

The N-terminal catalogue supplies C and the C-terminal catalogue supplies N for
amide candidates; the identity retains those `backbone_roles`. NME's methyl C
cannot become an outgoing peptide carbon. Both public peptide policies retain
their existing chain/TER, geometry, alternate-site, stored-edge and selection
criteria. The unique policy still checks full-source named competitors before
output filtering, including endpoints that are unselected or not chemically
qualified. Neither policy assigns biological termini or a complete terminal
chemical state. Without coordinates, only eligible intra-group reference pairs
can be proposed or applied.

Observed cap H atoms use the same exact-name, all-matching-parent and stored-H
assignment checks as other supported groups. They do not consult or credit the
protein H-alias dataset. A partial or mixed H inventory is not complete
protonation, H-role or valence certification. No caps or H atoms are added.

The operation retains actual hashes of the existing n_terminal/c_terminal JSON
resources and original variant indices. Optional Ackredit credits the inspected
historical catalogue as **data**, not OpenMM execution or an independently
validated published parameterization. The catalogue's external original sources
and bond orders remain explicitly unassessed. The coverage, covalent-candidate,
peptide-candidate and application reports now record **rule_version=2** for this
new scope; dictionary schema identifiers remain at version 1, and historical
reports are not rewritten. H5MSM 0.5 needs no schema change for these typed values.

### Executed evidence

The final **321-case selection passes in 20.01 s** with twelve workers and
Pytest Receptor. It includes **41 new cap controls**, the affected heavy/H,
coverage, peptide and inference suites, PDB policies, reference-data guards,
native history, generated argument contracts and four public doctest modules.
The new controls use literal independent atom pairs and analytic C-N geometry,
both methyl layouts, NHE/NH2 attachment, explicit naming exclusions, duplicate/
element/stored-field conflicts, an unselected competing group, original-axis
selections, TER and alternate PDB sites with OpenMM imports blocked, absent
structures, independent states/all-structure retention, non-default pm output,
unchanged stable topology and coordinates, H5MSM typed history and repeated real
Ackredit captures. Test selections overlap and are not a full source matrix.

The final directed four-provider-floor profile passes **45 cases in 9.06 s**
with published ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit
0.9.0 payloads. Each actual import origin/hash is checked. Other dependencies
come from the existing development environment; this does not qualify a clean
installed runtime. SMonitor runtime remains active while its incompatible
development pytest plugin is disabled in that floor profile.

Documentation/source-boundary/schema/docstring tests pass **1,091 cases in
57.34 s**, with existing warnings retained. Foundations, four Toolbox pages,
Cookbook, the course and docstrings describe the same limits. A final Markdown
paragraph separation changes no course executable cell, output, ID, metadata or
cell inventory. Ruff, import-laziness/dependency checks, 247 public docstrings,
API registry and signature stability against a16d289ec also pass.
The final notebook/source-boundary selection passes another **1,004 overlapping
cases in 12.94 s** after that final paragraph correction. Developer-guide and
generated-index checks pass without changing report lifecycle status.

The initial 23-control development run had 22 failures; three negative controls
expected the coverage auditor's reason rather than the public candidate reason
and were corrected. Those three are test defects, not library regressions.
The expanded run had one further fixture error: a purported competitor was in
the target's own group and was correctly excluded by the existing method.
Moving that competitor to a different source group fixes the intended control;
the production competition rule is unchanged. The receipt retains these
development failures rather than presenting them as passing runs.

The [receiving receipt](../../devtools/data/terminal_cap_receiving_304_20261106.json)
records implementation/data hashes, the JUnit results, provider origins and
unchanged-original probes. Original 181L/1IEP source bytes are retained; their
disabled/native graph, stable-axis and coordinate digests match the earlier
benchmark exactly. This is a regression observation, not a new speed/memory claim.

### Remaining before #304 closure

The current qualified PDB path is explicit-only reading, reviewed naming
declaration on the native topology, then standalone inference. Delivering a
conversion naming request before native PDB inference is still part of the
remaining reader/context audit; a late declaration must not be mistaken for an
already context-aware calculation. No source convention is inferred from cap
labels and existing reader-engine defaults remain unchanged.

Additional supported-group and disulfide policies, bounded unknown-group
geometry and their adversarial acceptance controls remain to be settled and
qualified. Complete terminal/protonation-state assignment is not offered by this
cap reference lookup. Final source qualification and owner integration remain
pending; #304 stays partial and no release is authorized.

## PDB source naming before reconstruction — 2026-11-06

### What and shared boundaries

All six PDB file/text/handler conversions to MolSys/Topology now accept the
existing public source declaration as keyword-only `from_naming_scheme=None`.
Every previous positional argument and form-specific connectivity default is
preserved. The declaration reaches fresh Topology before group classification,
native templates and source-structure-0 inference. No convention is guessed and
no label is renamed. The undeclared reserved-small-molecule backbone heuristic
cannot overwrite an explicit CCD interpretation: HID under CCD remains a small
molecule, while the same label under Amber is an amino acid. This is bounded
label interpretation, not chemical validation of the observed atom inventory.

The generic naming dispatcher already discovers readers supporting this
keyword, so their science is not duplicated in basic.convert. Numeric/all output
selection retains the direct reader route. A semantic selection instead uses
interpreted native inventory before selecting its source atom population.
The shared helper no longer truncates atom_indices during that first read;
conflicting explicit indices and a semantic selector are refused before reading
or inference. This shared fix also receives the existing GRO/native naming paths.

Context-aware name-only projection requests topology inventory without implicit
bond reconstruction when that reader exposes a connectivity option. An explicit
engine or inference request retains its normal meaning. Ordinary MolSys reader
defaults are unchanged; notably text-to-MolSys still defaults to disabled
inference. These name-only queries neither require graph reconstruction nor
produce a chemical assessment.

Source naming admission for external OpenMM inference reuses the existing
preparation guard. Reviewed contextual labels and incompatible cap declarations
need an external naming adapter; they are not silently interpreted by another
vocabulary. Explicit OpenMM requests raise before provider execution. The legacy
optional route warns, retains the typed failure cause and preserves declared
edges. Undeclared input keeps its previous policy. This is not a native fallback.
Reader inference examines the full source before output extraction: selecting
only an ordinary group does not conceal another unsupported input label from
that external operation. Ordinary preparation tools retain their own selected
group scopes.

The first reader report now retains scalar `source_naming_scheme` as an original
operation input. Later metadata changes do not rewrite it. Existing typed history
and H5MSM 0.5 preserve it without a schema change or coordinate snapshot. Pure
Topology projection retains stable inventory/declarations, not ChemicalStates
bonds or history; one stale converter doctest that still queried those bonds is
corrected to inspect the 1,441 source atoms instead.

### Executed evidence

The final source selection passes **543 cases in 25.30 s**, with twelve workers
and Pytest Receptor. It includes **60 new PDB context controls**, all affected
candidate/inference/name/preparation modules, GRO/MDTraj source context,
conversion-fidelity and generated argument contracts, plus public doctests.
Literal checks cover all six reader/projection routes, all three source kinds,
undeclared/Amber/CCD classification, semantic selections, pre-inference naming,
unchanged positions/Boolean defaults, bad-context diagnostics, caller-owned
handler reuse and lifetime, original file bytes, nonconsecutive structures,
atom maps and non-default pm/fs policy, immutable original history and H5MSM.
Real native and OpenMM engines both match the independent nine-edge capped
peptide control; injected engine cases qualify dispatch only. No whole-profile
scientific equivalence is inferred from that small control.

The final directed profile passes **64 cases in 7.70 s** with published
ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads;
actual import origins and content hashes are checked. Other development
dependencies remain reused. Only SMonitor's incompatible development pytest
plugin is disabled there; its runtime diagnostics remain active. This does not
qualify an all-dependency-floor or clean installed environment.

Documentation receiving passes **1,091 cases in 47.88 s**, with warnings retained.
Foundations, the build tutorial, three form pages, Cookbook, course and public
docstrings agree. All four edited notebooks retain every code cell, output,
cell ID, metadata value and cell count. The source registry records the six
intentional keyword-only additions; independent guards retain old positions
and exact Boolean defaults. The generated converter-argument union is already
correct and passes unchanged. Dependency/import-laziness, 247 public docstrings,
API registry/signatures and Ruff checks pass.

The final notebook/source-boundary follow-up passes **1,004 overlapping cases in
13.86 s** after the last narrative clarification. Developer-guide and generated
index checks pass with the issue still partial.

The [receiving receipt](../../devtools/data/pdb_naming_context_receiving_304_20261106.json)
retains exact sources, runtime/floor provider origins and all failed development
runs. The initial draft used an unavailable root Topology import; the supported
native namespace fixes that test defect. The corrected baseline has 24 failures
and five passes. Another six initial assertions expected ArgumentError instead
of its distinct ArgumentChoiceError diagnostic; those tests now require the
correct class and argument. One affected-run failure found the real stale
Topology doctest described above. No native graph or validation was weakened to
make those tests pass.

Both unchanged original PDBs retain exact disabled/native/OpenMM graph,
atom-axis and coordinate digests against the retained benchmark. Counts remain
13/1,322/1,322 for 181L and 0/4,445/4,469 for 1IEP. The explained native/OpenMM
disagreements remain. These isolated conversion observations are regression
receiving, not a new speed/memory claim.

### Remaining scope

This closes the direct PDB naming-context prerequisite, not #304 as a whole.
Additional-group/disulfide/unknown-geometry policies and their acceptance controls,
the final combined-source gate and owner integration remain. Broader source/
composite producer receiving belongs to the staged #549 rollout; direct-reader
tests do not certify every multi-provider conversion. The issue stays partial,
and no release or main integration is claimed by this checkpoint.


## Final native policy boundaries — 2026-11-06

### Decision and actual behavior

The offered native composition retains stored disulfide and metal-coordination
edges without inferring additional ones. Geometry for groups without an exact
supported template is disabled. These are explicit boundaries of this profile,
not a promise to reconstruct arbitrary chemistry. The #304 acceptance allows
unsupported chemistry to remain reported; a universal distance cutoff would not
establish covalency, oxidation state, coordination or chemical completeness.
The existing public disulfide detector separately returns geometric candidates,
including competing partners, without applying them. Its observations do not
choose a disulfide matching. Existing source declarations and their conflicts
remain stored; missing/ambiguous/symmetry-specific declarations are not replaced
with a different nearby atom pair.

The application report now records these fixed choices in
`excluded_inference_policies`, with an int64 `unsupported_group_indices` array
on the original selected source group axis. This additive metadata makes
existing behavior inspectable; candidate pairs, scientific rule_version=2,
function signatures/defaults, dictionary schema versions and H5MSM 0.5 are
unchanged. A selector limits additions and the exclusion report, not the source
system or retained edges. Historical indices retain their original operation
scope after extraction. Returned report arrays are detached from stored history.

The four reviewed MSE/SEP/TPO/MLY references retain their own literal heavy
connectivity; sequence parents never replace them. ACE/NME/NHE/NH2 keep the
previously received explicit naming and layout limits. Water, ions, arbitrary
ligands and unreviewed modified groups remain unsupported and unassessed by
this profile. Other H, order, valence, terminal and protonation exclusions remain
with their owning candidate reports. No chemical store, geometry kernel,
optional dependency or scientific reference is introduced in this checkpoint.
Existing template attribution remains with the tools actually consulted.

### Executed receiving

The new module `tests/build/test_covalent_inference_policy_boundaries.py` has
54 controls. It checks literal complete returned edge inventories through native,
PDB file/text and caller-owned handler inputs for both existing compositions;
three close sulfur sites; single/competing declarations; explicit LINK/CONECT;
water/ligand/metal/unknown-group proximity; all four curated modified groups;
unsupported symmetry, absent endpoints and malformed SSBOND labels; selected
and empty atom populations; retained dative typing; nonfinite excluded-group
coordinates; source identities, graph and coordinates; pm/fs policy; and detached
historical policy arrays through extraction and H5MSM. These assertions check
the graph, not merely output labels. No OpenMM import is permitted in native
composition controls.

The completed affected selection passes **227 cases in 16.43 s** with twelve
workers and Pytest Receptor, retaining the one H5MSM 0.4 deprecation warning.
It includes native application, PDB policy/declarations/context, cap and
independent disulfide-detector controls plus the public inference doctest.
The final published four-provider-floor selection passes **55 cases in 9.53 s**
with four workers. It uses the existing ArgDigest 0.14.0, DepDigest 0.15.1,
SMonitor 0.16.0 and Ackredit 0.9.0 payload routes; other development dependencies
remain reused and only the incompatible development pytest plugin is disabled.
This is source receiving, not a clean installed or all-dependency-floor claim.

Documentation receiving passes **1,091 cases in 48.66 s**, with warnings retained.
The docstring, Foundations, Toolbox, Cookbook and course explain the same
policies. Both edited notebooks preserve every executable cell, output, ID,
metadata value and cell count. Ruff lint/formatting over the whole checkout,
247 public docstrings, dependencies/import laziness, generated arguments and
API registry/signature guards pass. The aggregate fast release gate also passes
14/14 checks; it explicitly does not run the full scientific/matrix/installed
gates. This introduces no signature waiver.

Both unchanged original PDBs pass fresh native child-process receiving with
OpenMM imports blocked, two conversions per input and H5MSM round trips.
Graphs, stable atom axes and physical coordinates match the earlier digests
exactly: 1,322 bonds for 181L and 4,445 for original 1IEP. Individual timings and
RSS are retained observations; no new statistical benchmark or improvement is
claimed. The existing measured disadvantages remain part of this decision.

The initial 44-case policy run had 43 missing-field failures and one pass; its
literal graph assertions already passed. These are not 43 repaired chemistry
bugs. The first larger command accidentally included the legacy network-only
5XJH download test and was interrupted after 227 passes; it is not a completed
passing gate. The final command explicitly excludes that one network case and
completes all 227 selected cases. Ruff's first run found an import-order error
in the new test; sorting imports corrects it, and final Ruff plus the final
55-case profile pass. The
[receiving receipt](../../devtools/data/pdb_policy_boundaries_receiving_304_20261106.json)
retains these unsuccessful runs as well as the accepted results and exact hashes.

### Final acceptance map and remaining gate

| Requirement | Delivered boundary and evidence |
| --- | --- |
| Explicit-only/native/OpenMM policies | Six PDB routes, typed failure/absence outcomes and the existing engine/default policy guards; CIF/BCIF disabled-inference correction retained. |
| Exact local chemistry | Standard/curated heavy templates, exact or opt-in alias H-parent consensus, naming-scoped caps; no sequence-parent substitution. |
| Polymer context | Same-chain/TER/insertion/alternate controls, full-source competitor checks and explicitly selected source structure/state. |
| Declared and excluded connectivity | Typed CONECT/LINK/SSBOND diagnostics, preserved conflicts, no proximity-derived disulfide/coordination or unknown-group fallback; new boundary controls above. |
| Original truth and ownership | Exact 181L/1IEP graph/axis/coordinate regressions, retained disagreements, analytic literal pairs, non-default units, state/history and failure/source preservation. |
| Workload and persistence | Retained 45-process benchmark, explicit slower/larger cases, typed H5MSM graph/history round trips and documented eager-memory limits. |
| Public lifecycle | Docstrings/doctests, Foundations, Toolbox, Cookbook, course and maintained forms contract agree. |

The remaining work is the **final combined-source/full-matrix gate, owner
integration and documented closeout**. This matrix records implemented bounds;
it does not itself certify those pending gates or a package/release. #304 stays
partial until they finish, and the other fourteen issues retain the authorized
order. Do not add a new universal chemistry implementation merely to remove an
honest unsupported category, or silently drop a demonstrated defect from the
offered profile.

## Exact-source gate receiving — 2026-11-06

The source remains frozen at **56b37c983253e8f93cda6333703df2b3a626a238**
on `dev/ordered-stabilization-304-20261106`. Manual full-source run
[42205436569](https://github.com/uibcdf/molsysmt/actions/runs/42205436569),
attempt 1, uses controlled MolSysViewer
**42234de839ed047016f8f241ea5eb717cfeb07be**. The controlled wheel and all
four Linux Python 3.11–3.14 jobs and macOS Python 3.12/3.13 succeed. The two
remaining macOS jobs are queued at this inspection; the complete gate is pending.
Do not restart this active run
merely because an observation times out. The separate #593 course correction
is prepared on a descendant branch and is not silently included in these
source results.

### Received artifacts and actual test accounting

The [partial receiving receipt](../../devtools/data/native_pdb_full_source_receiving_304_20261106.json)
retains the native artifact metadata, exact run/head, SHA-256, size, scientific
certificates and selected test-accounting facts. All thirteen received archives
match their independently checked GitHub digest and size. Ephemeral download
URLs and raw event logs are not committed. The six scientific certificates
each qualify the expected 61 registry selectors, expanded to 83 actual cases,
with no omissions or failures and clean tracked source. Their
`release_eligible` field is a certificate predicate, not authorization to
publish a release.

Each of the four full Linux suites has **29,253 passes, zero failures/errors**
and 118 JUnit skips. The public `pytest_receptor.read_artifact` API verifies
complete event evidence, valid integrity, a complete final record and exit 0.
Its counts are 29,370 executed items and 117 item skips; JUnit has 29,371
testcases because it also represents the genuine collection-skipped
`tests.build.solvate.test_scientific_attribution` module as one virtual case.
Both views and the exact collection record are retained rather than forcing
their totals to agree. All 83 registered scientific cases are also present
and passing in the full suites.

Eleven directed PDB, CIF and native connectivity/coverage modules contain
**432 passing cases per Linux cell** and three optional Ackredit-presence
omissions. Each omission is the exact absent-dependency condition; none masks
a connectivity failure. Those same three controls execute separately on the
frozen source with the existing Linux/Python 3.14 interpreter and published
ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads:
**3 passed, no omissions**. Other optional full-suite omissions remain visible
in the receipt. This does not establish installed-Ackredit receiving in every
hosted cell or a clean installed MolSysMT/Viewer pair.

The macOS Python 3.12 and 3.13 full artifacts independently pass the same
archive, receptor-integrity and scientific-selector checks. Each records
29,252 passing cases, 119 JUnit skips and 118 receptor item skips, including
the same virtual collection-skipped module. The one extra platform omission is
`tests/build/get_missing_bonds/test_get_missing_bonds.py::test_get_missing_bonds_molsysmt_MolSys_1`,
explicitly restricted to Linux. All 83 scientific and 432 directed cases pass.
Event-cache filenames include platform and Python minor, and original archive
digests are rechecked before extraction; a cached Linux event log cannot stand
in for a macOS result.

The initial receiving comparison incorrectly required identical JUnit and
executed-item totals, and then required zero skips even for the optional
Ackredit controls. Investigation established the collection record and genuine
dependency absences above. The comparison was corrected to account for those
exact observations; no library implementation or scientific test was changed
to make the comparison pass. The receipt preserves that limitation and the
receiving-script digest. This observation is separate from the older failed
frozen PR gate caused by the stale generated argument table.

### Coverage reads the returned graph

The [original-graph receiving receipt](../../devtools/data/native_pdb_actual_graph_receiving_304_20261106.json)
records an additional fresh audit of both unchanged original PDBs on this
tracked-clean source, with OpenMM imports blocked. For 181L, explicit-only
input has 13 stored bonds, zero assessed groups, 162 incomplete and 140
unassessed; native inference returns 1,322 bonds, 162 assessed, zero incomplete
and the same 140 unassessed groups. Original 1IEP changes from zero bonds and
274 incomplete groups to 4,445 bonds and 274 assessed groups, with zero
incomplete or unassessed groups. In every case the readiness report's stored
pair inventory equals the graph actually returned.

Removing one literal N–CA pair on a detached native copy through the public
ChemicalStates tool makes exactly its MET group incomplete: pair `[0, 1]`
for 181L, `[1, 5]` for 1IEP. The audit reports exactly that missing pair and
leaves each original source graph unchanged. Thus the assessment observes
current stored edges rather than treating a previously matched template as
permanent completeness. An assessed heavy-template group does not imply
universal valence, protonation, hydrogen placement or mechanics readiness.

### Still pending

Finish the two queued macOS jobs, inspect their actual evidence, integrate the
qualified owner source and perform documented closeout. The issue remains
partial; the ordered fifteen-issue objective is unchanged. These receipts
do not authorize tags, Releases, package promotion or a new source matrix.
