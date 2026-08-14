---
summary: MolSysSuite consumers need a stable public provider for MolSysMT argument aliases.
issue: uibcdf/molsysmt#157
status: resolved
opened: 2026-08-14
closed: 2026-08-14
verification: reproduced
area: [argdigest, api, dependencies]
guard: tests/attribute/test_argument_aliases.py
normative: devguide/digestion_and_dependencies.md
blocked_by: []
supersedes: []
---

# Public alias contract for MolSysSuite consumers

**Reported:** 2026-08-14, while auditing whether MolSysViewer could be released against
ArgDigest 0.12.0 and the current MolSysMT candidate.

## What

MolSysMT should provide a public, stable and introspectable representation of the
argument-name aliases that sibling MolSysSuite libraries need when they validate a
public wrapper and delegate to MolSysMT with `skip_digestion=True`.

The first consumer, MolSysViewer, currently imports both
`molsysmt.attribute._attribute_synonyms` and
`molsysmt._private.argdigest.normalization.get_element_names.TABLES`. Neither path is a
supported public contract. The temporary integration is version-bounded and guarded in
`uibcdf/molsysviewer#62`; this proposal owns its durable replacement.

## How

Design a provider under a public MolSysMT namespace that returns read-only plain data,
not live mutable dictionaries and not ArgDigest registry objects. It needs to describe:

- canonical attribute synonyms such as `atom_names -> atom_name`;
- context-dependent names such as `name -> group_name` when `element="group"`;
- the semantic family or intended operation, without embedding the caller name of a
  different package; and
- enough provenance or schema version information for a consumer to fail clearly when
  it cannot understand the contract.

MolSysMT's own `AliasTable` declarations should be derived from the same provider or
tested for exact parity with it. MolSysViewer should then build its caller-scoped tables
from the public data and delete both private imports.

This is an integration API, not necessarily a root-level convenience. It should not add
`Topology`, `Structures`, or other non-root objects to `molsysmt.__init__`, and it should
not make ArgDigest a type-level part of the public return value.

## Why

The private coupling has already produced a real resolver-valid failure. MolSysMT 0.12.0
declared the identity entry `constraints -> constraints`. ArgDigest 0.12.0 correctly
rejects self-aliases, so MolSysViewer passed the old mapping into `AliasTable` and failed
during import before any viewer could be created. Commit `7eaf39275` removed the identity
entry, but no published MolSysMT version currently contains that fix.

The current source pair is healthy: the MolSysMT mapping has 155 effective aliases, no
self-alias, no ambiguous source and no chain, and MolSysViewer's 21 normalization tests
pass. That proves compatibility of the checked-out revisions; it does not turn a private
path into a stable cross-package interface.

## Intended contract and exclusions

- The provider is read-only from the consumer's perspective.
- Canonical names are not aliases and therefore never map to themselves.
- Renaming remains one pass; the provider must not encode alias chains.
- Context-dependent aliases are enumerated explicitly. It must not generate a Cartesian
  product such as `{element}_{name}` that admits nonexistent attributes.
- Consumers remain responsible for scoping aliases to their own callers.
- The provider does not decide how simultaneous alias and canonical keywords are
  resolved; that behavior belongs to ArgDigest.
- Compatibility with arbitrary historical MolSysMT releases is not a goal. Honest
  dependency floors are preferable to silently filtering malformed upstream data.

## Acceptance criteria

1. A supported public import path returns the complete alias contract as immutable or
   defensive-copy plain data.
2. Tests reject self-aliases, alias chains, ambiguous sources and nonexistent canonical
   targets.
3. MolSysMT's runtime normalization and the public provider have exact parity.
4. MolSysViewer consumes only the public provider and retains caller-scope regression
   coverage for `viewer`, `Region` and `Whole` query methods.
5. Wheel and Conda metadata in the consumer declare the minimum MolSysMT version that
   introduced the provider.
6. The public API registry, developer documentation, User Guide and relevant course
   material are updated according to lifecycle integrity before the provider is called
   stable.

## What was refuted

Silently deleting identity entries in MolSysViewer would make MolSysMT 0.12.0 importable
with ArgDigest 0.12.0, but it would hide a malformed producer contract and imply broader
compatibility with an old molecular-system architecture that has not been established.

Making ArgDigest accept self-aliases was also rejected. Its refusal is an intentional,
tested diagnostic: a rename that performs no rename is configuration error, not a useful
compatibility feature.

Copying all aliases permanently into MolSysViewer avoids private imports but creates two
independent authoritative lists. It conflicts with the repository's single-source rule
and would let the viewer silently age whenever MolSysMT adds an attribute alias.

## Resolution

MolSysMT 0.22.0 exposes `molsysmt.attribute.get_argument_aliases()`. It returns a
defensive-copy dictionary with schema version 1, the complete attribute-synonym mapping
and explicitly enumerated element-dependent short names. MolSysMT's own caller-scoped
ArgDigest tables are derived from this provider, and parity, canonical-target,
single-pass and copy-isolation properties are executable guards.

MolSysViewer now builds its own caller-scoped tables from this public provider. Both
private imports that motivated the proposal were removed, its normalization suite still
covers `viewer`, `Region` and `Whole`, and a static guard rejects their reintroduction.
The consumer retains `molsysmt>=0.22.0` as the honest schema boundary. Handling a call
that supplies both an alias and its canonical keyword remains an ArgDigest concern and
is tracked independently in that repository.
