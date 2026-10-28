---
summary: Complete native hierarchy operations for group inventories without atoms.
issue: uibcdf/molsysmt#518
status: resolved
opened: 2026-10-28
closed: 2026-10-28
verification: measured
area: [native, form, basic, sequence, h5msm]
guard: tests/native/test_group_inventory_hierarchy.py
normative: devguide/h5msm_format.md
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

## Accepted implementation scope — 2026-10-28

The maintainer now authorizes this follow-up. Use a compact optional ordered
chain-to-group relation owned by Topology, without adding group.chain_index.
Ordinary atom-backed topology keeps its existing derived path. Native group
inventories can supply the relation explicitly; query, selection, extraction,
builder and serializers must preserve it. Persist it in a versioned topology
layer while retaining the existing H5MSM 0.5 layer-1 reader/writer for topology
without the additional relation.

The maintainer also specifies generated chain IDs A..Z, AA..AZ, BA.., with one
chain per sequence when no explicit chain assignment is supplied. Existing
chain_names.py already has this order through three letters. Reuse the same
ordering, extend generation beyond its finite table when needed, retain explicit
chain IDs and keep FASTA record identifiers/full descriptions separately. A
FASTA header token is not automatically a declared chain ID.

## Implementation and bounded contract

Topology owns an optional packed chain/group relation: signed integer offsets
and ordered group indices. Native group/chain/molecule/entity getters use the
represented tables and relation; ordinary atom-backed topologies without it keep
the existing path. Queries retain repeated positions and ambiguous group-to-chain
memberships. Text selectors evaluate sparse hierarchy rows without an invented
atom table. Empty declarations remain addressable; no relation between an empty
chain and an empty molecule is guessed from matching row positions or labels.

`msm.extract` adds keyword-only `element=None`. Native inventories without atoms
use groups by default; explicit group/chain/molecule/entity selection remaps
hierarchy while retaining source IDs and requested group order. Related parent
tables keep source order. Explicit atomic hierarchy extraction keeps the existing
sorted atomic subset semantics. Source-preserving string extraction retains its
existing position contract. Repeated extraction positions are rejected. Queries
and extraction deliberately have different repetition semantics.

Builder staging accepts groups without atoms, empty chains and empty molecules.
Atom-free compilation retains assigned types and occurrences rather than building
an empty chemical graph. Chain/molecule rebuilds retain their declared slots;
explicit chain/group membership is transported by native copy, addition, atom
extraction and permutation. Resetting groups/chains clears the optional relation;
raw table edits still require an explicit relation update and existing owner
invalidation responsibilities. No new automatic scientific recomputation is added.

TopologyDict's existing chain `group_indices` encode this relation. Its atom-free
decoder preserves the declared tables without builder inference. Its existing 0.1
schema still lacks exact per-atom chain assignments for split groups; H5MSM is the
lossless route for that atomic case. H5MSM 0.5 topology layer 2 adds typed packed
membership, while no-declaration writes keep layer 1. Older layer-1-only readers
need an update for layer 2; other layer codecs and root version are unchanged.

Generated chain IDs use the existing alphabetic ordering, extended beyond the
finite three-letter lookup. FASTA direct chain-ID queries and native conversions
use the same generated labels. Header tokens remain chain/molecule names, complete
descriptions remain entity names, and source entity-ID queries preserve record
IDs. No header parsing heuristic pretends that record tokens are explicit chains.

## Verification

Focused native/FASTA tests and the dictionary/H5MSM round trip pass. The broader
atomic regression revealed the topology permutator's closed field allowlist,
which now validates and carries the new membership field on its unchanged group
axis. The source-string out-of-range diagnostic previously lacked its expected
form name in the current diagnostics runtime; it now names the actual source
form without changing the boundary or selected positions. Alphabetic-label
expectations are intentionally updated; tests preserving raw source text and
record identifiers remain unchanged.

Final validation in the existing Python 3.14 development environment:

- 3,892 tests passed using `--receptor=llm -n12`: all native tests, Topology/
  TopologyDict/MolSysDict adapters, native sequence conversion, FASTA, H5MSM,
  public extraction and permutation, selectors, notebook schemas and heading
  hierarchy. Existing legacy/dependency warnings remain visible.
- 34 direct hierarchy guards passed, including alphabetic boundaries through
  ZZ/AAA, shared membership, invalid atomic contradictions, source-preserving
  extraction, absent chemistry/structures, both selected axes, dictionary and
  H5MSM round trips, legacy layer 1 and malformed layer-2 membership.
- 26 public doctest examples passed. Docstring fidelity, public signature
  stability, dependency lazy-import validation and all 97 form-adapter structural/
  delivery checks passed. Ruff and `git diff --check` passed.
- Sphinx HTML passed with `-W --keep-going -j12`; the build disabled overwriting
  existing autosummary stubs. Four pre-existing foreign RST edits retain their
  original hashes and are excluded from the delivery.

MolSysDict and staged-builder writers now reuse the same native membership
projection as TopologyDict. Atom-free dictionary reconstruction does not mark
connectivity or components inferred from an absent graph. Structure selection
uses the existing native extraction route so named analyses retain its normal
remapping rules; absent optional domains stay absent.

These are local source checks, not a complete release/nightly matrix or an
installed-artifact qualification. The issue closing receipt identifies the
published implementation commit.

The expanded dictionary regression also distinguishes omitted grouping from an
explicit empty `groups` list in MolSysDict. Omitting the field retains builder
fallback inference; an explicit empty list preserves a declared group-free
atomic inventory. This reconciles the existing stored-query fallback guard
with the group-free round-trip contract, without weakening either expectation.
