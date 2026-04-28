# Proposal: Native ProtOr Atom Typing and Radii in MolSysMT

## Summary

MolSysMT should provide a native, reusable capability to assign ProtOr-style
atom types and van der Waals radii to protein atoms.

The immediate motivation is CASTp/CASTpFold fidelity in TopoMT, but the
capability is general enough to belong in MolSysMT itself rather than in a
single consumer library.

The proposed feature should:

- assign a ProtOr-like atom type of the form `XnHm` to heavy atoms in proteins;
- assign the corresponding ProtOr van der Waals radius;
- ignore explicit hydrogen atoms as geometric primitives while accounting for
  hydrogen effects implicitly through the assigned heavy-atom type;
- expose traceable fallback behavior for unsupported or ambiguous cases;
- be usable from any supported molecular-system form through the standard
  MolSysMT API.

This proposal does **not** request immediate support for full small-molecule
chemical perception or arbitrary ligand typing. The first target is proteins,
with a clear extension path for later coverage.

---

## Motivation

### Why this belongs in MolSysMT

ProtOr-like typing is not only useful for TopoMT/CASTp.

It is a general structural-chemistry primitive that can support:

- surface and pocket computation;
- atom-radius assignment for geometric methods;
- solvent-accessibility and molecular-surface workflows;
- native structure-preparation and topology-aware analysis pipelines;
- future structure-quality diagnostics and environment-aware descriptors.

If each downstream library implements its own protein-aware atom typing,
MolSysSuite will accumulate duplicated, drifting chemistry logic. Centralizing
this in MolSysMT is therefore the more robust architectural direction.

### Immediate driver: CASTpFold parity

The public CASTpFold documentation states that:

- internal computation depends on atom/group van der Waals radii;
- atoms are typed in a form like `XnHm`;
- hydrogen effects are accounted for implicitly in the heavy-atom group;
- explicit hydrogen atoms are otherwise ignored in the geometric computation.

TopoMT currently contains a first ProtOr-like implementation, but it is still
too method-local and not yet mature enough to serve as a canonical chemistry
service for the suite.

MolSysMT is the right place to grow this into a stable capability.

---

## Problem Statement

Current MolSysMT native structure support includes:

- element-aware and residue-template-aware reconstruction tools;
- native handling of missing atoms and hydrogens;
- topology-level queries and expected-atom logic.

However, MolSysMT does **not** yet provide a native public service for:

- protein-aware heavy-atom ProtOr typing;
- implicit-hydrogen-aware radius assignment;
- transparent traceability of the rule used for each atom.

As a result:

- downstream geometric methods either rely on ad hoc local tables;
- or fall back to element-only radii that are too coarse for some tasks;
- or cannot explain how a given atom received a specific radius.

---

## Scope

### In scope for the first implementation

- standard amino acids;
- common protein protonation variants where residue naming already encodes the
  chemistry, such as `HID`, `HIE`, `HIP`, and optionally `CYX`, `ASH`, `GLH`,
  `LYN` if present in supported forms;
- N- and C-terminus-aware handling where chemically relevant;
- assignment of:
  - ProtOr type label `XnHm`;
  - ProtOr radius in angstroms or native MolSysMT quantity form;
  - assignment provenance / rule metadata.

### Explicitly out of scope for the first implementation

- arbitrary ligand or drug-like chemical perception;
- full general-organic atom typing for all HETATM content;
- environment-dependent pKa prediction;
- quantum-chemical bond-order inference;
- automatic protonation of structures as part of this feature.

Those may become future extensions, but they should not block a first
protein-focused delivery.

---

## Desired Public API

The capability should be available through MolSysMT public surface, not as a
private helper only.

Two public entrypoints are recommended:

1. `get_atom_type(..., model='protor')`
2. `get_vdw_radius(..., model='protor')`

Example sketches:

```python
msm.get(
    molecular_system,
    element='atom',
    selection='molecule_type=="protein"',
    properties=['atom_type_protor', 'atom_vdw_radius_protor'],
)
```

or, if exposed as direct helpers:

```python
types = msm.structure.get_atom_type(
    molecular_system,
    selection='molecule_type=="protein"',
    model='protor',
)

radii = msm.structure.get_vdw_radius(
    molecular_system,
    selection='molecule_type=="protein"',
    model='protor',
)
```

The precise namespace can be discussed, but the key requirements are:

- public;
- form-agnostic;
- selection-aware;
- easy to reuse from downstream libraries;
- unit-safe for radii.

---

## Functional Requirements

### 1. Heavy-atom output only

The ProtOr assignment should be defined for heavy atoms.

Hydrogen atoms should not be required as explicit geometric participants for the
assigned type/radius. The primary assignment should be driven by the expected
chemistry of the heavy atom in its protein context, not by the presence of
explicit hydrogen records in the input structure.

If explicit hydrogens are present, they may be used only as a consistency check
or optional validation aid, not as a mandatory prerequisite for the assignment.

### 2. Implicit-hydrogen-aware typing

The assignment must support the notion that a heavy atom can be typed using
implicit hydrogen participation, e.g.:

- `C3H0`
- `C3H1`
- `C4H1`
- `N3H2`
- `O2H1`

This means the logic cannot be purely element-based.
It also means that the implementation should be able to assign the same ProtOr
type correctly whether or not explicit hydrogen atoms are present in the input
protein structure.

### 3. Protein-aware deterministic rules

For standard amino acids, a deterministic protein-aware mapping is expected.
This should not rely on fragile heuristics when residue identity and atom name
already determine the chemistry sufficiently.

Examples:

- aromatic carbons in `PHE/TYR/TRP/HIS`;
- carbonyl carbons and oxygens;
- hydroxyl oxygens in `SER/THR/TYR`;
- guanidinium nitrogens in `ARG`;
- amide nitrogens in `ASN/GLN`;
- sidechain sulfur handling in `MET/CYS`.

### 4. Terminal-state awareness

Backbone atoms at free termini may need different implicit-hydrogen handling
than internal residues.

Even if the first implementation does not cover every terminal detail, the API
and internal data model should leave room for:

- backbone `N` at N-terminus;
- `OXT` and terminal carboxylate handling;
- explicit provenance when terminal state could not be resolved confidently.

### 5. Explicit provenance

For each assigned ProtOr type, the engine should be able to say how it arrived
there.

Suggested internal provenance labels:

- `protein_table_exact`
- `protein_table_terminal_rule`
- `connectivity_rule`
- `explicit_hydrogen_supported`
- `element_fallback`
- `unsupported_atom`

This is important both for debugging and for downstream parity audits.

### 6. Graceful fallback

When the exact ProtOr type cannot be resolved, MolSysMT should still provide a
clear, deterministic fallback radius by element where appropriate, with an
explicit provenance label.

Silent chemistry guesses should be avoided.

---

## Recommended Internal Design

### A. Separate typing from radii lookup

The implementation should distinguish:

1. atom-type assignment
2. radius lookup

That means:

- one function assigns `XnHm`;
- another maps `XnHm` to a radius table.

This separation makes testing and future extension much easier.

### B. Use canonical data tables in `data/databases/`

ProtOr reference data should live in MolSysMT canonical data, not hardcoded in
multiple modules.

Suggested assets:

- `data/databases/atom_typing/protor_radii.json`
- `data/databases/atom_typing/protor_protein_templates.json`

The second file could encode standard residue and atom-name to ProtOr-type
assignments for protein-heavy atoms, including protonation variants where
needed.

### C. Hybrid strategy: table-first, chemistry-second

For proteins, the recommended assignment strategy is:

1. table-driven exact assignment for supported standard residues;
2. terminal-specific override rules where needed;
3. optional connectivity-informed resolution for ambiguous or incomplete cases;
4. element fallback if all else fails.

This is more robust than trying to infer all protein chemistry from generic
organic perception.

### D. Avoid mandatory external dependencies

The first implementation should be native to MolSysMT and not require RDKit,
Open Babel, or OpenMM.

If later optional adapters are added for richer chemistry inference, they should
be supplementary rather than mandatory.

### E. Explicit implementation paths and tradeoffs

The proposal should explicitly recognize three practical paths for deriving the
ProtOr heavy-atom type `XnHm`.

#### Path 1. Protein-template tables by residue and atom name

This should be the preferred first implementation path for standard proteins.

It consists of:

- residue-aware tables for standard amino acids;
- atom-name-specific ProtOr assignments for heavy atoms;
- explicit terminal overrides where needed;
- explicit support for common protonation-encoded residue names such as
  `HID/HIE/HIP` and optionally `ASH/GLH/LYN/CYX`.

Advantages:

- deterministic;
- transparent;
- easy to audit;
- does not require explicit hydrogen atoms;
- matches the typical structure of protein PDB inputs.

Limitations:

- less general outside standard proteins;
- requires deliberate maintenance of residue-template coverage.

#### Path 2. Connectivity- or chemistry-informed perception

MolSysMT may optionally support a second path that derives `XnHm` from bonding,
valence, and local chemical environment, either natively or through optional
adapters to third-party chemistry engines.

Possible sources include:

- MolSysMT-native connectivity and expected-topology logic;
- optional external adapters such as RDKit or Open Babel.

Advantages:

- more general for ambiguous cases;
- potentially useful for non-standard but protein-like groups.

Limitations:

- more complex;
- more sensitive to incomplete or noisy connectivity;
- should remain supplementary to the deterministic protein-table route for the
  first delivery.

#### Path 3. Temporary protonation as an auxiliary or validation route

A third possible path is to protonate the structure temporarily, use the
resulting heavy-atom hydrogen counts to infer `XnHm`, assign the ProtOr type and
radius to the heavy atom, and then ignore hydrogen atoms in the final geometric
output.

This path is compatible with the CASTpFold statement that hydrogen effects are
accounted for implicitly in the heavy-atom group while hydrogen atoms are
ignored in computation. Protonation, if used at all, would therefore be an
internal typing aid rather than part of the final geometric atom set.

Advantages:

- conceptually direct for determining the `Hm` component;
- useful as a validation route against other typing implementations.

Limitations:

- should not be the canonical first path;
- introduces dependence on protonation policy;
- can blur the distinction between chemical preparation and final geometry.

#### Recommendation across the three paths

For the first MolSysMT implementation, the recommended priority is:

1. protein-template tables by residue and atom name;
2. optional connectivity-informed refinement for ambiguous cases;
3. temporary protonation only as an auxiliary or validation route, not as a
   mandatory prerequisite of the public API.

---

## Proposed Data Model Outputs

The following atom-level properties are recommended:

- `atom_type_protor`
- `atom_vdw_radius_protor`
- `atom_type_protor_rule`
- `atom_type_protor_supported`

This makes the feature auditable and easy to expose through `get()` and
`set()`-style APIs.

Where possible, radii should be returned as MolSysMT quantities.

---

## Testing Strategy

The feature should be test-driven and validated at three levels.

### 1. Unit tests for the reference table

- every supported ProtOr type maps to the documented numeric value;
- fallback element radii are explicit and deterministic.

### 2. Unit tests for standard residues

For each standard amino acid, validate the assigned ProtOr type for each heavy
atom in a canonical topology fixture.

Critical cases:

- `HIS/HID/HIE/HIP`
- `ARG`
- `ASN/GLN`
- `ASP/GLU`
- `SER/THR/TYR`
- `CYS/MET`
- `GLY`
- `PRO`
- terminal `N`, `C`, `O`, `OXT`

### 3. Integration tests on real protein structures

Use one or more small PDB oracle systems to assert:

- all selected heavy atoms receive a type;
- no unexpected fallback dominates standard proteins;
- hydrogens can be absent and the assignment still succeeds;
- the same protein receives the same heavy-atom ProtOr typing whether hydrogens
  are absent or explicitly present in the input;
- explicit hydrogens do not force geometric inclusion of H atoms in the output
  heavy-atom radius set.

---

## Relationship to Existing MolSysMT Work

This proposal aligns well with the current native trajectory of MolSysMT:

- residue-template-backed structure preparation;
- native addition of heavy atoms and hydrogens;
- growing canonical data repositories in `data/databases/`;
- stronger topology-aware semantics at the atom/group level.

ProtOr typing would be a natural extension of that line, not a foreign feature.

---

## Relationship to TopoMT

TopoMT is currently a direct consumer of this need through CASTp/CASTpFold
reproduction work.

The recommended development strategy is:

1. allow a local prototype to mature in TopoMT if needed for short-term
   progress;
2. converge that logic into a proper MolSysMT implementation once the rules are
   stable;
3. make TopoMT consume the MolSysMT API rather than carrying chemistry logic
   long-term.

This proposal is therefore both:

- a request for a MolSysMT-native feature;
- and an architectural guardrail against persistent duplication across the
  suite.

---

## Risks and Open Questions

### 1. Terminal-state ambiguity

Some forms may not expose enough information to distinguish internal vs terminal
state perfectly without rebuilding topology metadata first.

### 2. Protein variant naming

Residue naming conventions differ across PDB-derived sources.
MolSysMT should define what variants are supported natively and what falls back
to a conservative rule.

### 3. Choosing the canonical typing path

The first implementation should state clearly whether the authoritative route
for standard proteins is:

- table-driven by residue and atom name;
- connectivity-informed;
- or hybrid.

This proposal recommends the table-driven route as canonical for the first
protein-focused delivery, with the other paths treated as auxiliary.

### 4. Non-standard residues

A strict first implementation should avoid pretending to support full ligand
chemistry. The fallback path must remain explicit.

### 5. Temporary protonation policy

If temporary protonation is ever used internally for validation or ambiguous
cases, MolSysMT should document:

- whether it is optional or automatic;
- which tool or rules are used;
- and how it is prevented from affecting the final heavy-atom-only geometric
  output.

### 6. Public API placement

The exact public namespace is still open:

- `molsysmt.basic`
- `molsysmt.structure`
- `molsysmt.element`
- or a property-driven `get()`-first exposure

This should be chosen to fit the existing API philosophy.

---

## Proposed Acceptance Criteria

This proposal can be considered successfully implemented when:

1. MolSysMT exposes a public ProtOr assignment capability.
2. Standard protein heavy atoms receive deterministic ProtOr types.
3. ProtOr radii are returned natively and unit-safely.
4. Explicit hydrogens are not required for the assignment to work, and their
   presence does not change the expected heavy-atom typing for standard protein
   cases.
5. Fallback behavior is explicit and traceable.
6. The implementation path for standard proteins is documented explicitly,
   including whether connectivity or temporary protonation may be used only as
   auxiliary routes.
7. The implementation is covered by focused unit and integration tests.
8. Downstream methods such as TopoMT can consume the feature without embedding
   their own ProtOr tables.

---

## Recommendation

This proposal should be accepted as a native chemistry-typing enhancement for
MolSysMT.

It is small enough to be tractable, broad enough to benefit the whole suite,
and directly aligned with current native-implementation priorities.

The recommended implementation order is:

1. canonical ProtOr data tables in `data/databases/`;
2. internal heavy-atom ProtOr typing engine for standard proteins;
3. public API exposure;
4. tests and documentation;
5. downstream adoption in TopoMT and any future geometric modules.
