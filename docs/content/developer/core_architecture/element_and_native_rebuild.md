# Element Queries and Native Rebuild

This page summarizes the current architecture for public element helpers and
native rebuild logic. The canonical source of truth remains `devguide/`.

## Architecture

MolSysMT separates two layers:

- `molsysmt.element`: public, form-agnostic query helpers.
- `molsysmt.native`: native reconstruction and inference over `molsysmt.Topology`
  and `molsysmt.MolSys`.

Public element helpers are allowed to use:

- dispatch by form,
- `molsysmt.get`,
- `molsysmt.select`,
- conversion paths.

Native rebuild workflows are not.

## Native Rebuild APIs

The rebuild entry points belong to the native layer:

- `molsysmt.Topology.rebuild_groups()`
- `molsysmt.Topology.rebuild_components()`
- `molsysmt.Topology.rebuild_molecules()`
- `molsysmt.Topology.rebuild_chains()`
- `molsysmt.Topology.rebuild_entities()`
- and the `molsysmt.MolSys.rebuild_*()` wrappers

These are public native APIs. They are not general form-agnostic helpers.

## Semantic Contract

When rebuilding or answering public element queries, MolSysMT follows the same
semantic vocabulary:

- `preserve`: keep explicit metadata when available and consistent,
- `infer`: derive metadata from local system evidence,
- `fallback`: synthesize a deterministic local default when inference is not possible,
- `impossible`: do not invent metadata without local justification.

## Canonical Fallbacks

Current canonical local fallbacks are:

- molecules fall back to components when no better molecule definition exists,
- `molecule_name` falls back to `component_name`,
- `molecule_type` falls back to `component_type`,
- `entity_index` is inferred from molecules,
- water molecules collapse into a single entity key,
- generated ids are deterministic strings.

## Current Consolidation Status

The public element families currently aligned with native fast paths are:

- `component`
- `molecule`
- `chain`
- `entity`

This means that when the input is already native, the public helper delegates
to native projection helpers instead of recomputing native semantics through
the form-agnostic dispatch layer.

## External Enrichment

Native rebuild logic is local-only. It must not depend on remote lookups or
online heuristics.

Richer semantic enrichment from remote databases belongs to MolSysSuite tools
such as Sabueso.
