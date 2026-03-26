# Element Queries and Native Rebuild

## Purpose
This document defines the architectural boundary between public
form-agnostic element queries and native rebuild/inference workflows.

This file is part of the `devguide/` source of truth. If other developer
documents disagree with it, this document wins.

## Two Distinct Layers

MolSysMT now treats these concerns as different layers:

- `molsysmt.element`: public, form-agnostic query helpers.
- `molsysmt.native`: native reconstruction, normalization, and inference.

They are related, but they are not interchangeable.

## Public Element Layer

The `molsysmt.element` package provides public helpers such as:

- `get_component_index`
- `get_component_name`
- `get_component_type`
- `get_molecule_index`
- `get_molecule_name`
- `get_molecule_type`
- `get_chain_index`
- `get_chain_name`
- `get_chain_type`
- `get_entity_index`
- `get_entity_name`
- `get_entity_type`

These functions are form-agnostic. They may accept a native MolSysMT object
or any supported external form.

### Rule

Public element helpers may use:

- form dispatch,
- `molsysmt.get`,
- `molsysmt.select`,
- conversion paths,
- piping rules.

That is acceptable because their contract is public and form-agnostic.

## Native Rebuild Layer

The native reconstruction APIs are:

- `molsysmt.Topology.rebuild_groups()`
- `molsysmt.Topology.rebuild_components()`
- `molsysmt.Topology.rebuild_molecules()`
- `molsysmt.Topology.rebuild_chains()`
- `molsysmt.Topology.rebuild_entities()`
- and the corresponding `molsysmt.MolSys.rebuild_*()` wrappers

These are public native APIs, but they are not form-agnostic APIs.

### Rule

Native rebuild logic must not depend on:

- `molsysmt.get`,
- `molsysmt.select`,
- public `molsysmt.element.*` queries,
- or any other form-agnostic dispatch layer over the same object being rebuilt.

Native rebuild must instead operate on native topology tables and native
helpers in `molsysmt/native/_topology_infer.py`.

## Shared Semantics

Both layers must respect the same semantic contract:

- `preserve`: keep explicit metadata when present and consistent,
- `infer`: derive metadata from local evidence already present in the system,
- `fallback`: synthesize a deterministic local default when inference is not possible,
- `impossible`: do not invent metadata that cannot be justified locally.

## Component vs Molecule: Orthogonal Concepts

`component` and `molecule` are distinct and orthogonal in MolSysMT's Topology.
Understanding this distinction is critical when working with covalently bonded
complexes, post-translational modifications, or metal-coordination complexes.

| Concept | Definition | Source of truth |
|---------|-----------|----------------|
| `component` | Connected subgraph of atoms (via covalent bonds) | Graph connectivity — computed from the bonds table |
| `molecule` | Semantic chemical unit | Group types within each chain — inferred from group names/types |

**One component may contain multiple molecules.**
Example: MnATP chelated to a protein residue. CONECT records in 1ATP.pdb link
Mn (ion) to `ASN:OD1`, `ASP:OD1/OD2` (protein) and to ATP atoms. This makes
protein + Mn + ATP + water one connected component — but they are clearly
distinct molecules (a protein, an ion, a nucleotide).

**Practical consequences:**
- Covalent drugs: receptor + covalent inhibitor = 1 component, 2 molecules.
- Post-translational modifications (phospho-Ser, phospho-Thr): the modified
  residue stays in the same molecule as the rest of the chain, even though
  it may have a different `group_type`.
- Do **not** derive `molecule_index` from `component_index`.

## Molecule Inference Algorithm

`infer_molecule_indices_from_topology` in `native/_topology_infer.py` uses
group types to partition atoms into molecules within each chain:

```python
_CHAIN_POLYMER = frozenset(
    {'amino acid', 'terminal capping', 'unknown', 'nucleotide', 'saccharide', 'lipid'}
)
_STANDALONE = frozenset({'ion', 'water', 'small molecule'})
```

Rules (applied group by group within each chain):

1. **Chain-polymer types** extend the current molecule. A new molecule starts
   only when the chain changes or when coming from a standalone group.
2. **Standalone types** each get their own molecule (one molecule per group).

This means a run of `amino acid` + `terminal capping` + `unknown` groups
forms a single molecule (a peptide chain), while each `ion`, `water`, or
`small molecule` group gets its own molecule — regardless of connectivity.

`infer_molecule_types_from_topology` then determines the `molecule_type` from
the group names/types *within each molecule* (not the whole component), using
`_get_component_type_from_group_names_and_types`.

## Canonical Fallback Rules

Topology inference in `native/_topology_infer.py` follows these rules:

- `molecule_index` is inferred from group types within each chain (see above).
  It does **not** fall back to `component_index`.
- `molecule_name` is derived from the group names/types within each molecule.
- `molecule_type` is derived from the group types within each molecule.
- `entity_index` is inferred from molecules (molecules with the same name and
  type map to the same entity).
- Water molecules collapse into a single entity key.
- `entity_name` falls back to the grouped molecule name.
- IDs generated during rebuild are deterministic string ids.

These rules are local-only. They do not perform remote enrichment.

## Role of Sabueso

Sabueso belongs to the MolSysSuite ecosystem and is responsible for external
semantic enrichment from remote sources such as PDB, UniProt, and similar
services.

MolSysMT rebuild code must not try to replace Sabueso by embedding online
heuristics or database lookups into native rebuild workflows.

## Native Fast Paths in Public Element Helpers

Public element helpers may use native fast paths when the input is already:

- `molsysmt.Topology`, or
- `molsysmt.MolSys`

In that case, the public helper should delegate to native projection helpers
in `molsysmt/native/_topology_infer.py` instead of reimplementing topology-native
logic locally.

This keeps the public API fast on native objects without breaking the
form-agnostic contract for other forms.

## Current Consolidated Families

As of this stabilization step, the following public element families are
explicitly aligned with the native layer:

- `component`
- `molecule`
- `chain`
- `entity`

Other element families must follow the same pattern when equivalent native
semantics exist and the additional complexity is justified.
