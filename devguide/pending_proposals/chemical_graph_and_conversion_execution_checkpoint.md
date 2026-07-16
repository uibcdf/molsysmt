# Chemical Graph and Conversion Execution Checkpoint

**Status:** fixed pre-1.0 chemical-graph consolidation block complete

**Recorded:** 2026-07-15

**Next decision:** select the next 1.0 consolidation block without reopening
the accepted native chemical-graph contract

## Purpose and authority

This checkpoint records where the current consolidation program stopped and the
exact point from which work should resume. It is an operational index, not a
second architectural specification.

Detailed semantics and acceptance requirements remain in:

- [Attribute-Centric Molecular-System Architecture](attribute_centric_molecular_system_model.md);
- [Chemical State v1 Executable Contract](chemical_state_v1_executable_contract.md);
- [Conversion Fidelity Matrix and MolSysDict Schema Evolution](conversion_fidelity_and_molsysdict_v1.md);
- [Native DCD and XTC trajectory I/O](rusterization_parallel_trajectory_io.md);
- [Exploring an AOT Rust Backend to Replace Numba Kernels](rusterization_heavy_computations.md).

When this checkpoint and a detailed proposal disagree, the detailed proposal,
current normative documentation, code, and executable tests determine the
actual contract according to the developer-documentation authority order.

This checkpoint deliberately does not select column names or freeze a schema.
Its job is to make the next design discussion finite, traceable, and testable.
An item appearing below is not evidence that it has been accepted or
implemented.

## Scope boundary

The next block concerns a static, chemically meaningful native graph and its
faithful conversion. It does not include force-field bonded terms, geometric
contacts, interaction analysis, reaction perception, bond-order calculation,
or a general cheminformatics toolkit. Those capabilities may consume the graph
later, but they must not expand the first vertical implicitly.

The implementation must preserve MolSysMT's ability to represent incomplete
systems. Coordinates, mechanics, complete valence, and even connectivity may be
unavailable. Chemical validation must therefore distinguish malformed data from
chemistry that is merely unknown or partial.

## Completed or evidenced work

### Contract-tested conversion slice

The first `tests/conversion_truth/` slice is implemented and covers a curated
native system with string IDs, hierarchy, typed and untyped bonds, irregular
time, multiple structures, and triclinic boxes.

That slice found and corrected these concrete failures:

- native atom extraction could reorder topology without applying the same order
  to structural arrays;
- `MolSys -> MolSysDict` and YAML conversion ignored requested subsets;
- `MolSys -> mdtraj.Trajectory` could combine a full topology with selected
  coordinates;
- H5MSM could materialize missing bond metadata as the string `<NA>`;
- public `MolSysBuilder.add_bond()` metadata arguments were not consistently
  usable through digestion.

The slice is evidence for those paths only. It is not evidence that the complete
conversion matrix or chemical graph is faithful.

### Reference-state storage seam

The first reversible migration step is implemented. Native `Topology` now owns
a private reference-chemical-state storage boundary, and `Topology.bonds` plus
`Topology.components` are properties that return those authoritative tables
directly. There are no duplicate bond or component tables, and existing public
access remains compatible.

Legacy pickle state containing direct `bonds` and `components` entries migrates
on restore. Focused native, builder, conversion-truth, and H5MSM tests cover
table identity, independent copying, current pickle round trips, and simulated
legacy restoration.

This seam is not a public `ChemicalState` API and does not implement a
persistence schema. Atom-aligned `component_index` is now physically owned by
each private chemical state; it is no longer duplicated in `Topology.atoms`.
Legacy pickles with the old atom column migrate it into the resolved reference
state, while H5MSM 0.3 retains its historical on-disk atom dataset through an
explicit adapter translation.

The second migration step has established private native component-membership
accessors and routed `Topology` lifecycle operations, native hierarchy
inference, `MolSysBuilder`, topology expansion, and the central
`molsysmt.Topology` get/set adapter through that seam. Physical storage is now
state-local, and these core paths no longer depend on its location. The
migration also corrected a preparation check that looked for
`component_index` on groups despite the existing atom-level invariant.

Specialized native builders now use the same seam for peptide construction,
water boxes, solvation, ions, missing hydrogens, and native atom/capping
placers. This migration exposed and fixed a tiled-water defect that assigned
computed endpoints to an unused `_bonds` attribute instead of the authoritative
bond table; a focused two-tile regression fixture now asserts all remapped water
bonds.

The native H5MSM adapter and the ViewerJSON-to-native adapter route component
membership through the same seam. This intermediate 0.3 adapter decoupling was
the prerequisite for the completed 0.4 persistence migration described below.

The first private multi-state container vertical is also implemented. Native
`Topology` now owns an ordered private chemical-state collection and a nullable
reference-state index. The default remains one implicit reference state for
backward compatibility, while private lifecycle operations can represent zero
or multiple states. Reads with zero states fail as unavailable, multi-state
reads without a reference fail as ambiguous, and an explicit bond/component
mutation can create the first state without making reads stateful.

Each private state now carries validated identity, connectivity completeness,
component completeness, component evidence, provenance reference, and an
optional atom-attribute table. Copy and pickle preserve every state and the
reference independently. Restore logic accepts both legacy direct
bond/component tables and the intermediate single-reference-state storage
produced earlier in the migration.

The private atom-state vertical is implemented for `formal_charge`,
`is_aromatic`, `n_unpaired_electrons`, `n_implicit_hydrogens`,
`allows_implicit_hydrogens`, and `stereochemistry`. Columns remain absent until
materialized, use nullable Pandas dtypes, and preserve the distinction between
an absent column, a missing per-atom value, and explicit zero or `False`.
Assignment validates names, values, lengths, and atom indices; extraction,
copy, and pickle preserve the data. The first semantic atom-stereo vocabulary
is `R`, `S`, `r`, `s`, `unspecified`, and `unknown`; adapter-specific traversal
tags are not accepted as canonical values.

Subset extraction now supports multiple private states because component
membership is physically state-local. Each state subsets atom attributes,
filters and remaps all bond atom references, selects its own component rows,
and remaps its own membership independently. A topology with multiple states
and no reference remains valid after extraction; reference-dependent reads
continue to fail as ambiguous.
The atom-state fields are now public for native `Topology` and `MolSys` through
the canonical names `formal_charge`, `atom_is_aromatic`,
`n_unpaired_electrons`, `n_implicit_hydrogens`,
`allows_implicit_hydrogens`, and `atom_stereochemistry`. Getter, setter,
availability, mixed stable/state retrieval, reference-state selection, and
legacy formal-charge conflict behavior are tested. H5MSM 0.4 persistence is
implemented; priority adapter mappings and an explicit public state-selector
argument are implemented for the fixed priority scope.

### Bond-schema migration impact audit

A read-only repository audit after the atom-state vertical found direct native
bond-table use in 45 Python modules. Native lifecycle code, builders, public
getters, H5MSM 0.3, ViewerJSON, MolSysDict, and several third-party adapters
read or mutate `Topology.bonds` directly. The legacy `order` and `type` columns
are strings; current RDKit and OpenFF adapters encode aromaticity and dative or
fractional concepts into them. Renaming those columns in place would therefore
be a high-risk semantic and compatibility break, not a self-contained schema
edit.

At that stage, the recommended next vertical was a bond-access migration seam before changing
physical columns:

1. define private state-resolved bond read/write operations for endpoints and
   optional metadata, backed by the single authoritative state table;
2. route native lifecycle operations and `MolSysBuilder` through the seam;
3. route central native getters and serialization adapters through it;
4. regression-test legacy `bond_order` and `bond_type` behavior without
   declaring richer attributes;
5. only then replace the physical legacy columns with the normalized contract,
   using explicit compatibility translation rather than duplicate canonical
   and legacy columns.

This ordering preserves one authority and makes each migration step reversible.
The seam must not reinterpret `"aromatic"`, `"dative"`, or fractional strings;
semantic splitting belongs to audited converter-specific migration and must
produce a fidelity report when exact preservation is impossible.

The first bond-seam vertical is now implemented. Private operations resolve an
explicit or reference state for bond reads, replacement, reset, append, and
removal while retaining one authoritative table. Native `Topology` lifecycle
operations and `MolSysBuilder` use the seam. Plain DataFrames are normalized
back to native storage without changing non-missing legacy metadata; endpoint
shape and range plus metadata lengths are validated. Tests cover zero-state
mutation, ambiguous reference reads, explicit-state isolation, nullable legacy
metadata, and lifecycle behavior.

This segment found two compatibility defects and fixed them without changing
the H5MSM version. Bond-table coercion could turn a missing legacy value into
the literal string `"nan"`; it now preserves nullable strings. The H5MSM 0.3
extractor assumed optional `order` and `type` datasets always had one entry per
bond, although the writer can represent those attributes as unavailable with
zero-length datasets. Extraction now supports both layouts. Central public
getters, capability checks, TopologyDict, MolSysDict, ViewerJSON, and the H5MSM
0.3 native reader/writer now use the seam. The native topology merge adapter
uses controlled bond-table concatenation, avoiding Pandas dtype drift for
unavailable optional columns.

Conversion-truth tests establish that these consumers fail closed when several
states have no reference and omit unavailable optional metadata instead of
fabricating values. The H5MSM reader is also verified to populate bonds through
the state seam. The repository-wide direct-access count fell from 45 to 32
Python modules at this stage. The remaining central native-form consumers are
format or third-party adapters that require fidelity mappings rather than a
mechanical rewrite.

The physical normalized bond schema is now implemented privately. Required
endpoints and fourteen optional chemical fields follow the accepted nullable
dtypes; optional columns are allocated only when used. Normalization rejects
self-bonds, duplicate unordered pairs, invalid references, unsupported bond
types and evidence, and unexplained component-participation overrides. Legacy
integer/fractional orders, order labels, aromaticity, and accepted chemical
types are split into their canonical fields. Opaque labels such as `amide` are
rejected because they cannot be mapped without inventing semantics.

Native extraction and addition remap endpoints, stereo reference atoms, and
donor/acceptor indices together. If an extraction removes a stereo reference,
the dependent stereochemistry is removed rather than left inconsistent.
Component reconstruction excludes edges with `joins_components=False`.
Missing participation values remain a documented legacy-compatibility
assumption and therefore produce partial rather than complete component
semantics.
H5MSM 0.3 reads use an explicit reduced translation for fields they can
represent. New writes use H5MSM 0.4 and persist the normalized schema without
that reduction. Public rich-bond delivery and priority third-party adapter
fidelity now use this normalized storage.

The endpoint-only native/build vertical is also complete. Component inference,
the public native component helper, water-box tiling, solvation, peptide
construction, hydrogen preparation, and native heavy-atom/capping placers now
resolve bond endpoints through the same state seam. They preserve optional
legacy columns while remapping or extending endpoint indices and fail closed
when a topology has several states without a reference.

This migration exposed that `MolSys.add_missing_bonds()` replaced the existing
endpoint columns even though its contract says it adds inferred missing bonds.
It now delegates to the native append operation, preserving existing bonds and
rebuilding components consistently. A regression test fixes that behavior.
The repository-wide direct-access count is now 24 modules, down from 45. One is
the authoritative private storage implementation; the other 23 are format or
third-party adapter modules that need explicit fidelity decisions. There are no
remaining direct `.bonds` consumers in `molsysmt.build`, native inference, or
the component helper.

### H5MSM transition decision

H5MSM 0.4 is now the emitted format version for persisted chemical states. Its
state container, minimum fields, global structure-to-reference association, and
deterministic 0.3 migration have executable coverage.

The transition requirements are:

- retain an explicit 0.3 reader and legacy fixtures;
- make the new writer emit one unambiguous version and schema;
- prefer an additive `chemical_states` layout rather than silently changing the
  meaning of `/topology/bonds`, `/topology/components`, or
  `/topology/atoms/component_index`;
- define how a 0.3 file becomes a single reference state;
- reject unsupported future versions rather than interpreting them as 0.3;
- test minimal, empty, nullable, complete, and selected-system round trips;
- keep direct file getters version-aware or route them through one normalized
  reader before removing any 0.3 paths.

These gates now pass. New writes emit 0.4; all 17 active bundled H5MSM demos are
0.4 assets validated against `molsysmt/data/demo_manifest.json`. One immutable
0.3 alanine-dipeptide file is isolated under tests as the migration fixture.
The public per-structure state-assignment API and its on-disk nullable mapping
are implemented.

### Bundled demo-system regeneration gate

Bundled demo systems and files were regenerated after the native chemical
state schema, priority converter mappings, and H5MSM 0.4 writer stabilized.
The completed regeneration phase:

- maintain a machine-readable manifest of source identity, retrieval or local
  provenance, preparation recipe, expected chemistry, and generated files;
- use deterministic repository scripts rather than manually edited binaries;
- validate atom hierarchy, state-local components, bond semantics, formal
  charge, structures, units, and exact/equivalent round trips as applicable;
- cover the representative peptide, small-molecule, cage, solvent, and other
  systems used by documentation and tests;
- update documentation paths and course examples in the same change; and
- retain a minimal immutable set of H5MSM 0.3 files only as legacy migration
  fixtures, clearly separated from current demos.

Generated demos are release assets, not scientific oracles. Their expected
properties must be recorded independently so regeneration cannot bless its own
mistakes.

The manifest records frozen source checksums, source identity, owning recipe,
and independent hierarchy, bond, and structure counts. Migration asserts exact
or canonical-ID-equivalent data before atomic replacement. The repository
validator checks all 17 active 0.4 files and the isolated 0.3 fixture.

The performance gate records 100,000-atom direct expansion at about 35.0 ms
versus 51.9 ms for the merge reference on the recorded machine. Materialized
native storage is about 204.8 bytes per atom, and materializing optional
`formal_charge` adds 3.0 bytes per atom. These are regression baselines, not
cross-machine limits.

### Progress accounting

Progress reports for this execution checkpoint use the fixed weighted scope
below. The percentages are engineering estimates, not test-coverage metrics.
Separate proposals for `Interactions`, native XTC/DCD I/O, and Rust backends are
not included in this denominator.

| Objective | Weight | 2026-07-16 estimate |
|---|---:|---:|
| Architecture decisions and executable scope | 15% | 100% |
| Native reference-state storage and lifecycle migration | 20% | 100% |
| Exact atom/bond chemical-state schema and semantics | 15% | 100% |
| Versioned persistence and legacy migration | 12% | 100% |
| Priority converters and semantic round trips | 15% | 100% |
| State-aware native selection | 10% | 100% |
| Capability truth, tests, and lifecycle documentation | 8% | 100% |
| Legacy cleanup, removal, and performance gates | 5% | 100% |

The weighted completion estimate for this fixed block is **100%** after its
final validation gate. The prior PyTraj and H5MSM work
remains covered. MMTF and MSMPK were subsequently removed before 1.0 rather
than retained behind an artificial deprecation window. Every
private chemical state now owns its bond graph, atom chemistry, component
membership, and component metadata without duplicate authority. Copy, pickle,
single-state add, atom removal, and extraction preserve aligned chemical atom
rows; extraction remaps every state independently. Native add rejects
multi-state inputs until an explicit state-alignment policy exists rather than
matching non-unique labels or list positions silently. H5MSM 0.3 and legacy
pickles translate through compatibility boundaries. The canonical attribute
registry now distinguishes chemical-state attributes from stable topology and
mechanical parameters. The six atom-state fields are public on native
`Topology` and `MolSys` through `get()`, `set()`, and instance-aware capability
checks. `formal_charge` writes have one canonical chemical-state authority;
the mechanical location is a read-compatibility facade, and conflicting legacy
copies fail closed. MolSysMT selections materialize only requested atom-state
columns and state-local component membership. They reject unavailable fields
and unresolved multi-state systems instead of returning misleading empty
selections. The full accepted rich-bond inventory is registered and publicly
delivered by native Topology, MolSys, and H5MSM through getters, setters where
mutable, instance-aware availability, and direct bond-domain selection.
H5MSM 0.4 now persists zero, one, or multiple states, optional nullable atom
chemistry, state-local components, the complete normalized bond inventory,
completeness, evidence, and provenance references. Compatibility hard links do
not duplicate physical authority. H5MSM 0.3 migrates to one reference state;
unknown versions fail closed. Atom-subset writes remap every state, and legacy
0.3 extraction can remain streaming-compatible. Public `get()` exposes state
indices, IDs, counts, reference index, completeness, and component evidence.
The `chemical_state='reference'`, `'structure'`, or integer resolver now scopes `get()`,
`set()`, `has_attribute()`, and `select()` across atom chemistry, components,
and bonds without mutating the stored reference. State IDs remain non-unique
labels rather than selectors. External forms fail closed for explicit indices
until their mappings are audited. `structure_chemical_state_index` is the
public nullable association owned by MolSys. Native copy, extraction, removal,
append, and concatenation preserve it; incompatible state inventories fail
closed. H5MSM 0.4 persists the real association and never promotes a global
reference into per-structure evidence. RDKit and OpenFF now populate independent
atom and bond semantics; MDTraj and OpenMM preserve their documented reduced
subset in both directions. Immutable conversion preflight reports classify
exact, equivalent, and lossy outcomes, and `strict=True` rejects detected loss
before target creation. Stable nullable `isotope` is public and survives native
dictionaries, merge, H5MSM 0.4, and RDKit input. MDAnalysis and ParmEd rich
inbound mappings are implemented. mmCIF preserves its audited rich subset;
PDB/PDBFixer declare reduced fidelity; NetworkX emits a canonical attribute
graph. The active H5MSM demo corpus is regenerated as version 0.4 from frozen
0.3 inputs with checksum and invariant validation. Generic report coverage
beyond the audited priority paths remains future work and is outside this fixed
denominator. Future segment reports must not silently change the weights or
scope.

The closing validation repaired the complete `MolSys -> biopython.SeqRecord`
route, including non-contiguous atom selections and the intermediate
one-letter sequence adapters. Sequence conversion now retains amino-acid order
while omitting ligands, solvent, ions, and other non-peptide groups. The
`select`, `convert`, and Form Teleportation user notebooks execute cleanly. The
two MolSysViewer merge regressions pass against this checkout, as do the focused
conversion and merge suites, Ruff, dependency validation, and the adapter
structural and delivery audit. These results close the earlier public-fidelity
stint. The subsequent adapter, demo, removal, and performance gates close the
fixed block recorded here; they do not claim exhaustive fidelity for every
optional third-party adapter.

The final repository gate was executed on 2026-07-16 with
`python -m pytest -n 12 --dist loadgroup -o faulthandler_timeout=120 tests -q`.
All 9,152 collected tests completed: 9,150 passed and two were explicitly
skipped. The run included the network-backed PDB identifier tests and the heavy
test group. Before the final run, the H5MSM 0.4 bond getters were changed from
an atom-by-atom full-topology reconstruction to one direct nullable-column read
followed by atom projection. This removed the pathological closing-suite delay
without weakening assertions; both H5MSM adapter suites, comprising 1,044
tests, pass independently. Ruff, dependency-policy validation, adapter-contract
validation, demo-asset validation, and whitespace validation also pass. The
remaining pytest output consists of expected warnings exercised by negative
comparison tests, optional-library behavior, and CPU fallback when no CUDA GPU
is available.

### Comparative object-model audit

MDTraj, OpenMM, RDKit, OpenFF, MDAnalysis, ParmEd, mmCIF, and relevant trajectory
I/O behavior were inspected to understand their object contracts and conversion
boundaries. The purpose was to learn semantics, not copy implementations.

The audit established these design pressures:

- MDTraj and OpenMM Topology expose compact endpoint/type/order bond models;
- RDKit exposes richer bond kind, aromaticity, conjugation, direction, and
  stereochemistry;
- OpenFF separates formal order, aromaticity, fractional order, and
  stereochemistry;
- MDAnalysis can preserve whether connectivity was guessed;
- ParmEd separates chemical bond information from force-field bond parameters;
- mmCIF separates chemical-component bonds from broader structural connections;
- OpenMM System, GROMACS, and AMBER mechanics must not be confused with chemical
  topology.

These are audit findings. Every external API and semantic mapping must be
rechecked against the dependency version used when an adapter is implemented.
The per-adapter evidence, loss classification, fixture matrix, and ordered
implementation waves are recorded in the
[Chemical-State Adapter Fidelity Audit](chemical_state_adapter_fidelity_audit.md).

### Architecture decision record

The attribute-centric architecture, interaction boundary, and nested chemical-
state direction are recorded in the master proposal. Private chemical-state
implementation is underway as recorded above; no public `ChemicalState` or
`Interactions` API has been introduced.

## Agreed conceptual decisions

1. `atom_id`, `group_id`, and other native `*_id` fields are string labels and
   need not be unique. Internal indices are the identity and remapping mechanism.
2. A converter must preserve duplicate source labels when the target permits
   them; it must not invent uniqueness for convenience.
3. `Topology` is provisionally the umbrella for a stable atom inventory and
   semantic organization plus zero, one, or multiple nested chemical states.
   Geometry may inform an explicit inference operation but must not silently
   mutate a state.
4. Chemical bond order, aromaticity, fractional order, bond kind, conjugation,
   and stereochemistry are distinct concepts.
5. Mechanical bond terms, constraints, equilibrium lengths, force constants,
   and functional forms belong to molecular mechanics, not chemical bond type.
6. A component is a state-local covalently connected atom set. Molecule and
   component remain orthogonal, so a covalent drug-protein adduct may be one
   component while retaining two stable semantic molecule labels.
7. Coordination, hydrogen bonds, ionic relationships, and contacts do not join
   covalent components automatically.
8. `Topology.connections` will not be introduced. Declared and observed
   non-covalent relationships belong to a future interaction domain.
9. Bond graphs, formal charge, radical state, protonation, and covalent
   components belong conceptually to chemical state. Elemental identity,
   isotope, and semantic groups, molecules, chains, and entities remain in the
   stable topology core.
10. Form capabilities and instance attribute availability use the canonical
    attribute system; no parallel `coverage` layer will be added.
11. `atom_type` remains the canonical memorable atom-level type and must not be
    confused with `atom_ff_type`; element symbol and atomic number can be
    derived when `atom_type` is unambiguous.
12. Provenance is optional cross-cutting metadata, not a required peer
    `MolSys` object. Compact evidence and detailed provenance are distinct.
13. Nesting chemical states under `Topology` is provisional. A future major
    design may extract them and rename the stable core if real lifecycle and
    compatibility evidence justifies that change.

## Explicitly not implemented

- the public zero/one/multi-state container (private storage, reference
  compatibility facades, and explicit native state selection are implemented);
- a complete conversion-fidelity audit for every supported form; current
  structured reports are conservative and instance-aware for audited fields;
- sparse-by-absence stable topology columns; this is a post-1.0 proposal in
  `optional_native_columns_memory_model.md`;
- `Interactions`;
- a MolSysMT-owned DCD reader;
- a MolSysMT-owned XTC reader;
- a Rust extension replacing Numba kernels;
- a Rust topology or selection engine.

## Migration impact audit

A repository scan on 2026-07-15 originally found direct bond, component-table, or atom
`component_index` access in 93 package Python files, including 77 form-adapter
files. The scan found 159 `.bonds` occurrences, 112 `.components` occurrences,
57 affected test files, and broad documentation exposure. These counts are an
impact estimate rather than a stable metric; it justified the staged migration
rather than one immediate schema edit.

Bond ownership can migrate with relatively low compatibility risk if
`Topology.bonds` becomes a property returning the authoritative reference
state table. Components are more invasive because current code reads and writes
`Topology.atoms["component_index"]` directly as well as `Topology.components`.
A joined or copied compatibility table would risk stale duplicate authority.

The staged migration was executed as follows:

1. introduce state-aware accessors and route internal lifecycle operations
   through them while the current storage remains authoritative;
2. introduce one reference chemical state and make `Topology.bonds` and
   `Topology.components` direct references or properties, never copies;
3. migrate direct `atoms["component_index"]` readers and writers to a
   state-aware component API;
4. move persistence and adapters behind the same accessors with legacy read
   fixtures;
5. remove old physical storage after repository-wide direct-access checks,
   lifecycle tests, documentation migration, and compatibility translations.

Steps 1-5 are complete for the native private vertical. The package has no
remaining direct read or write of `Topology.atoms["component_index"]` outside
legacy-payload detection; H5MSM occurrences address the explicitly versioned
0.3 file layout. Tests now assert that the stable atom table has no component
column and that old pickle state migrates to the reference chemical state.

Temporary compatibility storage, if unavoidable inside one migration step,
must have one declared authority, explicit synchronization assertions, and a
short removal gate. It must not become the permanent design.

## Resume here: executable chemical-graph contract

The next work item is a design-and-approval block. In accordance with the
maintainer decision for new approaches, do not modify the native schema until
the following contract is discussed and accepted.

### Decision 0: topology and chemical-state container

Approve the executable boundary before choosing columns:

- stable topology-core ownership of atom identity, isotope, and semantic
  hierarchy;
- nested chemical-state ownership of bonds, formal charge, radicals,
  protonation, stereochemistry, and components;
- zero-state, one-state, and explicit reference-state behavior;
- convenience access such as `Topology.bonds` without duplicate authority;
- state-local component indices and invalidation after graph mutation;
- state-aware native selection for component, bond, chemical-attribute, and
  `bonded to` predicates while stable label predicates remain state-independent;
- the location of structure-to-state association at `MolSys` composition level;
- a documented future escape hatch for extracting states or renaming the
  stable topology core without treating either as current implementation scope.

### Decision A: atom-level chemical prerequisites

Inventory the minimum atom attributes required to interpret and round-trip bond
chemistry:

- element or atomic number;
- formal charge;
- isotope;
- atomic aromaticity;
- radical or unpaired-electron state;
- atom stereochemistry;
- explicit-versus-implicit hydrogen semantics.

Classify each as required for the first native slice, deferred but schema-aware,
or source-specific metadata. Do not claim chemically faithful RDKit/OpenFF
conversion until the accepted minimum is present.

The decision must finalize the accepted semantics of existing `atom_type`. A
converter must not infer an element silently from an ambiguous atom name or
force-field type. Formal-charge migration into chemical state must include a
compatibility and deprecation path for its current mechanical location rather
than creating two independent values.

### Decision B: bond attributes

Approve exact names, dtypes, nullability, normalization rules, and public
semantics for at least:

- endpoint atom indices;
- formal bond order;
- aromaticity;
- fractional or partial bond order;
- chemical bond kind;
- conjugation;
- bond stereochemistry and any required stereo reference atoms;
- explicit-versus-inferred evidence;
- namespaced source metadata needed for reversible conversion.

The contract must prohibit using `"aromatic"` or `"dative"` as numeric bond
orders and must not silently convert unknown order into single order.

Evidence and provenance must not be collapsed into one boolean. At minimum the
design must be capable of distinguishing a value explicitly declared by a
source, a value inferred by MolSysMT or another tool, the method responsible for
an inference, and an unknown origin. The first slice may implement a smaller
representation only if its upgrade path is explicit.

### Decision C: graph and component invariants

Define:

- endpoint bounds and canonical endpoint ordering;
- self-bond policy;
- duplicate-edge and multi-edge policy;
- which bond kinds participate in covalent component inference;
- dative-bond treatment;
- behavior for invalid valence and incomplete chemistry;
- molecule/component behavior for covalent adducts;
- exact distinction between unavailable connectivity and known zero bonds.

Also decide how a partial bond set affects component inference, whether
source-declared component membership can coexist with or override inferred
membership, and what happens when atom extraction, atom removal, sorting, or
merge remaps endpoints. Component rebuilding must never present an inference
from incomplete connectivity as a fully known chemical partition.

### Decision D: conversion and compatibility policy

Define:

- exact preservation versus documented chemical equivalence;
- resonance and aromaticity canonicalization behavior;
- target-incompatible metadata handling;
- strict and permissive loss behavior;
- source-label preservation and target-required renumbering;
- compatibility of old H5MSM, MolSysDict, and YAML payloads.

Every attempted conversion must have one of four testable outcomes:

1. **Exact:** all in-scope values and their missingness are preserved.
2. **Chemically equivalent:** representation changes under an approved,
   documented equivalence rule.
3. **Lossy:** the conversion succeeds and reports every non-representable or
   normalized field.
4. **Rejected:** strict policy or malformed input prevents conversion with a
   catalog-backed diagnostic.

Permissive mode must not mean silent loss. Decide whether the loss information
is returned, attached as provenance, emitted as a warning, or exposed through a
conversion report before implementing adapters. Strictness must be defined per
unsupported semantic field, not merely as a catch-all exception switch.

## Decision artefacts and approval gate

The design block is complete only when each decision has a durable artefact and
an executable consequence:

| Decision | Required artefact | Minimum executable consequence |
| --- | --- | --- |
| 0: state boundary | accepted ownership, zero/one/reference-state behavior, and facade rules | no duplicate bond/component authority and explicit ambiguity diagnostics |
| A: atom chemistry | accepted attribute ownership and first-slice table | attribute-registry and missingness tests |
| B: bond semantics | names, domains, dtypes, nullability, vocabularies | construction and validation tests for every accepted field |
| C: graph invariants | validation and component-participation matrix | mutation, remapping, partial-graph, and component tests |
| D: conversion policy | exact/equivalent/lossy/rejected policy and compatibility matrix | conversion reports, diagnostics, and old-payload fixtures |

The accepted record must label every entry as **accepted**, **deferred**, or
**rejected**, with a reason. Deferred fields must say whether the storage schema
reserves an upgrade path; otherwise “schema-aware” has no verifiable meaning.

## Minimum scientific fixture corpus

The existing `rich_molsys` fixture is useful for structural conversion truth,
but it is not a chemical-graph validation corpus. Before schema fan-out, add
small, inspectable fixtures covering at least:

- known zero bonds and unavailable connectivity as distinct cases;
- duplicate native ID labels without duplicate atom indices;
- unknown bond order without implicit promotion to single;
- a conventional single/double/triple-order example;
- aromatic or resonance-sensitive chemistry with exact and equivalence checks;
- a conjugated bond and, if accepted in the first slice, stereochemistry with
  its reference atoms;
- coordination or dative semantics without accidental covalent-component
  merging;
- a covalent ligand-macromolecule adduct with molecule/component orthogonality;
- partial connectivity and explicitly inferred connectivity;
- invalid endpoints, self-bonds, and duplicate-edge cases according to the
  accepted policy.

Prefer bundled or programmatically constructed minimal systems whose expected
semantics can be reviewed directly. Larger real systems may complement these
fixtures but must not be the only oracle.

## First implementation vertical

Only after Decision 0 and Decisions A-D are accepted should implementation
begin.

### Vertical 1: native lifecycle

Implement the accepted minimum through:

- the native topology core and reference chemical-state container;
- state-owned atom chemistry, bonds, and components;
- reference-state convenience access without duplicate tables;
- `MolSysBuilder` bond operations;
- getters and setters;
- copy, extraction, removal, merge, sorting, and rebuild;
- component inference;
- validation and catalog-backed diagnostics.

Integrate accepted attributes into the canonical attribute registry and form
capability declarations. Public API changes require complete Lifecycle
Integrity: NumPy-style docstrings and doctests, User Guide Foundations, Toolbox,
and Cookbook coverage, plus verification of the corresponding Four Paths course
modules. Native table tests alone do not complete this vertical.

The complete candidate attribute inventory and the per-attribute delivery
checklist are normative in
[Chemical State v1 Executable Contract](chemical_state_v1_executable_contract.md#canonical-attribute-policy-and-complete-first-version-inventory).
An implementation slice must update those complete lists when it accepts,
renames, defers, or rejects a field. Partial hand-maintained lists are not an
acceptable completion artefact.

### Vertical 2: persistence

Version affected schemas where needed and cover:

- missing and nullable values;
- known-empty connectivity;
- old-file compatibility;
- unknown future versions;
- migration fixtures;
- exact versus intentionally omitted metadata.

Choose one canonical persistence form for the first gate instead of changing
every format simultaneously. Its writer must emit an explicit schema version;
its reader must retain old-payload support or fail with an actionable version
diagnostic. A write followed by a read is insufficient migration evidence:
committed legacy fixtures must be read without first being rewritten by current
code.

### Vertical 3: two external semantic probes

Before migrating the full adapter matrix, validate the same curated chemical
fixtures through:

1. OpenMM Topology as a compact biomolecular topology model; and
2. RDKit or OpenFF as a chemically richer molecular graph model.

Use the other rich form as a subsequent independent adapter check. Object
construction alone is not success: tests must assert every representable field
and every intentional loss.

Probe dependency versions and mapping assumptions at implementation time. Soft
dependencies remain lazy and guarded by the repository dependency policy; the
chemical-graph work must not turn a probe library into an accidental hard
dependency.

### Fan-out gate

Do not migrate all adapters until the native lifecycle, selected persistence
format, and both external semantic probes pass the same conversion-truth
fixtures. Revise the schema before fan-out if a probe exposes a semantic defect.

The gate also requires:

- no silent downgrade in the four conversion outcomes;
- compatibility evidence from committed legacy payloads;
- preservation of duplicate string ID labels wherever the target permits it;
- deterministic diagnostics for rejected or lossy paths;
- `ruff check molsysmt`, dependency validation, focused tests, and the relevant
  scientific/conversion-truth suite;
- a focused memory and construction benchmark showing that the richer graph
  does not impose an unexplained regression on topology-heavy workflows.

If the proposed schema fails the gate, keep adapters on the current contract and
revise the prototype. Do not add compatibility aliases across many forms before
the native representation is accepted.

## Provisional order after the chemical-graph block

The current order of exploration is:

1. complete the version 1.0 reference chemical state, chemical graph, attribute
   truth, and priority conversion-fidelity work;
2. build a DCD corpus and small read-only reference parser;
3. compare DCD Python and Rust/PyO3 implementations and adopt Rust only if the
   correctness, performance, memory, packaging, or maintenance evidence passes
   the recorded gates;
4. perform the XTC specification/corpus/offset feasibility study, with Rust as
   the leading production candidate because compressed XDR decoding is not a
   minor pure-Python task;
5. evaluate AOT Rust migration of one leaf numerical kernel and one scientific
   PBC/MIC kernel as a separate route toward eliminating Numba warmup;
6. prototype one narrow, independent `Interactions` vertical slice;
7. research efficient multi-state/reactive storage and assignment only after
   the reference-state and interaction boundaries are stable.

This order is provisional after the 1.0 gate. DCD/XTC I/O, AOT numerical Rust,
and `Interactions` are independent projects and may be reordered by measured
impact and maintainer priority. A Rust topology/selection engine remains a
separate, more ambitious exploration and is not implied by either trajectory
I/O or AOT numerical kernels.

## The MDTraj/Rust item to remember

The capability most directly associated with MDTraj and Rust in this workstream
is native trajectory I/O:

- MolSysMT currently delegates DCD and XTC parsing to established third-party
  readers;
- DCD is the lower-risk first owned reader;
- XTC compressed decoding is the higher-risk target for which Rust is the
  leading candidate;
- MDTraj and MDAnalysis remain compatibility oracles and fallbacks until an
  owned backend passes the complete corpus, corruption, cursor, numerical, and
  packaging gates.

This is distinct from the AOT Rust proposal whose purpose is to replace Numba
kernels and eventually remove normal-workflow warmup.

## Re-entry rule

> Do not start Rust, `Interactions`, multi-state/reactive expansion, or broad
> adapter migration before the native reference chemical-state contract passes
> its first vertical validation gate.

## Exit criteria for this checkpoint

This checkpoint can be archived when:

- Decision 0 and Decisions A-D have an accepted decision record;
- the native chemical-graph vertical passes its contract tests;
- persistence migration and compatibility behavior are explicit;
- OpenMM plus RDKit or OpenFF semantic probes pass or expose documented target
  limitations;
- the scientific fixture corpus distinguishes exact equality, approved chemical
  equivalence, explicit loss, rejection, partial knowledge, and known-empty
  connectivity;
- public API and attribute additions satisfy Lifecycle Integrity and dependency
  policy;
- focused performance evidence records the cost of the accepted representation;
- the next project is selected using the provisional order and current evidence.

At that point, durable rules move into normative documentation and remaining
work continues in its specific pending proposal.
