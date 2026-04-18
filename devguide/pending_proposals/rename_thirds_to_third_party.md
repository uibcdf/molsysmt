# Proposal: Rename `thirds` to `third_party`

## Status

Pending proposal

## Purpose

Recommend renaming the `thirds` namespace in MolSysMT to `third_party` for
clarity, consistency, and ecosystem alignment.

## Motivation

The current name `thirds` is short, but it is not a standard architectural term
for external-provider integrations.

Problems with `thirds`:

- it is semantically weak;
- it is not self-explanatory to new contributors;
- it does not match the terminology commonly used in Python projects;
- it creates avoidable divergence with other ecosystem packages that are moving
  toward `third_party`.

By contrast, `third_party` is immediately understandable:

- it clearly signals code owned by external providers or technologies;
- it maps well to common software-architecture vocabulary;
- it improves discoverability in the codebase;
- it reduces cross-repository friction when the same architectural distinction
  exists elsewhere in the ecosystem.

## Recommendation

Adopt `molsysmt.third_party` as the canonical namespace and treat
`molsysmt.thirds` as a compatibility alias during a transition period.

## Proposed Transition

### Phase 1: Introduce `third_party`

- add `molsysmt.third_party`;
- make it the canonical namespace in internal imports and new code;
- keep `molsysmt.thirds` available as an alias.

### Phase 2: Migrate Internal Code and Docs

- update internal imports to `molsysmt.third_party`;
- update developer documentation and user examples;
- stop introducing new references to `molsysmt.thirds`.

### Phase 3: Deprecate `thirds`

- emit a deprecation warning when `molsysmt.thirds` is imported, if practical;
- document the migration path clearly in release notes and developer docs.

### Phase 4: Remove `thirds`

- remove the alias in a later release once downstream usage has had time to
  migrate.

## Compatibility Guidance

This should not be a hard rename in one step if `molsysmt.thirds` is already
used externally.

The recommended pattern is:

1. add the new namespace;
2. migrate internals first;
3. deprecate the old name;
4. remove it only after a compatibility window.

## Expected Benefits

- clearer repository structure;
- better readability for contributors;
- more standard terminology across the MolSysSuite ecosystem;
- easier alignment with TopoMT and future cross-repo documentation.

## Short Rationale

`third_party` is a better architectural name than `thirds`.

The only strong argument for keeping `thirds` is backward compatibility, and
that concern is better handled with a staged migration than by preserving a
weaker public name indefinitely.
