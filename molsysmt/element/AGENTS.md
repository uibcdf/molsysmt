# Element Agents Guide

This guide refines the repository root `AGENTS.md` for public element helpers under `molsysmt/element`.

## Scope

- This guide applies to every file under `molsysmt/element` unless a more specific local `AGENTS.md` overrides it.
- Element helpers are part of the public API. Preserve backward-compatible behavior unless a coordinated breaking change is explicitly planned.

## Public query layer vs internal reconstruction layer

- Public element functions are form-agnostic query helpers.
- In the public query layer, using `molsysmt.get`, `molsysmt.select`, form detection, and piping is acceptable when needed to support arbitrary input forms.
- Internal reconstruction and inference paths are owned by the native layer, not by `molsysmt.element`.
- In particular, logic used by native rebuild workflows must operate on native topology/structure data directly and must not call `molsysmt.get` or `molsysmt.select`.
- Do not add public `molsysmt.element.rebuild_*` helpers. Native rebuild entry points belong to `molsysmt.Topology` and `molsysmt.MolSys`.

## Rebuild semantics

- Rebuild operations mix two different tasks:
  - reconstructing membership/index mappings,
  - preserving, inferring, or synthesizing metadata.
- Keep those tasks conceptually separate when implementing or refactoring element helpers.
- For every rebuilt attribute, contributors must classify behavior as one of:
  - `preserve`: keep explicit metadata already present and consistent,
  - `infer`: derive metadata from local system evidence,
  - `fallback`: synthesize a stable local default when inference is not possible,
  - `impossible`: do not invent the attribute.

## Canonical local-only policy

- Rebuild and inference code in MolSysMT must rely only on local evidence already present in the molecular system.
- Do not assume online enrichment, web lookups, or external registries during rebuild workflows.
- Richer semantic completion belongs to external enrichment tools such as Sabueso, not to local rebuild helpers.

## Canonical fallback rules

- If no better molecule definition is available, treat each molecule as a component.
- Under that fallback:
  - `molecule_index = component_index`,
  - `molecule_name = component_name`,
  - `molecule_type = component_type`.
- If no better entity definition is available:
  - infer `entity_index` from molecules,
  - group waters under the same entity key,
  - otherwise group by `molecule_name`.
- Synthetic ids must remain stable and must be stored as strings.
- Synthetic names must be stable and deterministic. Never pretend they were explicitly present in the source data.

## Attribute-specific expectations

- `group_name`
  - preserve when explicitly present,
  - do not invent chemically rich names if absent.
- `group_type`
  - may be inferred from local group identity and local atom composition.
- `component_index`
  - may be inferred from connectivity.
- `component_type`
  - may be inferred from local group types and local component composition.
- `component_name`
  - may be inferred from local component composition and canonical naming rules,
  - otherwise use deterministic fallback names.
- `molecule_index`
  - may be inferred from explicit molecule metadata when present,
  - otherwise may fall back to component membership.
- `molecule_name` and `molecule_type`
  - preserve explicit metadata when present,
  - otherwise infer locally when possible,
  - otherwise use the canonical fallback rules above.
- `entity_index`, `entity_name`, and `entity_type`
  - preserve explicit metadata when present,
  - otherwise infer locally when possible,
  - otherwise use the canonical fallback rules above.

## Refactoring rule

- When a public element helper contains both:
  - form-agnostic dispatch code, and
  - topology-native inference logic,
  split those concerns instead of duplicating them.
- The preferred design is:
  - a public wrapper in `molsysmt/element`,
  - plus an internal helper operating directly on native topology data.
- Native rebuild workflows must reuse the internal helper, not the public wrapper.

## Testing expectations

- When changing element semantics, update or add direct tests under `tests/element`.
- When the change affects rebuild behavior, also add or update integration tests that exercise:
  - native rebuild workflows,
  - PDB and string-PDB conversions,
  - downstream consumers such as `compare`, `info`, or `nglview.NGLWidget` when relevant.
