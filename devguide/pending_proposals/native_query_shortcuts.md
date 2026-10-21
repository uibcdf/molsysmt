---
summary: Native objects query their domains without universal form dispatch
issue: uibcdf/molsysmt#128
status: active
opened: 2026-10-21
closed:
verification: measured
area: [api, basic, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native objects query their domains without universal form dispatch

**Reported:** Original issue #128; expanded by the maintainer on 2026-10-21
to native forms used by TopoMT, DockingMT, PharmacophoreMT and ElastNetMT.
**Status:** Baseline and architecture study. No optimized runtime route or new
public method is implemented by this study.

## What

Provide efficient native access when the input's representation and domain
owners are already known. `MolSys.get()` and `MolSys.info()` currently call
the universal providers. Repeated small queries should not rediscover forms,
search complementary items or reconstruct native containers unnecessarily.

The proposal extends beyond `MolSys`, `Topology` and `Structures`, but does not
require every native class to have identical query semantics.

## How

### Inventory and proposed order

| Native family | Inspected current route | Proposed treatment |
| --- | --- | --- |
| `MolSys` | General `get` and `info` shortcuts delegate to `basic`; supports independent and partial domains. | First implementation target; explicit native ownership and preserved state/structure semantics. |
| `Topology` | No general instance `get`/`info`; form getters read its tables and chemical-state facade. | Include in the first shared-core implementation; adding instance methods is a public API addition. |
| `Structures` | No general instance `get`/`info`; already has specialized quantity getters, including `get_coordinates`. | Include in the first implementation; preserve quantity policy, array shapes, copies and index validation. |
| `ChemicalStates` | Properties, `get_bonds`, history operations; general form adapter currently exposes only atom/state counts and reference state. | Include domain access in the design; preserve existing specialized methods and explicit state resolution. Do not invent hierarchy it does not own. |
| `Interactions` | Already has validated sparse `query`, `between_selections`, bounded export, coverage and persistence. General form adapter exposes source-axis counts. | Reuse native sparse queries; metadata summary must not materialize occurrences or force lazy packing/index construction. Generic attributes do not replace occurrence queries. |
| `MolSysBuilder` | General instance shortcuts delegate with unconditional validation bypass; native editable tables and arrays exist. | Include editable-system access; repair uibcdf/molsysmt#391 separately and never finalize/build the system just to query it. |
| `MolSysDict`, `TopologyDict`, `StructuresDict`, `ChemicalStatesDict`, `InteractionsDict` | Serialization forms, not interchangeable physical storage. The first two wrap topological getters through a whole native conversion. `StructuresDict` is a plain dictionary form, not an exported class. | Evaluate direct reads for stored counts/metadata and selected fields before adding methods or caching reconstructed objects. Preserve schema semantics and validation. |
| `MolecularMechanics` and its dictionary form | Minimal experimental parameter container; specialized access and adapter capability declarations. | Inventory and follow-up measurements after the primary domain core; do not expand mechanics or its persistence contract under #128. |
| `Simulation` | Configuration object with specialized parameter/construction methods; not a registered `molsysmt.Simulation` molecular-system form. | No general molecular query API presumed; assess independently if a concrete consumer needs it. |
| `ViewerJSON` | Encoded transfer representation; form declares native conversion pipes. | Profile only for a concrete transfer/consumer requirement; compressed data does not offer the same direct-access opportunities as a resident domain. |
| H5MSM/PDB/GRO file handlers and coordinate entries | Native Python types with file/format lifecycle and supported adapters. | Keep a separate I/O study; in-memory shortcuts must not imply reading or converting a complete file for a summary. |

### Shared execution, distinct validated boundaries

1. Factor reusable native attribute delivery below both public entry points:
   native instance methods and form-agnostic `basic` functions. Reuse the
   canonical attribute catalogue and the current semantic providers; do not
   maintain another list of attribute meanings in each class.
2. The native boundary already knows its owner. Avoid universal form discovery,
   complementary-item search and conversion pipes for resident domains.
   Explicitly resolve `MolSys` attributes to their actual stored domains.
3. Keep one real ArgDigest boundary. Its function contract, aliases and
   caller-specific digesters must admit the same supported inputs before an
   internal call can use `skip_digestion=True`. Sharing a method name is not
   sufficient to inherit `basic.get`'s caller-scoped alias/domain registration.
4. Share index validation, selection rules, chemical-state scoping, scalar/ID
   normalization and unit-aware output assembly. These are part of the result,
   not dispensable dispatch overhead. Native property access alone is not a
   replacement for `get`.
5. Separate data acquisition from `info` table construction. Share columns and
   presentation logic while letting a native provider deliver the values.
   A concise `repr` remains a different, deliberately narrower operation.
6. Keep the universal fallback for other forms and complementary form inputs.
   Define supported optimized cases explicitly; if a selection still uses the
   universal parser internally, report that limitation instead of claiming a
   completely native route.

No long-lived cache of mutable native data, copied chemical-state store or
parallel sparse-interaction engine is proposed. Direct dictionary reads should
avoid reconstruction where the serialized field already supplies the result;
derived attributes still need their legitimate computation.

## Why

Suite clients often retain native systems across many queries. Dispatch and
boundary coordination can dominate small metadata/selection operations. A
shared native core also makes provider ownership explicit without weakening
the form-agnostic public toolbox used on external representations.

## What is measured and what is assumed

The reproducible baseline script is
[`benchmarks/native_queries.py`](../../benchmarks/native_queries.py).
It validates synthetic expected counts, coordinate values and selected axes
before timing; measures existing general queries and narrower adapter/property
references; and records warm sparse domain queries separately.

**Benchmarked baseline:**
[`native_queries_20261021.json`](../../benchmarks/baselines/native_queries_20261021.json).
Run from the repository root in the existing development environment:

```bash
python benchmarks/native_queries.py --iterations 3 --repeats 3 \
    --output /tmp/native-queries.json
```

The completed campaign has 23 object/size cases: six resident native objects
at 32, 1,000 and 100,000 atoms, plus five dictionary forms at 32 atoms. All
coordinate fixtures have eight structures. No new environment was created.
Numbers below are median milliseconds per call, not cross-machine limits:

| Object, atom count | General `get(n_atoms=True)` | Existing instance `get(n_atoms=True)` | Narrow validated adapter | General `info`, DataFrame |
| --- | ---: | ---: | ---: | ---: |
| MolSys, 32 | 0.580 | 0.561 | 0.052 | 8.704 |
| Topology, 32 | 0.505 | absent | 0.046 | 8.808 |
| Structures, 32 | 0.705 | absent | 0.102 | 5.765 |
| ChemicalStates, 32 | 0.609 | absent | 0.042 | 4.982 |
| Interactions, 32 | 0.662 | absent | 0.053 | 5.310 |
| MolSysBuilder, 32 | 0.512 | 0.409, invalid boundary (#391) | 0.042 | 8.351 |
| MolSys, 100,000 | 0.545 | 0.535 | 0.052 | 9.026 |
| Structures, 100,000 | 0.612 | absent | 0.082 | 5.131 |
| MolSysDict, 32 | 355.071 | absent | 351.785 | 365.251 |
| TopologyDict, 32 | 345.351 | absent | 346.272 | 356.374 |

Interpretation:

- The existing MolSys instance method tracks the universal query's cost,
  consistent with its forwarding implementation. The source confirms that it
  has no native-specific executor.
- Profiling one warmed MolSys atom-count query records ten calls to
  `basic.get_form.get_form` and two to `where_is_attribute`. It also records
  digestion and quantity-probing machinery. These counts identify repeated
  coordination; profiled times are not substituted for unprofiled timings.
- General DataFrame and Styler summaries have similar costs here. HTML
  rendering was not timed. Avoid assuming Styler formatting alone explains the
  several-millisecond summary cost; acquisition deserves a separate stage.
- Full MolSys coordinate output grows from 0.585 ms at 32 atoms to 2.147 ms
  at 100,000 atoms (eight structures, about 19.2 MB of numeric output).
  Selecting three atom positions and three structure positions stays around
  0.85--0.86 ms. Copying large data is a real additional cost; no dispatch-only
  change makes that cost disappear. These are latency observations, not a
  measured peak-memory result.
- Dictionary topological count queries are dominated by their native conversion,
  which is also paid by direct adapter calls. Both inspected wrapper modules
  call their whole-object converters before invoking the native getter. The
  serialized atom-list length supplies the stored count without that rebuild.
- Warm `Interactions.query` selects the two expected occurrences in approximately
  0.39--0.66 ms across these cases. This fixture has only two occurrences: it
  demonstrates the distinct existing API and is not a sparse-engine scaling test.

No speedup of a future implementation has yet been measured. The direct adapter
omits parts of the general query contract, and the trusted adapter explicitly
omits boundary validation; neither is an equivalent replacement benchmark.
Returning a raw property also omits the complete query/output contract.

An exploratory run including 1,000-atom dictionaries was interrupted before
completion; it produced no accepted timing artifact. The completed baseline
deliberately bounds dictionaries to 32 atoms. Small unbonded synthetic fixtures
do not establish client-level throughput, complex selection performance,
multi-state behavior, cold-start time, memory peaks or installed-package parity.

### Recommended next implementation slices

1. Repair builder boundary correctness in #391, retaining that issue's own
   regression evidence.
2. Implement the shared native query core for ordinary resident-domain access
   and explicit index selections in MolSys, Topology and Structures. Include
   ChemicalStates ownership and partial-system rules from the beginning.
3. Reuse that core in native summary acquisition and share table formatting
   with `basic.info`. Validate both small tables and selected element tables.
4. Add direct dictionary reads for useful stored fields, starting with counts;
   avoid a mutable reconstructed-object cache. Keep legitimate derivation and
   explicit conversion separate.
5. Integrate useful ChemicalStates/Interactions metadata access while retaining
   specialized state/occurrence query methods. Assess mechanics, encoded viewer
   payloads and file handlers only against their own concrete workloads.

Each implementation slice must measure the complete validated before/after
route; narrower adapter timings above are reference costs only.

### Study checks

The completed baseline's embedded assertions pass, and its recorded benchmark
SHA-256 matches the script. The existing
`tests/native/test_molsys_shortcut_validation.py` passes all 15 cases with
`python -m pytest --receptor=llm -n 12`; this protects the current MolSys
boundary and does not test a future executor or repair the builder bypass.
Repository Ruff checking/format verification and developer-guide validation
also pass. No library runtime source changed in this study.

## What was refuted

- Merely wrapping `basic.get` in a native method does not eliminate dispatch.
- Setting `skip_digestion=True` on incoming user arguments is not a valid
  optimization. The builder reproduction in #391 demonstrates the failure.
- Every native form needs an identical molecular query interface: sparse
  occurrences, state collections, simulation configuration and file handlers
  have different domains and lifecycles.
- A raw property access or prevalidated getter provides a demonstrated native
  public speedup: it provides only a narrower reference cost.
- A native shortcut needs a new compiled backend: no numerical hot loop has
  been identified in this dispatch study. Measure before introducing one.

## Scope and exclusions

This stage is an evidence-producing study under the maintainer's release pause.
It does not close #128, add public methods, change defaults or stabilize new
scientific behavior. #121 and #113 retain their separate prior-study requirement.
No candidate artifact identity or publication authorization changes.

## Acceptance criteria for subsequent implementation

- A documented matrix identifies native forms, supported attributes and
  optimized/fallback cases. Add only useful, complete public contracts.
- Preserve independently expected outputs/errors: aliases, unknown keywords,
  empty inputs, partial domains, indices versus string IDs, masks, selected
  atoms/groups, repeated/nonconsecutive structures, state-dependent attributes
  and mixed-level requests.
- Preserve quantity dimensions and nondefault session units; returned array
  shape/copy semantics and invalidation rules remain unchanged.
- Exercise `Interactions` compound participants, occurrence identity, coverage,
  lazy invalidated/patched results and bounded export through existing methods.
- Check live edits without stale cached counts or assignments. Builders remain
  editable; dictionary reads do not silently finalize, guess missing chemistry
  or expand sparse data.
- Benchmark equivalent fully validated routes, including metadata, selected
  coordinates and substantial coordinate outputs; separate first and repeated
  calls, allocation/copying, data acquisition and presentation costs.
- Mechanism guards prevent general dispatch/reconstruction in claimed native
  cases. Semantic assertions must be independent of the shared implementation,
  not only compare two routes that execute the same code.
- Update docstrings/doctests, Foundations/Toolbox/Cookbook and affected course
  modules for each public change. Follow normal API stability review.

## Provenance

Source before this study: `7ef2085d9b011b97bcb94644c0c48b14f96bdb02`.
The baseline artifact records Python, CPU, platform, package metadata versions,
actual import origins, repetitions, fixture sizes, date and benchmark SHA-256.
This development-environment evidence is not installed-artifact qualification.
