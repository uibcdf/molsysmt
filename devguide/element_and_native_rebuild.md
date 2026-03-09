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
helpers in `molsysmt/native/_hierarchy.py`.

## Shared Semantics

Both layers must respect the same semantic contract:

- `preserve`: keep explicit metadata when present and consistent,
- `infer`: derive metadata from local evidence already present in the system,
- `fallback`: synthesize a deterministic local default when inference is not possible,
- `impossible`: do not invent metadata that cannot be justified locally.

## Canonical Fallback Rules

Until a better explicit definition exists:

- molecules fall back to components,
- `molecule_name` falls back to `component_name`,
- `molecule_type` falls back to `component_type`,
- `entity_index` is inferred from molecules,
- water molecules collapse into a single entity key,
- `entity_name` falls back to the grouped molecule name,
- ids generated during rebuild are deterministic string ids.

These rules are local-only rules. They do not perform remote enrichment.

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
in `molsysmt/native/_hierarchy.py` instead of reimplementing topology-native
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
