---
summary: Native objects query their domains without universal form dispatch
issue: uibcdf/molsysmt#128
status: partial
opened: 2026-10-21
closed:
verification: measured
area: [api, basic, performance]
guard: tests/native/test_native_queries.py
normative:
blocked_by: []
supersedes: []
---

# Native objects query their domains without universal form dispatch

**Reported:** Original issue #128; expanded by the maintainer on 2026-10-21
to native forms used by TopoMT, DockingMT, PharmacophoreMT and ElastNetMT.
**Status:** Resident native query phase contract-tested; initial comparison measured,
with shared scalar-output optimization under comparative measurement.
Dictionary/encoded/file/mechanics follow-up remains outside this implementation.

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

The maintainer subsequently authorizes the resident native implementation during
the release pause. It adds the shared get/info pattern to six resident types,
preserving existing positional arguments and basic-tool result semantics.
It does not stabilize new scientific behavior or close the dictionary/file
follow-up scope of #128. #121 and #113 retain their separate prior-study requirement.
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


## Resident native implementation — 2026-10-21

The maintainer accepts a repeated public `get()`/`info()` pattern matching the
basic tools as closely as compatibility allows. `MolSys`, `Topology`,
`Structures`, `ChemicalStates`, `Interactions` and `MolSysBuilder` now inherit
that pattern from `native/queries.py`. Existing specialized accessors remain.
The [native query contract](../native_queries.md) states the delivered scope,
legacy positional order, keyword-only additions and expression fallback.

`basic.get._get` and `basic.info._info` share execution/output assembly; native
providers resolve a known class directly and bypass general discovery, search
and conversion for flat index queries. Public native boundaries use ArgDigest's
supported registry discovery, local normalization tables and attribute-domain
contracts. Existing value digesters are reused with their basic-provider
semantic context. No global wildcard registration is installed and no duplicate
attribute catalogue is introduced. Private execution helpers stay undecorated.

Structure scope is propagated through every info acquisition and recursive
expression-mask selection. The Structures count adapter uses existing native
alignment rather than dereferencing absent coordinates. Selected nullable
hierarchy counts reuse existing parent mapping; that separately tracked defect
and its guards belong to uibcdf/molsysmt#392. The builder's unconditional
validation bypass is repaired by the common boundary under uibcdf/molsysmt#391.

The new tests assert literal expected counts, parent memberships, duplicate and
empty axes, coordinate values/copies and angstrom output under a nondefault unit
policy. They also reject invalid/unknown arguments and test state selection,
partial systems, editable builders, inherited native query methods and sparse
views. A mechanism guard forbids universal get/info/get_form/where/select/convert
for the claimed native cases, while expression queries retain their fallback.
Executed new examples cover Foundations, both Toolbox tutorials, the Cookbook
and course module 4. Existing notebook cells/outputs are retained.

The resident implementation does not add dictionary instance methods, direct
file queries, a mechanics redesign, new ChemicalStates attribute families or a
replacement for Interactions.query. Those distinctions are part of the public
contract rather than implicit missing implementation.


### Resident correctness qualification

The final selected basic/native/interaction/connectivity campaign passes 2,285
cases on Linux/Python 3.14.7 with `--receptor=llm -n 12`:

```bash
python -m pytest --receptor=llm -n 12 tests/basic tests/native tests/interactions \
    tests/topology/test_selected_state_connectivity.py
```

It includes 54 new native-query cases, the existing shortcut boundary guards,
public get/info, sparse occurrence queries, extraction and H5MSM workflows.
Warnings remain visible (411 across 20 categories, dominated by legacy H5MSM
reads and intentional tiny-memory-budget tests). This is not the full package
suite, browser qualification or an installed-candidate matrix.

Seven new shared-method doctest examples and 34 current count examples pass;
changed method docstrings and new Foundations/Toolbox/Cookbook/course sections
render with zero Sphinx diagnostics. The public-signature guard records four
explicit inherited-method waivers while preserving positional call semantics.

### First resident comparison and remaining scalar overhead

Source `cbb8959e38a1088cefc0f1a7d73589d6b54b9ad6` is measured in
[`native_queries_resident_20261021.json`](../../benchmarks/baselines/native_queries_resident_20261021.json):

```bash
python benchmarks/native_queries.py --dictionary-limit 0 --iterations 20 \
    --repeats 5 --output /tmp/native-resident.json
```

Eighteen resident cases compare fully validated native and general routes in
the same sequential process, with identical independently checked results.
At 32 atoms, native atom-count calls take 0.349--0.395 ms versus 0.506--0.570 ms
through basic.get (about 1.4--1.6 times faster). MolSys info DataFrame acquisition
takes 7.183 ms versus 8.638 ms. ChemicalStates/Interactions info shows little or
no advantage in this first iteration; no universal summary speedup is claimed.

Profiling identifies remaining scalar-output quantity probing: a plain atom
count still calls PyUnitWizard.is_quantity and emits a probe miss. The shared
output assembler now bypasses that inspection for exact built-in scalars
outside its physical wrapping table; physical quantities, custom scalar
subclasses and arrays retain their existing path. This also benefits the
form-agnostic entry point. The affected get/info/native selection passes 373
tests after this bounded change, including explicit guards against probing a
plain count and nondefault-unit selected-coordinate tests. The previous
2,285-case campaign qualifies the resident implementation before this delta.

ArgDigest's registry discovery, caller patterns and per-decorator normalization
selection were inspected at the declared 0.13.0 floor. This is source inspection,
not an installed-provider minimum-version qualification. The current environment
uses the provider versions/import origins recorded in each artifact.
