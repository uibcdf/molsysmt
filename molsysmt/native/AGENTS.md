# Native Agents Guide

This guide refines the repository root `AGENTS.md` for native MolSysMT classes and helpers under `molsysmt/native`.

## Scope

- This guide applies to every file under `molsysmt/native` unless a more specific local `AGENTS.md` overrides it.
- Native classes are the canonical internal representation used by rebuild workflows and by conversion targets that need stable local semantics.

## Native-first rebuild contract

- `Topology.rebuild_*` and `MolSys.rebuild_*` are native reconstruction operations.
- They are public native APIs, but they are not form-agnostic APIs.
- Their implementation must operate directly on native tables, arrays, and connectivity data.
- Do not route native rebuild logic through:
  - `molsysmt.get`,
  - `molsysmt.select`,
  - form detection,
  - form-level piping,
  - or any other public form-agnostic dispatch layer.

## Relationship with public element helpers

- Public element helpers remain form-agnostic and may use dispatch machinery when required.
- Native rebuild paths must instead use topology-native inference helpers.
- The topology-native inference helpers currently live in `molsysmt/native/_hierarchy.py`.
- If a rule is needed both by public element helpers and native rebuild logic, factor the rule into a lower-level internal helper and let both layers depend on it.
- Do not duplicate hierarchy rules inside converters or rebuild methods.

## Rebuild responsibilities

- Rebuild methods must clearly separate:
  - index reconstruction,
  - id regeneration,
  - type inference,
  - name inference,
  - deterministic fallback synthesis.
- Rebuild methods must preserve explicit native metadata when requested and when it remains consistent.
- When explicit metadata is missing, rebuild methods may infer or synthesize local defaults according to the contracts documented in `molsysmt/element/AGENTS.md`.

## Canonical order of dependency

- The intended native dependency order is:
  - groups,
  - components,
  - molecules,
  - entities.
- Lower levels may feed higher levels.
- Higher levels must not recursively depend on form-agnostic public queries over the same object being rebuilt.

## Converters targeting native objects

- Form adapters that build `molsysmt.Topology`, `molsysmt.Structures`, or `molsysmt.MolSys` should:
  - preserve explicit metadata available in the source form,
  - populate native tables directly when possible,
  - call native rebuild/inference only for the information that is absent or needs normalization.
- Do not implement form-specific rebuild algorithms in `molsysmt/form/*` when the same semantics can be expressed by the centralized native rebuild layer.

## Local evidence only

- Native rebuild logic must use only local evidence present in the system being built or rebuilt.
- Do not add online enrichment, database lookups, or remote heuristics to native rebuild code.
- External enrichment belongs to higher-level tools such as Sabueso.

## Testing expectations

- Changes in native rebuild logic require:
  - direct native tests,
  - regression tests for affected form conversions,
  - and downstream validation when the change impacts public extraction behavior.
- Prefer tests that lock semantic expectations, not only counts or self-consistency against another conversion that uses the same backend.
