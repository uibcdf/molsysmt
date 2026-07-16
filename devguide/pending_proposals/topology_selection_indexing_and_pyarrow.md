# Proposal: Direct Topology Indexing and PyArrow Feasibility

**Status:** partially implemented; phase 1 completed 2026-07-13
**Scope:** low-to-medium-effort improvements within the current Pandas topology architecture
**Excluded:** DuckDB, Polars, a Rust topology core, and replacement of Numba

## Why this proposal exists

Topology selections currently build temporary atom-level tables through
successive `pandas.merge()` calls. The hierarchy already stores integer links
between atoms, groups, components, chains, molecules, and entities. Rejoining
those tables for every selection duplicates information, allocates temporary
DataFrames, and obscures the simpler data path.

Pandas also supports PyArrow-backed extension dtypes. They may reduce memory use
for repeated text columns and accelerate some string operations, but current
MolSysMT DataFrame subclasses, mutation rules, serialization, and NumPy
boundaries make compatibility and performance empirical questions.

These are two distinct changes. Direct indexing is the primary optimization;
Arrow dtypes are a later, optional experiment.

## Current evidence

The native topology already contains the required relationships:

- atoms store `group_index`, `component_index`, and `chain_index`;
- groups store `molecule_index`;
- molecules store `entity_index`.

Both `molsysmt.basic.selector.molsysmt.select_standard()` and
`Topology.get_atom_indices()` previously reconstructed atom-level attributes
with repeated merges. They now share
`molsysmt._private.topology_expansion.expand_atom_dataframe()`, which gathers
only the requested hierarchy columns through the stored integer links.

The current environment uses Pandas 2.x. It does not provide a global
`pd.options.mode.dtype_backend` switch. Arrow-backed storage must therefore be
requested explicitly with column dtypes or
`convert_dtypes(dtype_backend="pyarrow")`. The codebase also uses `.values` and
`.to_numpy()` frequently, so compatibility cannot be assumed.

## Phase 1: replacing hierarchy merges with direct gathers

**Implementation checkpoint:** complete on 2026-07-13.

### Intended implementation

Build only the columns referenced by a selection:

1. use atom columns directly;
2. gather group, component, and chain attributes using the indices stored on
   each atom;
3. gather molecule attributes through `atoms.group_index` followed by
   `groups.molecule_index`;
4. gather entity attributes through the corresponding molecule indices;
5. preserve existing duplicate-column resolution, null behavior, selection
   syntax, result ordering, and result dtype;
6. share the expansion helper between `select_standard()` and
   `Topology.get_atom_indices()` instead of maintaining two merge pipelines.

No result cache is part of this phase. Native topology DataFrames are mutable
and currently have no revision counter that could invalidate cached values.

### Why this comes first

- It removes the suspected allocation bottleneck directly.
- It adds no dependency.
- It preserves the current Pandas representation and public selection syntax.
- It benefits every input form that uses the native selector after conversion.
- It provides a simpler baseline against which Arrow can be evaluated.

### Acceptance criteria

- Existing selector and topology tests pass unchanged.
- New parity tests cover atom, group, component, chain, molecule, and entity
  attributes, including null indices and mixed hierarchy predicates.
- `@` variables, shortcuts, numeric comparisons against string IDs, and result
  ordering retain their current semantics.
- Benchmarks compare the old merge implementation with direct gathering at
  representative topology sizes and record wall time and peak memory.
- The implementation is adopted only when it provides a material improvement
  without a correctness regression.

### Recorded result

The parity suite covers all hierarchy levels, invalid and null links, native
cross-level selection, and atom ordering. The microbenchmark uses the same
synthetic 100,000-atom topology for both implementations and asserts exact
DataFrame parity before timing.

On the recorded Python 3.13 development session, direct gathering reduced the
median expansion time from 0.053222 s to 0.042146 s (20.8%) and the subprocess
high-water RSS delta from 31.324 MiB to 23.676 MiB (24.4%). These are
machine-specific measurements, not portable performance guarantees. The exact
environment, revision, dirty-state flag, repetitions, and statistics are stored
in `benchmarks/baselines/topology_expansion_session.json`; reproduce them with:

```bash
python benchmarks/micro/test_topology_expansion.py
```

## Phase 2: caching immutable selection plans

After phase 1 is profiled, cache only immutable analysis derived from the
selection string, such as referenced columns or a normalized expansion plan.
Do not cache expanded tables or selection results without introducing topology
revision tracking and explicit invalidation.

Acceptance requires parity tests and a benchmark demonstrating that parsing or
planning remains a meaningful part of repeated-selection cost.

## Phase 3: PyArrow-backed string prototype

### Prototype boundary

Start with isolated topology fixtures and text columns such as `atom_name`,
`atom_type`, `group_name`, and string identifiers. Keep hierarchy indices on
their current nullable integer representation during the first experiment.
PyArrow must remain optional during feasibility work.

Compare the current representation with explicit `string[pyarrow]` columns for:

- construction and copy cost;
- equality, membership, and string filtering;
- peak and retained memory;
- assignment, row insertion, and hierarchy rebuilding;
- `.values` and `.to_numpy()` consumers;
- conversion to and from Tier 1 forms;
- serialization and round trips;
- missing-value semantics;
- custom DataFrame subclass preservation.

### Decision gate

Arrow-backed strings should become a production option only if benchmarks show
a useful improvement in representative workflows, all topology invariants and
round trips remain correct, and the dependency policy is explicit. They should
become the default only after compatibility across supported Python and Pandas
versions is demonstrated.

No fixed speedup or memory ratio is assumed in advance.

## Explicit exclusions

DuckDB is not a low-effort extension of this plan. It would introduce a query
engine dependency, SQL translation, local-variable binding, and a second set of
selection semantics. Evaluating it fairly would require comparison with Polars
and native Rust alternatives.

Those choices belong to the existing long-term architecture proposals. This
proposal neither recommends them nor uses them as prerequisites.

## Recommended order

1. ~~add correctness and performance fixtures for representative selections;~~
   completed 2026-07-13;
2. ~~implement the shared direct-gather expansion path;~~ completed 2026-07-13;
3. ~~prove semantic parity and benchmark it;~~ completed 2026-07-13;
4. evaluate immutable selection-plan caching if profiling supports it;
5. prototype PyArrow-backed string columns independently;
6. decide whether Arrow remains experimental, becomes opt-in, or is rejected.
