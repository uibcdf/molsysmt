---
summary: mmCIF conversion reuses entity indices after revisiting an earlier entity.
issue: uibcdf/molsysmt#763
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: high
verification: measured
area: [form, convert, topology]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_entity_identity.py
normative:
blocked_by: []
supersedes: []
---

# mmCIF entity identity after revisits

**Reported:** downstream original-file failures in uibcdf/molsysmt#763.
**Status:** resolved in source, with independent tiny and unchanged original-file receiving.

## What

Public conversion of original 3WU2 and 5XNL mmCIF files fails before rendering.
The caller's entity/chain correspondence is not safe when an earlier entity is
revisited before a previously unseen entity. Entity metadata is also coupled
to category row position rather than its declared source ID.

## How

The converter uses each current atom's entity index as its next-new-entity
counter. Visits 1, 2, 1, 3 allocate native indices 0, 1, 0, 1. The chain counter
uses the same pattern. Later entity metadata loops enumerate source rows as
native entity indices. These are independently observable correspondence bugs.
The [wwPDB entity-ID definition](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_entity.id.html)
requires unique labels and explicitly permits nonnumeric identifiers; converting
the native labels through an integer array is therefore inappropriate.

## Why

A source-ID collision can either fail classification or produce an incorrect
molecular hierarchy. The reader is shared by CIF/BinaryCIF and their compressed
forms, with consequences for public MolSys/Topology conversion and client
visualization. This is a provider identity defect, not a renderer failure or
an input-size/resource-limit observation.

## What is measured and what is assumed

The owner reproduces the original failures: KeyError 31 on unchanged 3WU2 and
KeyError 9 on unchanged 5XNL. An independent four-atom source also proves silent
corruption: revisiting entity 10 before adding entity 42 returns the earlier
entity 2 instead. The first corrected entity-only cohort passes 74 focused and
929 surrounding CIF/BinaryCIF cases. It repairs 5XNL, but exposes #766's separate
explicit-link failure on 3WU2; that four-pass/four-failure run remains failed.

After both corrections, 106 focused cases and the complete 961-case affected
cohort pass without skips. All eight original-file cases pass: each source
under default and declared-only bond policies, with nm/ps/radians and
pm/fs/degrees standard-unit policies. Every retained atom's deposited entity,
name, chain and coordinates are compared with source rows. Declared covalent
links retain explicit evidence; source bytes/hashes remain unchanged. These
checks establish the received identity/coordinate/link contract, not universal
chemical correctness or a newly qualified installed artifact.

Reproduction commands, native exits, original hashes, resource measurements and
receptor/JUnit reconciliation are retained in the
[combined receipt](../../../devtools/data/mmcif_entity_identity_receiving_763_766_20261115.json).
The original real-file receiver is explicitly selected with
`MOLSYS_MT_763_ORIGINALS` pointing to the manifest's unchanged files. Default
unit tests require no network or downloaded originals.

## What was refuted

This is not a renderer issue or evidence that the originals need cleaning or
subsetting. Consecutive numeric IDs and metadata row order are not valid
identity assumptions. A successful load alone was insufficient: the tiny
counterexample produced the wrong entity without raising an exception.

## Scope and exclusions

Preserve first-occurrence native entity/chain order and exact source labels.
Join metadata by source ID, retain represented axes and leave source input
unchanged. Do not add new chemistry inference, rewrite the two original files,
select fewer atoms or infer full scientific correctness from a successful load.
Existing inference policies and independent chemical-state ownership remain.

## Acceptance criteria

- An independent synthetic expectation catches revisit collisions, reordered
  metadata, repeated chains and textual/zero-padded entity IDs.
- All five parsed/file entry forms preserve identity on MolSys/Topology routes.
- Both original public files load with complete represented identity, units,
  coordinates and source hashes intact, under default and declared-bond paths.
- Invalid entity declarations fail clearly, without mutating input.
- Relevant existing regressions, dependency/governance checks and Ruff pass.

## Provenance

Source parent ca3071960; existing Linux development interpreter and frozen
support runtime. Original public files and digests are recorded in the
[manifest](../../../devtools/data/mmcif_entity_identity_763_manifest.json).
Shared-host admission, finite CPU/RAM limits, input fingerprints and original
failed executions remain part of the receiving record. No publication or
new candidate/hosted matrix is authorized by this work.

## Resolution

Allocate new entity/chain indices from the respective represented-axis length,
preserve source labels as strings and join metadata by those labels. Exclude
unrepresented entity declarations from the represented native axes, and reject
duplicate/missing entity declarations explicitly. Branched metadata now finds
its represented chain by entity membership rather than treating an entity
index as a chain index. The guard asserts independent expected memberships,
metadata, labels and order through five forms and both native target routes.
The user form article, Common Core molecular-elements lesson and converter
notes explain the contract without changing stored code examples or outputs.
