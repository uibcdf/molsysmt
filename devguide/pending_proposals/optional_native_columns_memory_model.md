# Optional Native Columns and Memory-Proportional Topology Storage

**Status:** post-1.0 proposal; initial native baseline recorded, comparative
prototype benchmarks pending

**Recorded:** 2026-07-16

## Question

MolSysMT's canonical attribute vocabulary is intentionally broader than the
information present in most individual molecular systems. A protein topology,
for example, usually has no explicit isotope labels, while a cheminformatics
object may carry isotopes, atom stereochemistry, fractional bond order, or
detailed provenance. Materializing every accepted attribute as an all-null
column can therefore make native objects consume memory for information they do
not contain.

The proposed post-1.0 direction is **memory-proportional optional storage**:
selected canonical columns exist physically only when at least one value is
known or when an operation explicitly materializes them. Their logical API
contract remains stable whether the physical column exists or not.

This proposal does not authorize an implementation before 1.0. The 1.0 line
should prefer an explicit, predictable native schema while the chemical-state
and conversion contracts stabilize.

## Why the question is valid

An all-null nullable column still owns an index relationship, a data buffer, a
validity mask, and Python/Pandas objects. The retained cost depends on dtype and
backend. For a million atoms, even a compact nullable integer field can have a
measurable cost; repeated string, object, or extension columns may cost much
more. The exact retained and peak memory must be measured rather than inferred
from dtype width alone.

The cost is especially relevant when:

- many native topologies coexist in an ensemble or cache;
- large coarse-grained, solvated, or replicated systems are represented;
- converters construct intermediate native objects;
- optional attributes expand beyond `isotope` into richer chemical and
  provenance metadata;
- copy, extraction, merge, selection expansion, or serialization duplicates
  empty columns temporarily.

The opposite risk is also real. A physically variable schema can complicate
every consumer, create branch-heavy code, weaken DataFrame subclass
invariants, and confuse the difference between unsupported information,
unknown information, and a known empty collection. Memory savings are useful
only if those semantics remain exact.

## Current 1.0 baseline

The current native `Atoms_DataFrame` has a fixed stable-topology schema. The
nullable `isotope` field is present physically even when every value is
unknown. This gives converters, merge, pickle migration, H5MSM, selection, and
downstream consumers one predictable column layout during 1.0 consolidation.

Chemical-state atom attributes already use a different model: optional
canonical columns are materialized inside a state only when supplied. The rich
bond table similarly distinguishes mandatory endpoints from optional metadata.
These implementations provide useful evidence, but they do not prove that the
same representation is best for the stable topology tables.

H5MSM and in-memory storage need not have identical physical layouts. A missing
dataset in an older or future sparse H5MSM schema can be interpreted through
the same logical contract, while a 1.0 in-memory object may retain a fixed
column for compatibility.

## Required semantic model

For a canonical optional attribute `x`, three questions remain distinct:

1. **Form support:** can this form represent `x`?
2. **Instance availability:** does this particular object contain at least one
   known value for `x` in the resolved domain or chemical state?
3. **Requested delivery:** what aligned result is returned when the form
   supports `x` but the physical column is absent?

The proposed answers are:

- `has_attribute(item, 'x', include_none=True)` reports form support and does
  not depend on physical materialization;
- `has_attribute(item, 'x', include_none=False)` is false when the column is
  absent or all values are unknown;
- `get(item, x=True)` returns an aligned nullable result when the form supports
  `x`, even if this requires a cheap virtual all-missing array;
- setting at least one known value materializes the canonical typed column;
- setting every value back to missing may dematerialize it only through a
  documented policy; implicit dematerialization must not invalidate borrowed
  views or surprise mutation observers;
- an absent optional column means "unknown for every row", never "unsupported",
  "known zero", or "known empty connectivity";
- mandatory identity, relationship, and endpoint columns may never disappear.

These rules must be shared by native memory, dictionaries, H5MSM, conversion
reports, and selectors. No consumer should use raw column presence as a proxy
for form capability.

## Candidate column classes

### Mandatory physical columns

These define row identity or the relations required to interpret other tables.
They should remain physically present:

- stable atom labels and canonical atom typing selected for the 1.x contract;
- hierarchy relation indices such as atom-to-group and atom-to-chain;
- group-to-molecule and molecule-to-entity relations;
- bond endpoint indices in every materialized bond table;
- row counts and state inventory metadata required to resolve alignment.

Whether nullable semantic labels such as `atom_name` should remain mandatory is
a separate compatibility decision. This proposal must not silently reclassify
them.

### Optional physical columns

Initial benchmark candidates are:

- stable `isotope`;
- optional chemical-state atom fields;
- optional rich bond metadata beyond endpoints;
- optional detailed provenance references;
- future canonical annotations whose values are sparse across ordinary
  biomolecular systems.

Coordinates, per-structure arrays, molecular-mechanics parameters, and future
interaction results already belong to separate domains and are not justification
for adding a generic topology property bag.

## Preferred implementation direction

Retain the canonical attribute registry as the logical schema and introduce a
small typed optional-column store per native table or state. Public and internal
access should go through schema-aware helpers that can return:

- a materialized typed column;
- a zero-copy or cached virtual all-missing aligned view;
- an explicit unsupported diagnostic when the attribute is outside the form's
  contract.

The store must accept only registered attributes with declared domain, dtype,
nullability, vocabulary, and persistence mapping. It is not an unrestricted
dictionary. This preserves validation, discoverability, selection semantics,
and conversion fidelity.

Pandas may remain the 1.x compatibility view even if the internal authority
later becomes a struct-of-arrays or Arrow-backed store. A lazily assembled
DataFrame is acceptable only if mutation and view ownership are defined. A
DataFrame property that silently returns a detached copy would break existing
code and is not a compatible optimization.

## Alternatives to evaluate

### Fixed nullable schema

This is the current stable-topology baseline. It is simple, predictable, and
friendly to direct DataFrame access. Keep it if measured optional-column cost is
small relative to topology size and implementation complexity.

### Drop all-null columns opportunistically

This appears simple but spreads `if column in table` checks throughout the
codebase and makes mutation behavior inconsistent. It is acceptable only behind
central accessors and schema validation; ad hoc dropping is rejected.

### Pandas sparse dtypes

Sparse arrays may help fields dominated by one fill value, but nullable string,
boolean, and categorical behavior, mutation, serialization, and conversion to
NumPy must be benchmarked. Sparse dtypes are not assumed to be efficient for
every candidate.

### Arrow-backed nullable columns

Arrow supplies compact validity bitmaps and a columnar interoperability path.
It may reduce memory, especially for repeated strings, but adds compatibility
questions around Pandas mutation, custom DataFrame subclasses, optional
dependency policy, and zero-copy ownership. This work should share evidence
with `topology_selection_indexing_and_pyarrow.md`.

### Rust struct-of-arrays or ECS backend

A native optional-component model fits the longer-term MECS/Arrow direction,
but it is a substantially larger architecture change. Optional-column semantics
must be specified independently so that a Rust prototype can implement the same
contract rather than defining it accidentally.

### Generic property bag

Rejected. It would save schema-design effort at the cost of units, validation,
selection integration, documentation, and conversion reports. Only canonical
registered attributes may enter the optional store.

## Compatibility and migration risks

- User and downstream code may access `topology.atoms['isotope']` directly and
  assume the column exists.
- Exact DataFrame column order is observable and already has regression value
  because positional assumptions previously broke MolSysViewer.
- Pickles and native dictionary payloads may encode physical rather than
  logical schema details.
- H5MSM readers must distinguish a schema version that predates an attribute
  from a supported optional dataset that is absent.
- Selection planning must know that a supported-but-absent column yields an
  unavailable predicate, not a parser error.
- Returning a newly allocated all-null array on every `get()` could exchange
  retained-memory savings for allocation churn.
- Automatic dematerialization can invalidate references to a Series or Arrow
  array and complicate thread safety.

Any production change requires a versioned migration plan and a deprecation
window for direct native DataFrame column access if that access can no longer be
preserved.

## Benchmark and evidence plan

An initial 2026-07-16 baseline now records the accepted 1.0 representation in
`benchmarks/baselines/topology_storage_session.json`. On the recorded Python
3.13 environment, a 100,000-atom representative topology retained about 204.8
bytes per atom and construction took about 168 ms. Materializing the nullable
`formal_charge` state column added 3.0 bytes per atom; absent state columns had
no corresponding payload cost. These numbers are machine-specific baselines,
not adoption evidence. They establish the control against which the candidate
stores below must be measured.

Create reproducible fixtures at small, medium, and large scales, including at
least 10 thousand, 1 million, and 10 million atoms where the environment
permits. Compare:

1. fixed nullable Pandas columns;
2. schema-aware absent columns with virtual delivery;
3. Pandas sparse candidates;
4. explicit Arrow-backed candidates;
5. a native struct-of-arrays prototype only if the smaller experiments justify
   it.

Measure:

- retained RSS and backend-reported deep memory;
- peak memory during construction, copy, extraction, merge, and conversion;
- construction and mutation time;
- repeated `get()`, `has_attribute()`, and selection time for absent and present
  values;
- H5MSM and dictionary serialized size and read/write time;
- cost of materialization and optional dematerialization;
- downstream behavior in MolSysViewer and representative laboratory workflows.

Every benchmark must record Python, Pandas, PyArrow when used, operating system,
architecture, repository revision, dirty-state flag, repetitions, and robust
statistics. No adoption threshold should be invented after seeing one favorable
microbenchmark.

## Decision gates

Adopt optional physical columns only if all of the following hold:

- representative large systems show a material retained-memory reduction;
- common `get`, selection, conversion, copy, and merge workflows do not regress
  materially;
- form support, instance availability, null, explicit zero/false, and
  known-empty semantics remain distinguishable;
- direct DataFrame compatibility is either preserved or migrated explicitly;
- H5MSM, pickle migration, dictionary forms, and priority adapters pass
  round-trip and old-payload tests;
- the implementation uses the canonical registry and does not create a second
  attribute authority;
- lifecycle documentation and the Four Paths course are updated with the final
  user-visible behavior.

Reject or defer the change if savings appear only in synthetic edge cases, if
virtual delivery causes significant allocation churn, or if compatibility
requires pervasive special cases.

## Proposed phases

1. Record baseline memory and latency for the fixed 1.0 schema.
2. Prototype `isotope` as the smallest optional stable-column case behind a
   private schema-aware accessor.
3. Verify native lifecycle and downstream compatibility without changing the
   public default.
4. Compare Pandas, sparse, and Arrow representations using the same fixtures.
5. Decide whether the model is rejected, opt-in, or a versioned default for a
   post-1.0 release.
6. Only after acceptance, generalize to other canonical optional attributes.

## Relationship to other proposals

- `attribute_centric_molecular_system_model.md` defines the canonical domain
  boundaries and rejects unrestricted property bags.
- `chemical_state_v1_executable_contract.md` already uses absence semantics for
  optional chemical-state fields and rich bond metadata.
- `topology_selection_indexing_and_pyarrow.md` owns the near-term Arrow dtype
  feasibility experiment.
- `rusterization_hybrid_columnar_ecs_arrow_graph_engine.md` is the larger
  long-term storage and query architecture; it is not a prerequisite.

This proposal defines the memory and absence semantics those experiments must
respect. It does not select Pandas, Arrow, sparse arrays, or Rust in advance.
