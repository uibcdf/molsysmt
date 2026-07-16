# Chemical-State Adapter Fidelity Audit

**Status:** fixed pre-1.0 priority adapter scope complete

**Recorded:** 2026-07-15

**Implementation update:** the core Wave 1 boundary migration and normalized
Wave 2 storage are complete. RDKit and OpenFF now populate their accepted rich
atom and bond subset independently, including isotope on RDKit input. MDTraj
and OpenMM preserve formal charge, compatible integral order, and aromaticity
for their reduced model. Dispatcher preflight reports and strict rejection are
implemented for the audited canonical fields. MDAnalysis and ParmEd now map
their supported rich inbound semantics. mmCIF now preserves explicit and
inferred bond semantics conservatively. PDB/PDBFixer declare their reduced
endpoint behavior, and NetworkX emits the canonical attribute graph contract.

MMTF and MSMPK were removed before 1.0 on 2026-07-16. They have no compatibility
contract and are intentionally outside the remaining adapter matrix. BinaryCIF
or mmCIF replaces MMTF exchange; H5MSM replaces MSMPK persistence.

## Purpose

This audit translates the accepted chemical-state contract into concrete
conversion work. It distinguishes native-storage dependencies from legitimate
third-party APIs, records which chemical information each source can provide,
what MolSysMT currently retains, and which losses must become explicit.

External implementations were inspected only to understand their object
contracts and semantics. No implementation is to be copied. Every mapping must
be rechecked against the supported dependency version when it is implemented.
This document is subordinate to the
[Chemical State v1 Executable Contract](chemical_state_v1_executable_contract.md).

## Audit scope and evidence

The inspected local dependency versions were:

| Dependency | Inspected version |
|---|---:|
| MDAnalysis | 2.10.0 |
| MDTraj | 1.11.1 |
| OpenMM | 8.4.0 |
| OpenFF Toolkit | 0.18.0 |
| ParmEd | 4.3.1 |
| RDKit | 2025.3.6 |

These versions document the evidence boundary; they are not proposed minimum
versions.

The raw search found 23 form modules plus the authoritative native topology
implementation. This is not 23 instances of native-storage debt. Most inbound
adapters correctly access an external object's public bond collection, for
example `MDAnalysis.Topology.bonds`, `mdtraj.Topology.bonds`, or
`openmm.app.Topology.bonds()`. Such accesses must remain. Only access to a
MolSysMT native bond table bypasses the chemical-state seam.

## Classification of remaining access sites

### Native-storage dependencies

The following paths currently read or write MolSysMT's native bond table
directly and must be routed through the reference-state seam before the physical
bond schema changes:

- inbound endpoint construction from GRO and mmCIF;
- inbound RDKit and OpenFF construction of legacy `order` and `type` columns;
- native Topology output to MDTraj, OpenMM, and NetworkX;
- native MolSys output to PDB text and PDBFixer.

### Legitimate external bond APIs

The following accesses describe the source or target library and are not native
storage debt:

- MDAnalysis Topology and Universe bond attributes;
- MDTraj Topology extraction, getters, and inbound conversion;
- OpenMM Topology copy, extraction, getters, and inbound conversion;
- ParmEd Structure bonds;
- PDBFixer/OpenMM bond iteration after target construction.

They still require semantic fidelity work where metadata is ignored, but they
must not be mechanically replaced merely because their spelling contains
`.bonds`.

## Fidelity vocabulary

Every implemented conversion path must classify its result as:

1. **Exact:** every in-scope canonical semantic field and its missingness are
   preserved.
2. **Equivalent:** the target encoding differs, but the accepted chemical
   meaning can be reconstructed under a documented equivalence rule.
3. **Lossy:** supported information is retained and every unsupported or
   ambiguous field appears in a structured loss report.
4. **Rejected:** strict policy or malformed input prevents conversion with a
   deterministic diagnostic.

Permissive conversion never means silent loss. Endpoint preservation alone is
not exact when the source also supplies order, aromaticity, stereochemistry,
direction, evidence, or formal charge.

## Canonical mapping constraints

- Integral formal order maps only to `bond_order`.
- Fractional or partial order maps only to `fractional_bond_order`.
- Aromaticity and conjugation map independently to their boolean fields.
- Chemical relationship kind maps to the small canonical `bond_type`
  vocabulary; a force-field parameter class never does.
- Semantic stereochemistry must not be replaced by toolkit traversal tags.
- Donor/acceptor direction survives canonical endpoint sorting through explicit
  directional fields.
- Inferred or guessed connectivity preserves `bond_evidence` and must not be
  reported as explicit.
- Connectivity assembled from partial records, templates, or inference is not
  declared complete without evidence.
- Source-specific reverse-conversion metadata may be retained as namespaced
  metadata but cannot masquerade as a canonical field.
- Numeric source IDs become string labels and are not made unique.

## Adapter-family findings

### RDKit Mol

RDKit can provide atom formal charge, isotope, aromaticity, radical electrons,
implicit-hydrogen policy and count, and chiral state. Its bonds expose rich
order/type, aromaticity, conjugation, direction, stereochemistry, and stereo
reference atoms.

The implemented inbound adapter now preserves formal charge, isotope,
aromaticity, radicals, implicit-hydrogen count and policy, and semantic atom
stereochemistry. It maps integral and fractional bond order independently from
type, aromaticity, conjugation, semantic stereochemistry and reference atoms,
and dative donor/acceptor direction. Unsupported semantics remain reportable
rather than being collapsed into legacy strings.

This is a rich first-wave adapter. Populate independent canonical fields. Map
traversal-specific tags only when a documented semantic mapping exists;
otherwise retain namespaced metadata or report loss. Dative direction uses
explicit donor and acceptor indices. The expected result is exact for the
accepted canonical subset and equivalent or explicitly lossy beyond it.

### OpenFF Molecule

OpenFF independently exposes atom formal charge, aromaticity, stereochemistry,
integral bond order, aromaticity, fractional order, and bond stereochemistry.
The implemented inbound adapter preserves formal charge, atom aromaticity and
stereochemistry, integral and fractional bond order, bond aromaticity, and
covalent relationship type independently. OpenFF E/Z labels currently produce
an explicit adapter limitation because the inspected object does not expose the
two reference atoms required by the native stereo contract.

The target maps each concept independently and preserves missingness instead of
guessing a single bond. It must not infer chemical `bond_type` from numeric
order. The accepted subset should become exact after normalized storage exists.

### MDAnalysis Topology and Universe

MDAnalysis connection attributes may carry endpoints, optional type, guessed
evidence, and optional order; availability is instance-dependent. MolSysMT
currently imports endpoints only.

The target preserves compatible numeric order and maps per-bond guessed status
to `bond_evidence`. A source type is chemical only when documented for that
instance; otherwise it is namespaced metadata or a reported loss. Mixed
explicit and guessed arrays remain mixed. The expected result is exact for
endpoints, compatible orders, and evidence, with opaque types explicitly lossy.

### ParmEd Structure

A ParmEd bond may carry numeric `order`, an optional qualitative chemical label,
and a `type` object holding molecular-mechanics parameters such as force
constant and equilibrium length. MolSysMT currently imports endpoints only.

The target preserves compatible chemical order, evaluates qualitative labels
against the canonical vocabulary, and routes parameter data to
`MolecularMechanics` or reports its omission. A ParmEd parameter object never
becomes `bond_type`. Chemistry can become exact before mechanics does.

### MDTraj Topology

MDTraj bonds carry optional integer order and a small type vocabulary including
single, double, triple, aromatic, and amide. Both implemented directions now
preserve endpoints, compatible integral order, formal charge when exposed, and
aromaticity for the documented reduced subset.

Inbound conversion preserves orders 1--3 and maps aromaticity independently.
Amide is a source annotation or documented equivalence, not a canonical
chemical relationship kind. Outbound conversion exports the supported subset;
strict mode rejects richer semantics and permissive mode reports every dropped
fractional order, direction, stereo, evidence, or unsupported kind. Common
cases can be exact/equivalent; richer states are lossy or rejected.

### OpenMM Topology

OpenMM bonds carry optional order and a compact type vocabulary similar to
MDTraj. OpenMM atoms also carry formal charge in the inspected version. This is
separate from OpenMM System mechanics. Both implemented directions now preserve
formal charge, compatible integral order, and aromaticity for the documented
reduced subset; inferred connectivity is marked inferred and partial.

Inbound conversion should preserve formal charge, compatible integral order,
and documented aromatic/amide equivalence. Outbound conversion exports the
supported atom/bond subset and reports or rejects the rest. The reduced subset
can be exact/equivalent; rich states are lossy or rejected.

### mmCIF DataContainer

The adapter combines `chem_comp_bond` template edges, programmatic polymer
links, `struct_conn` records classified as covalent, and missing-bond inference.
It preserves available order, aromaticity, conjugation, and explicit versus
inferred evidence per edge. Explicit conflicts fail closed to unknown metadata
and partial completeness. mmCIF structural connections can also describe
non-covalent relationships, which do not form components by default. Only covalent
relationships participate in default component derivation. Generated polymer
links and fallback bonds carry inferred evidence. Connectivity remains
`partial` unless completeness is justified for the item. Standard reconstruction
may be equivalent; ambiguous structural relationships are lossy or rejected.

### GRO input

GRO primarily supplies atom inventory and coordinates, not a rich chemical
graph. MolSysMT currently derives endpoints through group knowledge and
missing-bond machinery but stores them without qualification.

The target routes endpoints through the state seam, marks derived edges as
inferred, and uses conservative completeness. This is equivalent only under an
explicit inference policy, never an exact source-chemistry conversion.

### PDB text and PDBFixer

PDB `CONECT` preserves endpoints but is not a general carrier for the canonical
state. PDBFixer uses OpenMM Topology and may reconstruct connectivity. Current
MolSysMT output ignores rich fields.

The implemented target reads through the state seam. Strict PDB output rejects unsupported
in-scope semantics; permissive output writes endpoints and reports losses.
PDBFixer comparison must use the actual output atom mapping rather than assume
identity after a subset or reconstruction. Only documented endpoint-only input
can be exact.

### NetworkX Graph

NetworkX permits arbitrary edge attributes. The implemented public conversion
uses the documented `canonical_attribute_graph_v1` contract: nodes carry stable
atom and available chemical-atom attributes; edges carry all available
canonical bond attributes; graph metadata carries completeness and evidence.
Subsets remap through native extraction, and absent attributes are omitted
rather than fabricated.

### Legacy PyTraj paths discovered after the initial search

The initial `.bonds` search did not find two accesses using the obsolete name
`bonds_dataframe`:

- native Topology to PyTraj Topology;
- PyTraj Topology to native Topology.

These are not isolated bond-seam substitutions. The PyTraj converters also use
obsolete `atoms_dataframe` layout assumptions and one undefined variable; the
inbound converter imports a retired module path and calls retired topology
rebuilders. Editing only the bond lines would leave each path falsely appearing
repaired.

The installed PyTraj 2.0.6 API and the upstream 2.0.x source were inspected. Its
public wrapper represents atoms, elemental identity, residues, original integer
residue numbers, masses, partial charges, and bond endpoints. It does not expose
a structured chain identifier in the installed version; `Atom.chain` is an
alias for covalent molecule number and must not be reinterpreted as a chain.

The declared bidirectional conversion is now rehabilitated for this reduced
contract. It preserves endpoints, atom names and elements, group names and
compatible integer IDs, supports subsets, and pipes multi-attribute reads
through native Topology. It no longer maps force-field atom type to elemental
`atom_type` or advertises unavailable chain and bond-order/type attributes.
Atom source IDs, non-integer group labels, chains, and rich bond metadata remain
explicit target limitations for the future conversion report.

### PDBFixer known-empty limitation confirmed by execution

PDBFixer reconstructs standard-residue bonds while parsing PDB text even when
the source contains a known-empty bond table and the text has no `CONECT`
records. Therefore the current target cannot claim known-empty exactness. The
adapter must not mutate OpenMM private storage merely to force that result.
This case belongs to Wave 4 strict/reduced conversion policy and must produce an
equivalence/loss record unless a supported public construction path can preserve
the empty graph.

## Required conversion policy

- `strict=True` rejects any in-scope source semantic field that the target
  cannot represent.
- Permissive conversion completes only with a structured loss report that the
  caller can request or inspect.
- Missing source information is not a conversion loss; discarding information
  actually supplied by the source is.
- Warnings are not a substitute for machine-readable conversion status.
- Direct converter functions follow the central `convert` policy rather than
  inventing incompatible local meanings of `strict`.

## Implementation order

### Wave 1: close native-storage boundaries

1. Route MDTraj, OpenMM, NetworkX, PDB text, and PDBFixer output through the
   resolved chemical-state seam.
2. Route GRO and mmCIF endpoint construction through the seam.
3. Preserve present endpoint behavior; do not claim rich fidelity yet.
4. Test zero state, one state, ambiguous state, known-empty, and subset behavior.

The core paths listed above now satisfy these boundary requirements. PDBFixer
known-empty reconstruction is a confirmed target limitation, not silently
classified as exact. PyTraj rehabilitation is complete for its documented
reduced model.

### Wave 2: normalized private bond-state storage

**Implementation status:** complete for native storage and lifecycle.

1. Implement canonical nullable dtypes and independent fields.
2. Keep temporary translating facades for legacy `order` and `type`, without
   duplicate canonical ownership.
3. Do not reinterpret legacy `"aromatic"`, `"dative"`, or fractional strings
   without an explicit migration rule and evidence.
4. Complete extraction, merge, copy, pickle, removal, and component tests before
   changing public capability declarations.

### Wave 3: rich inbound semantic adapters

**Implementation status:** complete for RDKit, OpenFF, MDAnalysis, ParmEd, and
mmCIF in the fixed priority scope.

The implemented sequence exercises the broad schema, evidence, mixed-source
completeness, and the chemistry/mechanics boundary.

### Wave 4: reduced outbound adapters and reports

**Implementation status:** complete for MDTraj/OpenMM reduced mappings,
PDB/PDBFixer reduced truth, NetworkX canonical graphs, and dispatcher
preflight/strict policy in the fixed priority scope.

No reduced target may silently downgrade a rich state. Broader adapters remain
subject to the same policy when they are prioritized after 1.0.

### Wave 5: persistence and public lifecycle

**Implementation status:** H5MSM 0.4, H5MSM 0.3 migration, canonical public
attributes, docstrings, User Guide, Cookbook, and Common Core course surfaces
are implemented for the priority vertical. The 17 current H5MSM demos have a
machine-readable source/recipe/invariant manifest and use H5MSM 0.4; one small
immutable H5MSM 0.3 fixture remains isolated for migration coverage.

After schema acceptance, define H5MSM 0.4 persistence, retain an H5MSM 0.3
reader and migration fixtures, update the complete attribute policy and all
Lifecycle Integrity surfaces, and regenerate demos from reproducible recipes.
Only the required small H5MSM 0.3 migration corpus remains as legacy data.

## Scientific fixture matrix

The gate requires deterministic fixtures for:

- known zero bonds versus unavailable connectivity;
- single, double, triple, and explicitly zero order;
- aromaticity and fractional order independent of formal order;
- covalent and directional/dative relationships, and conjugation;
- E/Z bond stereo with reference atoms and R/S atom stereo;
- formal charge, isotope, radicals, and implicit-hydrogen policy;
- explicit, inferred, guessed, user-defined, and unknown evidence;
- complete and partial connectivity;
- mmCIF covalent connection versus metal coordination;
- ParmEd chemical order versus mechanical parameter type;
- duplicate source IDs, atom subsets, and canonical endpoint remapping;
- multi-state reference resolution and ambiguity failure.

Expressive round trips assert canonical equality and missingness. Reduced round
trips assert documented equivalence or the exact structured loss report. Strict
tests assert a deterministic catalog diagnostic.

## Risks and controls

| Risk | Control |
|---|---|
| Replacing external `.bonds` APIs mechanically | Classify object ownership before every edit |
| Silent semantic promotion | Never infer order, aromaticity, or completeness during delivery |
| Premature public schema | Keep storage private until registry, getters, docs, and tests are atomic |
| Memory growth | Allocate optional columns only when present and benchmark large systems |
| Dependency semantic drift | Probe supported versions and record assumptions in tests |
| Components joined by coordination | Require covalent participation policy and metal-complex tests |
| Duplicate legacy/canonical ownership | Use translating facades with a removal gate |
| Demo files hiding migration defects | Generate current demos and keep separate versioned legacy fixtures |

## Exit criteria

This audit can be archived only when native adapters use the state seam; the
normalized table passes lifecycle tests; rich adapters preserve the accepted
subset; reduced adapters report or reject losses; evidence and completeness
survive conversions; H5MSM 0.4 and 0.3 migration gates pass; public additions
satisfy Lifecycle Integrity; and demo regeneration is reproducible.
