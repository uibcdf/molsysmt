---
summary: Complete native hierarchy operations for group inventories without atoms.
issue: uibcdf/molsysmt#518
status: open
opened: 2026-10-28
closed:
verification: reproduced
area: [api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Complete native hierarchy operations for group inventories without atoms.

## What

Native Topology can store explicit groups/molecules/chains with zero stored
atoms. A controlled five-group, three-molecule, three-chain case retains group
names and group/molecule membership, including a MolSys/H5MSM 0.5 round trip.
However, has_attribute(group_index) returns False; group-name selection returns
[]; group/chain projections and chain group counts return []. They currently
use atom-level membership. MolSysBuilder.add_group([]) rejects, and the
TopologyDict decoder uses that builder.

## Proposed completion

Design a compact ordered group/chain relation consistent with complete atomic
systems and ambiguous membership. Update hierarchy availability/getters,
selectors, extraction, builder and dictionary reconstruction deliberately.
Distinguish absent atom inventory from chemically evaluated emptiness. Review
scientific preconditions on sequence-only inputs and preserve known groups
instead of rebuilding them from an absent atom graph. Preserve string IDs,
source indices and named-analysis invalidation on real molecular edits.

Serialization must retain any new canonical relation: TopologyDict already has
chain group_indices in its record schema, but its writer derives them through
atoms. H5MSM's native topology tables have a strict versioned schema; extend it
explicitly if storage changes. No ad-hoc group.chain_index column is authorized.

## Acceptance and deferred state

Reproduce and correct the cases above with meaningful native and form-parity
guards, including zero groups, multiple chains/molecules, caps, unknown chemistry,
repeated source records and full atomic regressions. Keep per-chain sequence
boundaries on round trip; a global one-letter string currently concatenates
molecules and cannot represent those boundaries. This is a known limitation,
not an implicit decision to change public string output contracts.

The maintainer explicitly permits this follow-up after the bounded converters
in uibcdf/molsysmt#517. It is not a prerequisite for that delivery and no release
milestone is assigned. Native AminoAcidSequence evaluation remains separate in
uibcdf/molsysmt#242. A FASTAFileHandler is subsequent format/resource work and
does not by itself complete these native semantics.

## Evidence

Reproduced in the existing Python 3.14 development environment from b0f21e58d,
using only temporary objects/files. Complete direct table declarations avoid
mistaking unassigned hierarchy metadata for a sequence limitation. No repository
code was changed during the study. This is bounded operational evidence, not a
new supported atomic representation or a performance benchmark.
