---
summary: Native objects need an explicit copy ownership and memo contract
issue: uibcdf/molsysmt#121
status: active
opened: 2026-10-21
closed:
verification: reproduced
area: [native, api, basic, performance, tests]
guard: tests/interactions/test_copy.py
normative:
blocked_by: []
supersedes: []
---

# Native object copy ownership and memo contract

**Reported:** Existing issue #121 requests `copy()`, `__copy__()` and
`__deepcopy__()` and names TopoMT's `Topography` as a reference. The maintainer
requested a design study before implementation.
**Status:** The maintainer accepted advancing toward independent native handles
over shared protected storage with controlled writes. A reproducible development
prototype and contract probes now compare storage layouts. Earlier bounded
recommendations are retained below as alternatives. The final storage layout
and public signatures are not frozen. `Interactions`, standalone `Structures`
and complete/partial `MolSys` now provide resident copy boundaries, described
below. Molecular copies preserve owner bindings and may defer coordinate/box
allocation. The remaining resident convenience methods and named payload
wrappers now use independent graph copies. The production resident campaign
below measures copying, edits and consumers on three bounded synthetic systems.
It records H5MSM I/O/public-load allocation bottlenecks and the measured
refinements below. Attached coordinate/box setters and controlled topology chemical-state edits now
publish owner invalidation without dense geometry materialization. General table copy-on-write, other direct
domain mutation observation and full production/client performance qualification
are not delivered by these boundaries.

## What

Define native copying without form discovery, rebuilding, chemical inference,
interaction remapping or serialization. Preserve supported data, local indices,
units, producer provenance, domain ownership and intentional internal aliases.
Keep the existing independent-copy meaning of ordinary native `.copy()` calls.

## How

### Inventory at the inspected source

| Family | Existing `.copy()` | Python copy protocol and concern |
| --- | --- | --- |
| `MolSys` | Reconstructs base-class domains; uses interaction `remap()`; separate complete/partial branches. | No explicit hooks. `copy.copy()` shares topology and rewrites its owner through `__setstate__`. |
| `Topology` | Copies known tables and its chemical-state collection; returns a base `Topology`. | Serialization restoration coerces shared chemistry during shallow copying. Owner links are intentionally omitted by serialization. |
| `Structures` | Delegates to `deepcopy`. | No explicit hooks; current deep copy is a useful behavioral reference. |
| `ChemicalStates` | Reconstructs the collection and copies private states. | No explicit hooks; preserve state inventory, history and reference selection. |
| `MolSysBuilder` | Reconstructs topology and structures in a base builder. | No explicit hooks; copying must not call `build()` or synthesize missing parents. |
| `MolecularMechanics` | Manually deep-copies listed settings, assignments and parameter tables. | Include as a resident domain without expanding its experimental scientific or persistence scope. |
| `Interactions` | No `.copy()` method. | Both Python operations use `__reduce__`, encode/decode the analysis, duplicate numeric buffers and flatten filtered/patched storage. Query views preserve their selected occurrence indices in the observed examples. |
| `MolSysDict`, `TopologyDict`, `ChemicalStatesDict`, `InteractionsDict`, `ViewerJSON` | Independent payload copies already exist. | Reconcile wrapper semantics with the chosen contract; retain their distinct schemas. `StructuresDict` is a plain dictionary form, not a native class. |
| `Simulation` | Copies settings but retains the molecular-system reference. | Configuration/reference semantics need their own explicit decision, not automatic adoption of a molecular snapshot contract. |
| File handlers and `TrajectoryFile` | Resource-specific behavior; `TrajectoryFile.copy()` currently returns an empty handler. | Exclude live resources from generic resident copying. Reopening or snapshotting files is a separate I/O contract. |

The TopoMT reference separates shallow and deep analysis payload copies,
independently owns mutable registry/index containers, rebinds copied features
and registers the target in the deep-copy `memo` before descending. Its prior
registry-ownership correction is tracked by uibcdf/topomt#74. This is useful
ownership guidance, not evidence that shared editable molecular coordinates
would preserve MolSysMT's interaction-validity guarantees.

### Initial bounded public contract considered

1. `.copy()` returns an independently editable molecular snapshot. Preserve
   current calls; do not introduce `deep=False` without an agreed safe meaning.
2. `copy.deepcopy(obj, memo)` uses native hooks, registers its shell before
   traversing domains, and carries the same memo through the entire graph.
   Preserve cycles, repeated references and concrete supported subclasses.
3. One candidate for resident molecular containers is a documented domain-defined
   `copy.copy(obj)` that also isolates mutable molecular domains. It may share
   strictly immutable interaction numeric buffers, but must own analysis
   metadata and named-analysis containers independently. This is intentionally
   stronger isolation than Python's generic shallow instance fallback; it is
   not a promise of constant-time or constant-memory copying of coordinates.
   The maintainer must agree to this semantic choice before implementation.
   The reevaluation below now prefers explicit rejection of an unsafe shallow
   operation over silently paying for an independent mutable snapshot.
4. `Interactions.copy()` and its protocol hooks must preserve full/view state,
   selected occurrence indices, coverage, source maps, parallel observations,
   image vectors, provenance and lazy filtered/patched representation.
   Mutable storage independence and immutable-buffer sharing must be
   distinguished and tested. Logical independence does not require physical
   duplication of genuinely immutable bytes, even for a deep copy. Do not
   materialize a whole analysis merely to copy its small owner/metadata shell.
5. Document wrapper-specific shallow behavior explicitly. Plain Python
   dictionaries retain Python's own semantics. Do not silently present all
   serializable forms as if they owned the same domains as `MolSys`.

Private shared mechanics should allocate with `type(self).__new__`, copy state
without invoking migration hooks, and handle domain-specific owner links.
`MolSys.chemical_states` and its topology facade must refer to one copied
collection, not separate copies. A copied standalone topology must be detached
from its original owner. Rebind the owner only when copying the containing
system. A shared helper is worthwhile for common mechanics, but a generic
recursive `__dict__` copier alone cannot establish these guarantees.

Keep one validated public `.copy()` boundary, with `skip_digestion` following
the native API conventions. Python's protocol-supplied memo must not be reset
by the public convenience method. This design adds no dependency, scientific
method, Rust routine or H5MSM schema field.

## Why

Native clients need a reliable way to fork a molecular system before editing.
Today the convenience methods and the Python protocols have different
ownership, representation and subclass behavior. The existing shallow MolSys
fallback demonstrably changes the original's ownership link. A seemingly
lightweight interaction copy also goes through serialization instead of
reusing immutable storage.

## Reevaluation against the current implementation

### Client evidence

Read-only inspection of five sibling components finds the following concrete
routes. This is a bounded source study, not a complete behavioral audit or
installed-client qualification.

| Component | Observed requirement | Consequence for #121 |
| --- | --- | --- |
| DockingMT | Prepared ligands/receptors and pose conversion call `msm.copy()` before replacing coordinates. | Independent `.copy()` semantics are necessary; shared editable buffers would change the source. |
| MolSysViewer | View copying calls `msm.copy()`; source composition creates a detached candidate before mutation/publication. | Preserve independent candidate edits and the active system on failure. |
| TopoMT | `InputContext` saves/reconstructs independent molecular snapshots. `Topography.__copy__` additionally calls `copy.copy()` on each ordinary stored attribute, including native MolSys references. | Preserve independent snapshots. Changing the MolSys shallow protocol affects an existing indirect consumer, not just new code. |
| PharmacophoreMT | `copy_pharmacophore` explicitly deep-copies sites/metadata while retaining molecular references. | Analysis copying can intentionally share a source reference; this is not a request for another editable MolSys wrapper sharing coordinate buffers. |
| ElastNetMT | Inspected invariance/cache tests use `msm.copy()` before edits. No direct MolSys shallow-copy requirement was identified in inspected production code. | Preserve independent systems without inventing an unobserved shallow workflow requirement. |

**Executed client reproduction:** With a synthetic two-atom, one-structure
MolSys passed to `Topography`, `topography.copy(deep=False)` changes the
stored original MolSys topology owner to `copied._molsys`, while coordinate
buffers remain shared. This is the same provider defect already tracked by
#121, reached by a real client operation. It does not establish that TopoMT
requires a new shallow molecular-system abstraction.

### Rebinding ownership alone is insufficient

An experimental, temporary shell probe allocated a new MolSys, topology and
Structures wrapper with shared payloads and correctly separate topology owner
references. It separately copied the named-analysis dictionary. A validated
public `msm.set()` editing atom 0 in structure 0 through the clone produced:

```text
original_owner_intact: true
original_coordinate_after_clone_edit: [1.0, 2.0, 3.0]
original_evaluated_structures: [0, 1]
clone_evaluated_structures: [1]
```

The original coordinates changed but its original analysis still claimed
structure 0 as evaluated. The probe was not installed as an implementation.
The mechanism follows `Structures.set_coordinates` modifying selected rows
in place while the MolSys setter invalidates observations only on its target.
Thus the issue cannot be solved by adjusting a weak reference alone.

Reproduce this temporary shell experiment from the repository root:

```bash
python - <<'PY'
import weakref
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys

source = MolSys(n_atoms=2)
source.structures.coordinates = puw.quantity(np.zeros((2, 2, 3)), "nm")
source.interactions = {"pair": msm.Interactions.from_records(
    [{"structure_index": 0, "interaction_type": "pair", "participants": [
        {"role": "a", "atom_indices": [0]},
        {"role": "b", "atom_indices": [1]}]}],
    n_atoms=2, n_structures=2,
    evaluated_structure_indices=[0, 1], method="synthetic")}
# Experimental wrappers only; not an implementation of the proposed API.
clone = object.__new__(MolSys)
clone.__dict__ = source.__dict__.copy()
for name, original in (("_topology", source.topology),
                       ("structures", source.structures)):
    wrapper = object.__new__(type(original))
    wrapper.__dict__ = original.__dict__.copy()
    setattr(clone, name, wrapper)
clone.topology._molsys_owner_ref = weakref.ref(clone)
clone._interactions = dict(source._interactions)
msm.set(clone, selection=[0], structure_indices=[0],
        coordinates=puw.quantity([[[1., 2., 3.]]], "nm"))
print(source.topology._molsys_owner_ref() is source)
print(puw.get_value(source.structures.coordinates, to_unit="nm")[0, 0].tolist())
print(source.interactions["pair"].evaluated_structure_indices.tolist())
print(clone.interactions["pair"].evaluated_structure_indices.tolist())
# True; [1.0, 2.0, 3.0]; [0, 1]; [1] at the inspected source.
PY
```

`Structures` coordinates normally expose a non-writeable array, but their
supported setters enable writes and modify the owned buffer. That storage is
not equivalent to the bytes-backed immutable numeric storage in `Interactions`.
On the tested arrays, enabling writeability succeeds for the coordinate store
and raises `ValueError` for the interaction participant store.

### Alternatives and trade-offs

All alternatives retain independent `.copy()`/`deepcopy()` as the primary
editing route. The table concerns mutable resident molecular containers;
payload dictionaries and immutable interaction storage have distinct contracts.

| Alternative | Advantages | Costs and limitations |
| --- | --- | --- |
| A. Make `copy.copy()` an independent mutable molecular snapshot | Safe ownership/editing; existing TopoMT calls continue returning a system; straightforward implementation relative to shared-state machinery. | Stronger than the generic Python shallow contract; coordinate duplication may be large and happen indirectly; shallow/deep operations cease to express a useful payload-sharing distinction for these domains. |
| B. Share editable payloads between separately editable wrappers | Low initial numerical allocation; follows the usual shallow-sharing expectation. | Owner rebinding does not protect interaction validity; mutations can silently change the other system. Needs explicit shared lifecycle semantics or accepts loss of the required independent validity guarantees. |
| C. Explicitly reject shallow copying of mutable molecular containers | Clear failure before corruption or a hidden large allocation; `.copy()` and `deepcopy()` keep their existing independent purpose; no speculative shared-state engine. | An intentional API restriction; existing indirect callers such as TopoMT must select sharing or independent copying explicitly before rollout. |
| D. Introduce native copy-on-write or shared revision/invalidation state | Could make sharing cheap while preserving an agreed edit model. | Different models have different semantics: copy-on-write isolates edits, shared invalidation does not. Every supported write/alias route and field needs coverage; pandas alone does not cover native NumPy coordinate storage. Additional architecture and measurements are required. |

Sharing one existing MolSys by ordinary reference is already cheap and retains
one owner and validity lifecycle. It is an appropriate choice when a client
intends to share the whole molecular system. It does not create a detached
editing candidate and is not an independent snapshot.

**Earlier bounded recommendation, not accepted:** Prefer C for the six
mutable resident molecular containers (`MolSys`, `Topology`, `Structures`,
`ChemicalStates`, `MolSysBuilder`, `MolecularMechanics`), with an explanatory
protocol error pointing to independent `.copy()`/`deepcopy()`. Implement
independent native copies and explicit memo/ownership handling. Support a
lightweight copy of `Interactions` using independently owned mutable metadata
and shared genuinely immutable numeric bytes. Preserve standard shallow
payload-sharing semantics for the dictionary wrappers where no molecular
ownership/invalidation invariant is promised.

The rejection is a proposed supported restriction, not a placeholder that
pretends to implement a usable shallow molecular clone. If the maintainer
does not explicitly accept that narrower outcome for #121, the shallow-copy
part must remain open rather than being reported as delivered. If the maintainer
instead prioritizes uninterrupted existing `copy.copy()` calls, A remains a
defensible alternative, provided its payload cost and domain-defined semantics
are prominent. B is unsuitable with the current validity contract; D should
not be silently added as a small pre-1.0 copy fix.

The maintainer subsequently removed client compatibility and near-term
stabilization convenience as reasons to choose the final architecture. The
long-term direction below supersedes C as the preferred target to investigate;
it does not retroactively qualify D or promise a release date.

Before adopting C, coordinate the TopoMT call site: its shallow Topography copy
can deliberately retain the existing MolSys reference if molecular sharing is
intended, or explicitly request an independent molecular snapshot. That choice
belongs to TopoMT's owner and must be tested there. No sibling code was edited
and no new shared-suite copy policy is being asserted.

### Memory scale and immutable sharing

The following is exact buffer-size arithmetic for one resident float64
coordinate array, `n_atoms * n_structures * 3 * 8`, not measured RSS, a timing
benchmark, or an allocation of these large systems:

| Atoms | Structures | Source coordinates | Additional bytes for one independent coordinate copy |
| ---: | ---: | ---: | ---: |
| 10,000 | 1,000 | 240,000,000 | 240,000,000 |
| 100,000 | 100 | 240,000,000 | 240,000,000 |
| 100,000 | 10,000 | 24,000,000,000 | 24,000,000,000 |

The largest case requires 48 GB in decimal units for the two coordinate
buffers alone. This excludes topology, other structural series, interactions
and temporary allocations. It makes hidden snapshot semantics in an indirectly
called `copy.copy()` materially relevant. Native coordinate setters currently
normalize to float64; an external float32 input is not evidence that native
copying would need only half these bytes.

For `Interactions`, copying mutable metadata while sharing proven immutable
bytes is compatible with independent edits to the metadata. A fresh ndarray
header must protect each copy's shape/array metadata; merely sharing the exact
same ndarray object would not establish complete logical independence. A small
probe created `source.participant_atoms.view()`, reshaped the new header to
`(2, 1)` without changing the original `(2,)`, retained shared bytes and still
rejected enabling writeability. Lazy index/cache ownership also needs explicit
tests; this buffer probe does not qualify a complete copy implementation.

### External references and limits

- [Python 3.14 copy protocol](https://docs.python.org/3.14/library/copy.html)
  distinguishes shallow sharing from recursive copying, describes memo use
  and allows class-specific hooks. It also warns that deep copying can copy
  more than intended.
- [NumPy ndarray copy hook](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.__copy__.html)
  returns an array copy. This is a legitimate precedent for type-specific
  behavior, not proof that duplicating a complete molecular object graph would
  be the least surprising MolSysMT contract.
- [pandas 2.3.3 copy contract](https://pandas.pydata.org/pandas-docs/version/2.3.3/reference/api/pandas.DataFrame.copy.html)
  distinguishes deep and shallow data copying, documents copy-on-write as a
  different edit model, and does not recursively duplicate arbitrary Python
  objects inside object columns. Table copying alone is not a proof of a full
  recursive native graph contract.

These references inform API/ownership design, not a scientific computation;
there is no scientific attribution execution boundary to register with Ackredit.

## Long-term ownership and independent editing

The maintainer authorized this direction on 2026-10-21. Proceed with contract
probes and layout comparison before changing the runtime implementation.

### The distinction that determines the design

Logical independence is a user-visible property: changing one copied system
does not change the other or its interaction validity. Physical duplication is
a storage decision. A copy can share immutable data initially and separate the
changed storage before an edit. Rejecting shallow copying avoids today's defect
but does not supply this useful independent, low-allocation operation.

Given the maintainer's explicit priority for long-term design and willingness
to migrate clients, investigate D rather than freeze C as a permanent API
limitation. This is an architectural recommendation, not a measured ranking
showing that one particular block layout is optimal.

### Candidate public semantics, still for agreement

| Intent | Candidate operation | Proposed meaning |
| --- | --- | --- |
| Share the complete live object | Ordinary Python reference assignment | One system, one owner/validity lifecycle; edits are visible through both references. |
| Obtain an eager independent copy | `.copy(deep=True)` and the existing default `.copy()` | Copy mutable payloads immediately; preserve graph aliases with the native memo rules. Proven immutable storage can remain shared where the contract explicitly permits it. |
| Obtain a deferred independent copy | `.copy(deep=False)` and `copy.copy()` | Independent domain/owner handles sharing proven immutable payload storage initially; separate the affected storage before a supported write. |
| Recursively copy a containing Python graph | `copy.deepcopy(obj, memo)` | Preserve the deep-copy graph contract, including extension state, aliases and cycles; no accidental reset of the supplied memo. |

Deferred independent copying is a type-specific contract analogous to pandas'
copy-on-write behavior; it is not generic Python shallow mutation sharing.
That distinction must be prominent in docstrings and examples. The meaning of
application-owned extension attributes also needs explicit treatment; isolation
of scientific domains does not prove recursive isolation of arbitrary Python
extensions in the shallow protocol.

### Candidate internal architecture

1. Each MolSys copy has its own domain handles, named-analysis container,
   state/structure association and mutation/validity state. Do not share whole
   mutable `Topology`, `ChemicalStates` or `Structures` instances between copies.
2. Handles can refer to immutable storage shared with other handles. Within
   each system, its ChemicalStates handle remains the sole chemical domain and
   the topology compatibility facade refers to that handle. Do not duplicate
   chemical assignments or create a second source of chemistry.
3. A supported edit prepares its writable destination, validates the candidate
   and publishes changed storage through the owning domain. Stage the affected
   MolSys analysis invalidation using the existing validity rules. A geometry
   edit makes the affected structures unevaluated only in the edited branch;
   neither branch runs a detector automatically.
4. Factor preparation/publication below the public setters so native methods,
   form adapters and builders reuse one mutation mechanism. Native edits must
   not rediscover forms or call universal dispatch. Backend writes must never
   modify a shared published buffer.
5. External arrays and table access must not bypass that mechanism while the
   API promises isolation. Define protected reads, copies or explicit editing
   operations for the current mutable pandas/table routes. A direct subdomain
   edit must either notify its owner or be an explicitly detached operation;
   the existing manual-invalidation exclusions cannot silently become a claim
   of complete mutation tracking.
6. Metadata and cache ownership need their own treatment. Scientific method,
   units and provenance dictionaries must not become mutable aliases between
   independent analyses. Only proven immutable buffers may be reused; an
   ndarray's non-writeable flag alone is insufficient. Each reader/copy needs
   independent array metadata where shape changes are possible.

### Granularity is an open engineering decision

Compare detaching one contiguous field/domain with detaching affected structure
blocks. The first is simpler and keeps an eager NumPy array available, but one
small edit can duplicate the complete trajectory. Blocks can reduce that edit
cost and fit the existing chunked executor, but a request for one contiguous
array covering every structure may have to materialize all active blocks.
Repeated full-array materialization could outweigh cheap cloning and edits.

Do not promise constant-time cloning, structure-sized allocation for every
edit, or zero-copy full-array access simultaneously. Compare actual coordinate
reads, structure/atom selections, Rust consumers, iteration and H5MSM writes.
Retain the public quantity shapes and PyUnitWizard policy; changing a private
store must not silently expose bare magnitudes or a different public object.
No additional dependency or compiled backend is justified by the design alone.

The current H5MSM 0.5 scientific datasets need not encode an in-memory ownership
graph. Persistence writes the chosen system's logical values and named
analyses, using blocks where the provider supports them. That compatibility is
plausible, not verified until actual native read/write routes are tested.

### Evidence needed before choosing this architecture

- A native ownership prototype covering coordinates, a chemical-state edit,
  independent analysis metadata and owner-local invalidation. A geometry-only
  model cannot settle the complete native contract.
- Both edit directions, multiple generations of copies, partial systems,
  no-op/failed edits, captured old reads, frame coverage and occurrence identity.
- Explicit direct-table/array and external-input alias policies, including
  edits through a domain obtained before a copy was made.
- Physical allocation and timing for cloning, sparse and dense edits, repeated
  edits, selected and complete-array reads, iteration, H5MSM persistence and
  release of old branches/views. Account for initial freezing and temporary
  write buffers, not just the final replacement payload.
- Client adaptation/qualification for intentional shared source references
  versus independent editable candidates. A coherent provider contract comes
  first; existing client code may change rather than determine the semantics.

The existing interaction snapshots and TopoMT's immutable geometry snapshots
provide local examples of immutable-byte sharing and independent array headers.
They are reusable design evidence, not a drop-in general mutation engine for
Topology or Structures. The
[pandas copy-on-write contract](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
is an external reference for deferred independent edits; it does not cover
MolSysMT's native NumPy buffers or interaction invalidation. Arrow's
[columnar format](https://arrow.apache.org/docs/format/Columnar.html) illustrates
buffer locality and zero-copy trade-offs and explicitly leaves mutation
coordination to implementations. Neither reference mandates a new dependency.

## Development prototype and comparison campaign

The executable study is
[`devtools/scripts/study_native_copy.py`](../../devtools/scripts/study_native_copy.py).
Its regression module is
[`devtools/tests/test_native_copy_study.py`](../../devtools/tests/test_native_copy_study.py).
These are development tools, not exported native forms or production copy hooks.

The prototype compares three coordinate storage strategies with the same
independent-edit semantics:

- one contiguous immutable coordinate buffer, replaced on edit;
- separately owned immutable structure blocks, replacing touched blocks;
- one contiguous immutable base with block views, preserving the initial
  full-read fast path and replacing touched blocks after edits.

All contenders eagerly copy topology/chemical states, mechanics and other
structural series. Existing interaction invalidation snapshots provide separate
scientific metadata and coverage. This does not implement general
Interactions copy hooks, all-array-header isolation, native domain callbacks,
chemical copy-on-write, partial MolSys support or extension/subclass copying.
Such cases remain implementation acceptance work for #121.

The native bridge explicitly materializes editable coordinate storage before
passing it to current MolSys setters and the public H5MSM 0.5 converter. The
study checks that the bridge remains independently editable and retains a single
chemical-state authority with the correct topology owner. Its H5MSM measurement
includes complete coordinate materialization; it is not a claim of direct
block-backed native writing.

Warm operation timings and a separate traced-allocation pass cover initial
capture/freezing, coordinate-handle forks, complete prototype forks, one-atom
edits, batched/repeated edits, dense edits, nonconsecutive/repeated selections,
complete reads before/after edits, block scans and public H5MSM writes. Subject
preparation is outside individual operation timing; the combined fork/edit
case includes both. Tracemalloc is not process RSS and cannot account for all
native HDF5 or compiled allocations. Retained immutable byte owners are counted
separately from the logical slice sizes so that hybrid base retention is visible.

Run in the existing development environment:

```bash
python -m pytest --receptor=llm -n 12 devtools/tests/test_native_copy_study.py
python devtools/scripts/study_native_copy.py --case 32x9 --blocks 1,3 \
    --repeats 2 --io --output /tmp/molsysmt121-smoke.json
python devtools/scripts/study_native_copy.py --repeats 3 --io \
    --output /tmp/molsysmt121-comparison.json
```

The default matrix uses 62 atoms x 5,000 structures, 10,000 x 128 and 100,000 x
64, comparing the complete contiguous array and blocks of 1, 8 and 32 structures
with both independent and shared backing storage. Large 24 GB coordinate
systems are not allocated by this initial matrix. No timing result from these
development models alone can establish that a layout wins complete client
workflows or every chemical/structural field.

**Checkpoint (2026-10-21):** 64 study tests pass with 12 pytest workers,
including native distance calculations and H5MSM 0.5/unit assertions. The
14 fast repository gates and repository-wide Ruff checks pass. This qualifies
the development model and its measurement harness, not a public copy API.
Comparative results are recorded separately after fixing the measured source.

### Initial complete campaign

The retained artifact is
[`native_copy_20261021.json`](../../benchmarks/baselines/native_copy_20261021.json):
21 cases measured against clean source
`4e8cbad485c4757d49dc908d193d28bfdbb01c37`, with study SHA-256
`9c06847797b78fab8db09b1f603fd50cfb9a91791deeb4265445f35dde8a43c8`.
The host is an Intel Xeon E5-2630 v4 at 2.20 GHz, with 20 logical CPUs;
Python/package/platform identities and individual samples are in the artifact.
This uses the shared development environment, including the recorded development
versions of PyUnitWizard and ArgDigest; it is not a published dependency-floor
qualification. Each timing is the median of three warm samples; allocations
are from a separate execution. Temporary H5MSM files are removed after use.

For 100,000 atoms x 64 structures (146.48 MiB of float64 coordinates):

| Coordinate layout | Edit one atom, ms | New coordinate bytes, MiB | Traced edit peak, MiB | Full protected read before/after edit, ms |
| --- | ---: | ---: | ---: | ---: |
| Complete contiguous buffer | 127.269 | 146.48 | 292.97 | 0.048 / 0.126 |
| Separate one-structure blocks | 1.084 | 2.29 | 4.58 | 33.153 / 33.697 |
| Shared base, one-structure blocks | 1.126 | 2.29 | 4.58 | 0.044 / 34.890 |
| Separate eight-structure blocks | 5.129 | 18.31 | 36.62 | 35.562 / 36.899 |
| Shared base, eight-structure blocks | 5.123 | 18.31 | 36.62 | 0.046 / 36.293 |

These are prototype storage/quantity operations, not public native method
speedups. In particular, `full_read` returns a protected shared view when the
layout permits one and an assembled independent array otherwise. It is not
equivalent to a public getter promising an independently editable array.
The read-contract follow-up below separates those requirements.

Findings and limits:

- Replacing a complete array for every sparse edit is expensive in the large
  coordinate case. Block granularity changes both time and temporary memory.
- The shared-base strategy retains the initial contiguous-read fast path, but
  assembling after edits is still a full read cost. The one-structure hybrid
  result references 290.68 MiB of immutable backing bytes after replacing all
  but the last structure, versus 146.48 MiB for separate blocks. This is
  byte-owner accounting, not a measurement of process RSS or a GC experiment.
- Complete prototype forks cost about 55-59 ms in that case, despite sharing
  coordinate bytes: other domains are still copied eagerly. A cheap coordinate
  handle is not evidence of a cheap complete MolSys copy.
- Materialization plus public H5MSM writing costs about 3.9-4.2 seconds there.
  Those numbers include the current native bridge and writer; they do not
  distinguish a future streaming writer or certify one layout as faster I/O.
- Dense edits include the prototype's Python-level grouping/assignment loops.
  They are not an inherent lower bound for blocked storage and must not be
  used alone to discard it. Batched and repeated edits are separate workloads.
- A fixed number of structures per block is not yet a universal policy:
  structure size differs greatly between the three datasets. Candidate byte
  budgets and adaptive representation changes remain design work.

### Read-contract follow-up

The extended harness adds `owned_full_read`, one-structure reads with all atoms,
and nonconsecutive whole-structure reads. Owned reads duplicate a shared view
but reuse an already materialized independent output instead of copying it
again. Its ownership/CLI additions pass 71 tests, including mutation of returned
arrays without changing either branch.

```bash
python devtools/scripts/study_native_copy.py --reads-only --repeats 3 \
    --output /tmp/molsysmt121-reads.json
```

This is a separate measurement campaign because output ownership is part of
the query contract. A protected-view timing must not be presented as the cost
of an editable copy. Existing public getter behavior must be preserved or
changed explicitly, not incidentally by selecting a faster storage layout.

The separate artifact
[`native_copy_reads_20261021.json`](../../benchmarks/baselines/native_copy_reads_20261021.json)
contains 21 read cases measured against clean source
`365b9a030d19603e16232e2b0e160ee00aab3768`, with study SHA-256
`4be67b12132dce937bc15f0bd466de079ed81f89265b07051024e3e1a378db3c`.
It uses the same host/environment and timing policy as the complete campaign.
It does not repeat H5MSM writes; the artifact's I/O policy names the bridge
route, not an additional executed write qualification.

For the 100,000-atom, 64-structure case:

| Layout | Owned complete read, ms | One complete structure, ms | Four nonconsecutive/repeated complete structures, ms |
| --- | ---: | ---: | ---: |
| Contiguous | 34.385 | 2.026 | 7.351 |
| Separate blocks, one structure | 34.186 | 2.005 | 8.005 |
| Shared base, one structure | 37.022 | 2.341 | 9.168 |
| Separate blocks, eight structures | 40.247 | 2.331 | 9.534 |
| Shared base, eight structures | 36.642 | 2.387 | 9.019 |

The owned complete read has a traced peak of about 146.49 MiB in every layout:
one output coordinate array. The block prototype reuses its concatenated output
instead of allocating a second complete copy. This is why the earlier
protected-view timings must not determine the editable-output API contract.
These warm prototype measurements do not prove statistically distinct client
throughput across small differences between layouts.

### Next implementation boundary

The campaigns support pursuing independent handles over protected shared
storage, with local replacement, rather than making every small edit duplicate
all coordinates. They do not settle one universal block size or justify
discarding a storage layout solely from these development models.

Proceed with native mutation ownership and output contracts before exporting
deferred copying:

1. Preserve existing owned/editable public query results; use protected views
   only where that contract is explicit. Keep units and repeated axis selections.
2. Give each copied native domain its own owner handle and route writes through
   shared native preparation/publication machinery. Extend the prototype's
   failure and invalidation guards to real native setters; do not add scientific
   criteria or copy rules in form converters.
3. Decide the direct pandas/table access policy, old-domain-alias behavior and
   all non-coordinate series before claiming complete copy isolation. Retain
   eager copying of a field if it cannot yet be shared safely.
4. Implement native interaction copy hooks without encoding, remapping or
   materializing lazy results; preserve occurrence identity and independently
   owned mutable metadata. Extend the same memo/owner rules across MolSys,
   Topology, ChemicalStates, Structures and the other admitted native domains.
5. Keep the coordinate layout behind an internal storage contract. Compare
   byte-based granularity/adaptation and explicit retention reclamation before
   fixing defaults; native iteration/Rust/H5MSM routes need their own tests.

#121 remains active. The public `.copy(deep=False)` and molecular-container
Python copy hooks are not implemented by the storage study, and the existing
generic shallow MolSys owner defect is not yet fixed. The 71 development guards
and 42 comparative cases qualify the storage evidence, not a completed library
rollout or release candidate. The interaction-specific boundary below is now
implemented separately.

## First resident boundary: interaction copies

**Implemented and contract-tested:** `Interactions.copy(skip_digestion=False)`,
`copy.copy(analysis)` and `copy.deepcopy(analysis)` allocate a concrete-type shell
without invoking constructors, restoration, interchange, remapping or packing.
The public native method uses the existing ArgDigest result boundary; Python
protocol hooks accept their standard protocol arguments. A private helper owns
the representation-specific mechanics, not form adapters or the universal
dispatcher.

The helper shares numeric bytes only after following a NumPy array's backing
chain to an immutable `bytes` owner. A nonwriteable flag alone is not accepted
as evidence. It creates separate array headers, detaches mutable arrays/query
indexes, copies nested metadata and retains the original lazy graph. Filtered
roots, replacement segments and existing packed caches receive independent
analysis handles. Missing packed caches remain missing. The source's handles,
headers, cache state, metadata and validity are unchanged by copying or by
querying the copy. No coordinate sharing mechanism is introduced here.

Python's standard copy memo preserves repeated analysis/metadata references,
cycles, concrete subclasses and extension slots. Mapping proxies receive their
own backing dictionaries while preserving graph aliases. Slot reads do not
invoke normal constructors, inference or migration. Writable extension arrays
are copied rather than trusted as protected data.

### Raw-column memo boundary

**Reproduced and guarded limitation:** a standard NumPy `deepcopy(column)`
produces mutable storage. If an enclosing graph copies a raw protected column
before the analysis referring to it, the existing memo replacement cannot both
retain that exact earlier object and satisfy protected analysis storage. The
implementation raises `TypeError` instead of silently accepting the mutable
replacement. `deepcopy([analysis, analysis.participant_atoms])` preserves the
alias safely; the reverse order is explicitly rejected. This boundary is
documented and tested. It is not a claim of order-independent copying for every
arbitrary graph containing raw arrays. Revisit the storage-handle/public-array
exposure design before extending the guarantee; do not remove the rejection
without a real ownership solution.

### Verification scope

The production guard is `tests/interactions/test_copy.py`. It covers complete,
reordered query, invalidated, invalidated-query and replaced analyses; parallel
occurrences; compound participants; periodic vectors; source maps; evaluated-empty
and unevaluated structures; producer/execution metadata; independent headers,
query indexes, extension slots and memo cycles. It forbids constructors,
encoding/decoding, remapping and lazy packing during copy. H5MSM 0.5 round trips
the copied full analysis under an angstrom/ns application policy while retaining
declared nm measurement values and occurrence identity. Query views remain
queries; copying does not make them attachable as full named analyses.

Foundations, Toolbox, Cookbook and the Common Core specialized-domains module
now explain the analysis-specific guarantees and their limits. This phase adds
no dependency, scientific method, attribution boundary, schema field or release
candidate. Existing scientific attribution metadata is copied as stored rather
than registering a new calculation with Ackredit.

Local qualification on 2026-10-21, Linux/Python 3.14.7 in the existing development
environment:

- 74 interaction-copy cases are included in a 378-test focused run covering the
  sparse result lifecycle, native MolSys/chemistry associations, public copy,
  H5MSM 0.5 and the 71 storage-prototype guards. The run used
  `python -m pytest --receptor=llm -n 12` and passed in 17.92 s. One existing
  `StructuralAttributeDropWarning` reports the deliberate partial-charge drop
  in a concatenation test; no test failed or was skipped.
- All 11 result-module doctest items passed, including the three copy entry
  points. The added Toolbox and Cookbook copy examples were executed against
  their page's synthetic construction blocks.
- All 14 fast repository gates passed. Ruff checks and formatting passed for
  the production package and the added guard; the public docstring validator,
  developer-guide/index checks and course structure validator passed.
- Course code cells are unchanged; the new explanation and reference were
  added to its interaction overview. No installed-client matrix, native
  complete-system performance qualification or release gate is inferred from
  this focused run.

## Second resident boundary: protected Structures

**Implemented:** `Structures.copy(deep=True, skip_digestion=False)` retains eager
coordinate/box allocation by default. `deep=False` and Python `copy.copy()` create
independent geometry handles over protected blocks. Python `copy.deepcopy()`
uses eager geometry allocation and the enclosing memo. Every mode eagerly
detaches other mutable series, alternate-site and biological-assembly metadata.
Concrete supported types, ordinary extension state, slots, cycles and repeated
domain references survive without constructor/restoration calls.

Coordinates and boxes use `_StructureArray` in `molsysmt/native`. Inputs are
converted explicitly to nm float64 and frozen in independently owned byte
buffers without changing caller array flags or retaining writable aliases.
An internal initial budget of 1 MiB chooses the number of complete structures
per block; a structure larger than that budget remains one block. This is a
provisional implementation detail behind the storage boundary, not a proven
universal optimum or a public tuning parameter. There is no hidden complete
contiguous base that retired blocks keep alive.

Selected getters read only pertinent blocks, preserving nonconsecutive and
repeated axes, and return owned editable arrays. Native/form-agnostic queries,
attribute presence, counts, native iteration and selected extraction use the
same storage route. Full coordinate/box properties are read snapshots and may
assemble the complete series; full editable getters likewise need a complete
output array. Arbitrary internal NumPy coercion/indexing and current full-axis
append/add operations remain explicit materialization boundaries. No zero-copy
whole-array promise is inferred from deferred copies.

The H5MSM 0.5 codec uses storage metadata and row views rather than coercing the
complete protected geometry to a NumPy array. Write/append slices are bounded
by both storage blocks and the codec's row limit. Reads capture canonical nm
float64 blocks directly from selected HDF5 rows before constructing the resident
domain, avoiding an additional complete coordinate staging array. Full contiguous
reads use dataset slices; nonconsecutive/repeated selections retain their order.
The file schema, declared units and resident-data memory requirement are unchanged.
The guard forbids dense native projection and rejects geometry dataset reads or
writes larger than its small block budget, including the constant-box append
check. This is not a disk-backed native domain or a new public direct-file query API.

Selected setters construct replacement blocks before publishing a new storage
handle. Repeated indices use explicit last-assignment semantics. Empty selected
axes do not replace storage. Failed validation or failure while allocating a
later replacement block leaves the old storage intact. Whole structure-payload
replacement now prepares all owned series before dictionary publication, avoiding
a second eager coordinate copy and preventing a failed append from publishing
only some series. This is the standalone domain boundary; MolSys's existing
conservative invalidation context still publishes unevaluated coverage on a
delegation failure.

The representation-neutral shell/memo/proxy helper moved from
`interactions/_copy.py` to `native/_copy.py` because both resident types now use
it. It does not own domain attachment or rebind molecular owner references;
each domain must supply those rules. The ordinary `deep` Boolean digester is
reusable by subsequent native copy boundaries.

The production guard `tests/native/test_structure_copy.py` asserts protected
block sharing/replacement, eager allocation, input/output alias independence,
non-default units, repeated axes, failure atomicity, subclass/memo semantics,
H5MSM/pickle and native/Rust selected geometry without a full dense read.
Existing box-initialization guards now check read protection and immutable
backing buffers rather than requiring the old private ndarray representation.
The ordinary MolSys independent-copy test edits through its supported native
setter instead of relying on the old deep-copy fallback accidentally making a
read-only property writable. The declared protected property behavior is
unchanged; eager native copies now preserve it consistently.

Geometry oracle and direct Rust-boundary fixtures now explicitly obtain NumPy
coordinate arrays, retaining analytical values, nonmutation/read protection and
the original strided Rust input. They no longer assume the private geometry
handle itself is an ndarray or add ndarray-like flags/operators solely to
satisfy an obsolete representation check. The parallel-control protection test
uses deterministic values and checks actual immutable buffers and read snapshots.

The expanded persistence run also exposed an independent constructor/codec
bioassembly mismatch, now tracked as uibcdf/molsysmt#396. Copy tests use existing
schema-compatible native metadata and do not claim to fix that normalizer.
The older state-only info expectation is aligned under uibcdf/molsysmt#128.

Foundations, the basic-copy Toolbox page, the sparse-interaction Cookbook and
Common Core modules 4 and 20 now distinguish eager/deferred standalone geometry,
independent analysis metadata, owned output arrays and pending whole-MolSys
integration. No H5MSM schema version, dependency, scientific criterion or
Ackredit calculation boundary changes.

### Structure-boundary qualification

On 2026-10-21 in the existing Linux/Python 3.14.7 environment:

- The first hosted smoke run for `300c31990` failed at the signature guard:
  the intentional `Structures.copy` extension lacked its scoped declaration.
  The registry now names the accepted #121 arguments, unchanged eager default
  and ownership guard; the validator itself is unchanged. Ruff, developer-guide
  integrity and both governance checks passed on that source. This failed run
  is not counted as smoke qualification.
  The scoped declaration subsequently passed smoke in `efd827560`
  (run `39683171377`, inspected with `gh-run-receptor`).

- `python -m pytest --receptor=llm -n 12` over native domains, native/H5MSM form
  adapters, public copy/iterator/append/add/conversion routes, sparse lifecycle,
  vector/plane/distance/PBC geometry and the storage-study guards passed all
  **1,724 cases** in 78.09 s, with no omissions. The receptor retained 799 warnings
  in 16 groups: predominantly expected legacy-file notices, plus deliberate
  incompatibility/drop/GPU/memory-budget probes and existing pandas/unit notices.
- The 22 native-copy cases also pass after strengthening eager/deferred
  persistence with an actual coordinate edit under an angstrom/ns application
  policy and independent literal nm expectations. The final additional case
  verifies full coordinate initialization and explicit property-based removal;
  the validated setter continues to require a quantity. These are ownership and
  I/O contracts, not a complete-system speed/RSS benchmark.
- All 15 Structures/Interactions result-module doctest items passed; all 14 fast
  gates, package/changed-test Ruff checks and formatting, public docstring
  validation and course/developer-guide checks passed. The added Cookbook variant
  executes with its explicit synthetic setup. Changed course/Toolbox cells are
  explanatory Markdown; executable cells remain unchanged.
- Client-installed matrices, complete scientific suites, complete MolSys owner
  hooks and a release/package qualification are not inferred from this scope.

## Client coordination

At the maintainer's request, uibcdf/molsyssuite#122 owns the cross-component
contract/adoption coordination. Owner-local notices are:

- uibcdf/topomt#97: the existing Topography shallow path reaches the provider
  owner defect; preserve registry/feature ownership and decide molecular input
  reference versus snapshot semantics.
- uibcdf/dockingmt#51: ligand/receptor/pose variants must preserve their input
  systems and retained preparation evidence.
- uibcdf/molsysviewer#259: qualify view/composition independence, named analyses,
  geometry editing and session/persistence behavior.
- uibcdf/pharmacophoremt#60: retain intentional live molecular references in
  pharmacophore copies and request explicit editable molecular variants where needed.
- uibcdf/elastnetmt#28: preserve snapshot, geometric invariance and model/cache
  validity responsibilities.

The opening notices pin the delivered Interactions checkpoint
`85b8b038008de4b6ac05e6f6c3e5028935bd3f85`, identify complete-system work as pending,
and request owner-local qualification only when that provider boundary is ready.
They do not change source/dependency pins, claim installed-client qualification,
authorize publication or introduce another release blocker. Component checkouts
were refreshed read-only before the handoff: TopoMT is diverged, DockingMT,
PharmacophoreMT and ElastNetMT lag their remotes, and Viewer has unrelated active
work. Those branches, worktrees and source files were preserved.

## Third resident boundary: molecular ownership

**Implemented:** `MolSys.copy(deep=True, skip_digestion=False)` retains eager
geometry allocation by default. `deep=False` and Python `copy.copy()` seed
independent coordinate/box storage handles over proven immutable blocks before
copying the native graph. Python `copy.deepcopy()` propagates the caller's memo
and eagerly copies geometry. Both modes detach canonical tables, other mutable
series, mechanics data, named-analysis handles and ordinary extension metadata.
The universal `msm.copy(molsys)` keeps its registered-form dispatch and eager
default; native hooks do not register arbitrary subclasses as universal forms.

The molecular hook binds the copied topology's weak owner to the new system.
The topology hook excludes its old owner before traversing fields, rather than
removing it after recursion: when an explicit extension points back to an
enclosing MolSys, that enclosing copy can bind the topology during the same
memo traversal. Roots at the system, topology, chemistry or mechanics preserve
the same copied objects. Merely having a weak owner link does not clone its
source system when copying a standalone topology.

Topology and experimental mechanics Python hooks copy current state without
their serialization restoration hooks. ChemicalStates and private state records
use their ordinary constructor-free Python deep-copy route. The single memo
preserves one copied ChemicalStates collection behind both molecular and
topology access, nullable structure/state associations and explicit cycles.
Absent topology, chemistry or structures remain absent; no default domain is
synthesized. No constructor, remap, inference, interchange or dense coordinate
projection is required by these hooks. Analysis caches and lazy filtered/patched
representations retain their existing copy contracts and producer metadata.

Geometry edits through `msm.set` invalidate affected structures in each copied
analysis, including evaluated-empty structures and atoms with no old interaction.
The original system's geometry, ownership and evaluated coverage remain intact;
held result/query snapshots remain unchanged. Chemistry replacement on the copy
retains its single authority and invalidates only that copy's named analyses.
This does not add observation of direct attached-domain/table writes.

`tests/native/test_molsys_copy.py` supplies 57 cases across Python shallow/deep,
native eager/deferred and universal base-form copying. Guards cover domains and
canonical table values/dtypes, direct ownership, actual angstrom-valued geometry
edits, full/filtered/patched analyses, source maps and parallel handles, partial
domains, memo ordering/cycles, a native subclass with slots, failed allocation,
invalid allocation modes and H5MSM/pickle restoration. Native constructors,
restoration, remapping, lazy packing and dense geometry projection are forbidden
while the relevant copies execute. The native subclass fixture uses trusted
construction; it does not qualify subclass constructor digestion or automatic
registration as a universal form.

**Contract-tested:** Linux/Python 3.14.7, existing development environment,
`python -m pytest --receptor=llm -n 12`: **3,397 passed**, no omissions, in
81.14 s. Scope: native domains, MolSys/Topology/Structures and H5MSM adapters,
public copy, iteration, append/add/multi-input conversion, sparse copy/validity/
replacement, vector/plane/distance/PBC geometry and copy-study/API-guard tooling.
The receptor retained 801 warnings in 16 groups, predominantly legacy H5MSM
notices plus existing/deliberate compatibility, pandas, unit, GPU and memory
policy probes. This is not a full scientific or installed-client qualification.
All **19 doctest items** across MolSys/Structures/Interactions and all **14 fast
gates** passed. The signature registry names the optional MolSys extension and
its owning guard; the signature validator itself is unchanged.

Foundations for molecular domains, Toolbox copy/interaction pages, the sparse
Cookbook and Common Core modules 4/20 now describe molecular eager/deferred
copying, current edit boundaries and unchanged analysis identity. This adds no
dependency, scientific calculation/attribution boundary, file schema or release.

## Fourth resident boundary: remaining classes and payloads

**Implemented:** `Topology.copy`, `ChemicalStates.copy` and
`MolecularMechanics.copy` now use the constructor-free Python graph protocol,
with validated keyword-only `skip_digestion=False`. They preserve stored
tables, reference selection, history, producer reports, ordinary extension
metadata, concrete supported subclasses and graph aliases. Their canonical
tables still copy eagerly, and they expose no ineffective `deep` selector.
The private chemical-state convenience copy also preserves current state
without constructor validation/normalization.

`MolSysBuilder.copy(deep=True, skip_digestion=False)` retains eager geometry
allocation by default. Its deferred mode and Python shallow hook use independent
handles over protected coordinate/box blocks; tables and other mutable fields
detach in both modes. Copying does not compile a builder, synthesize parents or
normalize incomplete declarations. `n_structures` now delegates to the stored
Structures axis metadata rather than assembling the coordinate property.

MolSys, Structures and MolSysBuilder share a private helper that seeds deferred
geometry handles. Convenience methods without geometry share the small native
helper for independent copying and strict validation of the delegation flag,
including truthy non-Boolean values that a decorator might otherwise bypass.
These helpers do not discover forms, validate schemas or rebind domain owners.

`MolSysDict`, `TopologyDict`, `ChemicalStatesDict`, `InteractionsDict` and
`ViewerJSON` now detach mutable payload data under native and both Python copy
operations. Frozen numeric bytes may remain shared through independent array
headers. Compression/schema descriptors and ordinary wrapper extensions survive
the graph copy, but this adds no persistent schema fields. Unlike these wrapper
instances, plain dictionary forms keep Python's shallow `dict.copy()` semantics.
Copying is not admission, decoding, remapping or proof of JSON serialization.

Registered MolSysDict, TopologyDict, ChemicalStatesDict and InteractionsDict
forms lacked public `copy` adapters: `msm.copy` raised AttributeError despite
their native methods. Four small adapters now delegate to the validated native
boundary. A separate plain MolecularMechanicsDict adapter incorrectly used
`dict.copy`; it now deep-copies nested parameters, arrays and quantities as the
universal copy contract promises. A two-case guard reproduced both universal
and direct-adapter aliasing before that fix. Schema keys and form names remain
unchanged.

The initial 86-case remaining-family probe had 59 failures on the preceding
source: unsupported delegation arguments, lost extension/subclass state,
shared payloads and dense builder counts. The final
`tests/native/test_remaining_copy.py` has 97 cases covering nine resident/wrapper
families, convenience/Python protocols, graph memo aliases, slots, invalid
flags, incomplete staging and actual angstrom-valued edits. Registered native
reconstruction is checked for the four molecular/typed payloads; generated
ViewerJSON value copying and serialization of an independently JSON-safe
payload are separate checks.

Those additional interoperability probes exposed two independent, pre-existing
ViewerJSON defects: native reading rejects alphabetic chain IDs
(uibcdf/molsysmt#397), and generated bond scalars can be NumPy integers rejected
by JSON encoding (uibcdf/molsysmt#398). Both reproduce without copying. They
were reported separately; their codecs were unchanged at that copy checkpoint.
Subsequent corrections and their independent guards are recorded under #397/#398,
now resolved. Their qualification does not extend the copy benchmark or imply
lossless graphics persistence. The independent atom-subset extraction defect
is now resolved under #399, with its own route and memory-boundary guards.
Direct legacy-bond import and bond queries were subsequently reconciled under
#400. Those separate codec fixes do not extend native copy guarantees or provide
a multi-set chemical-state mapping.

**Contract-tested:** in the existing Linux/Python 3.14.7 environment,
`python -m pytest --receptor=llm -n 12` passed **3,676 cases** in 83.24 s, with
no omissions. Scope extends the third-boundary campaign to Builder, all five
payload-wrapper form adapters and the plain mechanics-dictionary adapter.
The receptor retained 847 warnings in 17 groups, mainly legacy H5MSM notices
and existing/deliberate atom-name, compatibility, pandas, unit, GPU and memory
policy probes. All 18 doctest items in the nine changed native modules and four
new copy adapters passed; all 14 fast gates, scoped signature-drift declarations,
Ruff checks, formatting and public docstring checks passed. Updated plain
mechanics-dictionary and sparse-payload Cookbook examples execute successfully.
The registered scientific suite and installed-client/package matrices are not
inferred from this source-level scope.

**Additional consumer qualification:** unchanged runtime source `6614f13fc`
also passed 204 tests in 31.54 s for chemical-template application, connectivity,
context/selection, stereochemistry, receptor/EST preparation, fixed-state
hydrogens, preparation history and partial-charge assignment. These routes use
the changed state/mechanics copies directly. A separate 14-case aromatic
bond-order normalization run passed in 5.28 s. Both used
`python -m pytest --receptor=llm -n 12` in the same environment with no omissions;
the 204-case run retained 34 existing pandas/drop warnings. No runtime changes
were made after these or the broader qualification. The exact source commit's
five hosted checks passed, including smoke run `39700026715`, inspected with
`gh-run-receptor`; the other four checks were inspected as a receptor aggregate.

Foundations includes a cross-family copy table, Builder staging behavior,
wrapper contracts and the corrected plain mechanics-dictionary schema. Toolbox,
Cookbook and Common Core modules 4/20 reflect the distinction between native
domains, payload wrappers and plain Python dictionaries. No scientific method,
attribution execution boundary, dependency, schema version or release is added.

### Remaining native integration

Do not close #121 on this boundary. The geometry checkpoint below closes direct
attached coordinate/box setter publication; other domain edits and the
pandas mutation/alias policy remain open. Canonical tables currently copy eagerly
and inherit pandas' handling of arbitrary Python objects in cells and table
metadata; their wrapper/subclass preservation also needs a deliberate contract.
Simulation settings and live resource handlers retain their separately stated
reference/I/O semantics. The general native helper remains private: molecular
owner rebinding belongs to its domain hook, not a generic state copy.
The production campaign below now measures resident memory/time/read/edit and
persistence on fixed synthetic systems. It does not establish an optimal block
budget. The subsequent H5MSM checkpoint measures and addresses the observed
I/O/allocation costs without qualifying all workloads.
Client-installed/source adoption evidence is not inferred from provider tests.

### Production resident campaign — 2026-10-21 local / 2026-10-22 UTC

**Benchmarked:**
[`benchmark_native_copy.py`](../../devtools/scripts/benchmark_native_copy.py)
executes the implemented native objects, not the earlier experimental `_Branch`
layouts. The
[raw snapshot](../../benchmarks/baselines/native_copy_resident_20261021.json)
records base `6e11395a976a2e0a2a3c8e046185a07aa131165a`, the dirty development
worktree, exact tool/runtime-file hashes, raw samples and package versions.
All recorded implementation hashes matched the files after the campaign.
The dirty changes were the new benchmark, its tests and documentation; no
runtime implementation changed during measurement. The existing Python 3.14.7
development environment includes source builds of some support libraries; this
is not published-dependency or installed-client qualification.

Reproduce from the repository root:

```bash
python devtools/scripts/benchmark_native_copy.py --repeats 3 \
    --output /tmp/native-copy-resident.json
python -m pytest --receptor=llm -n 12 \
    devtools/tests/test_benchmark_native_copy.py
```

The campaign used Linux on an Intel Xeon E5-2630 v4 at 2.20 GHz, about 32.9 GB
physical RAM, and temporary files on `/tmp` tmpfs (16 GiB capacity). OMP,
OpenBLAS, MKL and Rayon thread environment variables were fixed to one. Each
case/operation has a fresh subprocess, one same-shape warm-up, three untraced
timing samples and a separate allocation-tracing pass. The small correctness
suite completed near controller startup; no further test or benchmark campaign
was launched during measurement. Do not rank small latency differences from
this development run. The filesystem cache is warm/uncontrolled;
these are not physical-disk throughput or cold-start measurements. See the
[operational guide](../benchmarking/native_copy.md) for operation boundaries,
fixture and memory definitions.

Median times, rounded; atoms × structures name each column:

| Operation | 62 × 5,000 | 10,000 × 1,000 | 100,000 × 100 |
| --- | ---: | ---: | ---: |
| Deferred `MolSys.copy(deep=False)` | 1.84 ms | 2.36 ms | 6.40 ms |
| Eager `MolSys.copy()` | 2.54 ms | 155.41 ms | 152.53 ms |
| Edit one atom in one structure, including invalidation | 2.31 ms | 3.54 ms | 2.72 ms |
| Batched edit in eight structures, including invalidation | 2.58 ms | 4.71 ms | 15.43 ms |
| Two atoms / four explicitly ordered structure indices | 0.80 ms | 0.74 ms | 0.79 ms |
| Full coordinate property | 1.30 ms | 55.83 ms | 52.13 ms |
| All-coordinate iteration plus checksum, chunk 32 | 32.95 ms | 259.96 ms | 294.09 ms |
| Public Rust distance calculation, two atoms / all structures | 10.11 ms | 9.01 ms | 4.98 ms |
| Public complete-system H5MSM write | 0.278 s | 34.280 s | 19.624 s |
| Public complete-system H5MSM resident load | 0.170 s | 8.663 s | 5.188 s |

Copy/edit geometry accounting, decimal MB; these are unique immutable backing
bytes, excluding tables, analyses, metadata and allocator overhead:

| Geometry footprint | 62 × 5,000 | 10,000 × 1,000 | 100,000 × 100 |
| --- | ---: | ---: | ---: |
| Original coordinates + box | 7.800 MB | 240.072 MB | 240.007 MB |
| Additional geometry for deferred copy | 0 MB | 0 MB | 0 MB |
| Additional geometry for eager copy | 7.800 MB | 240.072 MB | 240.007 MB |
| Additional geometry after one-atom edit of deferred branch | 1.048 MB | 0.960 MB | 2.400 MB |
| Additional geometry after eight-structure batch | 1.048 MB | 1.920 MB | 19.200 MB |

The current 1 MiB budget produces 704, 4 and 1 structures per coordinate block
respectively. One 100,000-atom structure exceeds that budget and remains a
complete 2.4 MB block. Deferred copies still allocate independent canonical
tables/metadata: their traced operation peaks are 0.111, 0.961 and 8.948 MB;
the corresponding eager-copy peaks are 7.912, 240.791 and 245.804 MB. These are
incremental allocations traced separately, not total process RSS. RSS before,
retained-result and worker high-water counters are in the JSON with their
explicit lifetime limits. Releasing an object does not promise immediate OS
reclamation of allocator arenas.

**Contract-tested:** all ten benchmark operations pass their small-fixture
guards (**16 tests**, no omissions, 12 workers). Every measured sample checks
values/units, owner bindings, chemical authority, original-source isolation,
evaluated-empty/unevaluated coverage and parallel occurrence identity outside
timing as applicable. The validator rejects intentionally stale coverage after
a direct-domain edit, and rejects incorrect coordinates. It therefore does not
accept a cheaper edit that silently bypasses owner invalidation. No scientific
detector, attribution method, dependency floor or file schema changed.

#### Findings and next implementation boundary

1. **Measured:** deferring geometry allocation benefits the larger resident
   snapshots while preserving independent mutable tables and domain ownership.
   In the 10,000 × 1,000 case it reduces this copy's median latency by about
   66-fold; the 62-atom case benefits much less. This is a local result for
   these payloads, not a universal ratio or zero-RAM-copy claim.
2. **Measured:** full coordinate properties allocate about 240 MB in the large
   cases. Selected queries remain small; chunk-32 iteration traces peaks of
   16.854 MB and 160.820 MB for the two 240 MB trajectories. Atom count and
   structure count both matter when choosing an iterator chunk.
3. **Measured / inspected:** public H5MSM write/load costs require a separate
   I/O refinement before performance closeout. The writer passes protected
   coordinate blocks of 4 or 1 structures to HDF5, whose installed automatic
   chunk chooser gives temporal extents 32 or 4 for the two large dataset
   shapes. A metadata-only diagnostic with h5py's chooser gives chunk shapes
   `(32, 313, 1)` and `(4, 3125, 1)`. Repeated partial compressed-chunk access
   is a plausible mechanism; this has not yet been isolated against an aligned
   layout. Compare aligned layouts on write, full load, selected reads and file
   size before choosing a fix. Preserve bounded transfers and the existing
   schema/units; do not optimize only the write case.
4. **Measured / inspected:** public resident load traces 482.608 MB and
   501.228 MB for the large cases. The codec's protected reader is bounded,
   but `basic.convert` first materializes the file through
   `maybe_read_modular_h5msm` and then uses the native same-form converter,
   whose default `copy_if_all=True` takes another eager snapshot. This is a
   concrete candidate for the extra resident allocation. Qualify a fresh-file
   ownership path separately, preserving explicit user copy choices, selections,
   partial-domain behavior, owner links and named analyses. The current benchmark
   does not establish a lower public-load allocation bound.
5. **Still open:** no budget sweep proves 1 MiB optimal; no dense-interaction,
   large mutable-observable/metadata, installed-client or other-platform campaign
   is implied. General pandas/table alias policy and automatic publication of
   direct attached-domain edits remain design work. Keep #121 active.

### H5MSM fresh-load ownership boundary — 2026-10-21 local

**Implemented / contract-tested:** `basic.convert` now recognizes a single
H5MSM 0.5 path materialized by its reader. For one `molsysmt.MolSys` output,
the default native conversion reuses that fresh independent resident graph
instead of taking a second eager snapshot. The ordinary converter still
validates options, performs selections/remapping and returns conversion reports.
Explicit `copy_if_all=True` requests the additional snapshot; explicit False
remains supported. Existing resident inputs retain their independent-copy
default. Lists/composed inputs, multiple outputs, legacy files and conversion
to other forms retain their existing routes and ownership semantics.

Guard:
`tests/basic/convert/one_to_one/test_h5msm05_load_ownership.py`. Twelve
parameterized guards reject an extra MolSys deep copy on the original
`460b3e5bf` source, across full/partial domains and string/Path input. Additional
cases protect explicit copy choices, existing resident ownership, independently
edited repeated loads, non-default output units, nonconsecutive selection/source
maps, parallel occurrences, coverage, preflight reports and argument rejection.
Multiple MolSys outputs must still own distinct topologies.

The focused integrated campaign passed **841 tests**, no omissions, using
`pytest-receptor` and 12 workers; its 644 warnings are expected legacy H5MSM
deprecations. Scope: the new guards, complementary H5MSM composition, all
`tests/form/file_h5msm`, native Structures/MolSys copy guards and the public
interaction/H5MSM workflow. No schema, units or scientific-method changes were
made. This is source-level Linux evidence, not installed/client qualification.

The chunk-layout comparison follows this reader correction. It retains
automatic HDF5 layout as an explicit reference even if the runtime default
later changes. The bounded study compares 64 KiB, 256 KiB and 1 MiB aligned
coordinate chunks with complete xyz tuples. A separate larger run compares
the provisional 256 KiB compromise with the original automatic layout on both
240 MB coordinate cases. The larger results and any production adoption belong
to a subsequent dated checkpoint; they are not inferred from the small study.

### H5MSM layout adoption and production remeasurement — 2026-10-21 local

**Benchmarked:** the
[bounded layout study](../../benchmarks/baselines/h5msm_structure_chunks_20261021.json)
compares automatic coordinates with complete-xyz 64 KiB, 256 KiB and 1 MiB
chunks on 62 × 512, 10,000 × 128 and 100,000 × 16 fixtures. Each case/layout
uses a fresh worker, one warm-up, three timed samples and a separate traced
pass. `study_h5msm_structure_chunks.py` changes only the physical coordinate
dataset chunks in that worker and retains the original auto control. Public
write/load include the complete system; two selected reads use the private
structures codec with fresh file handles. The synthetic fixture, units,
hardware and warm-cache limitations match the operational guide.

The 1 MiB candidate improves bulk transfer but worsens the two-atom private
query on the 100,000-atom fixture (22.68 ms versus 9.79 ms automatic).
64 KiB is faster for that query (6.07 ms), but 256 KiB balances it against file
size and full transfer (9.34 ms; 22.89 MB versus 26.31 MB with 64 KiB).
These timings do not prove a universal optimum. The provisional **256 KiB**
choice was then compared with automatic layout on the two 240 MB coordinate
cases, using two timed samples per operation:
[large controlled snapshot](../../benchmarks/baselines/h5msm_structure_chunks_large_20261021.json).

| Larger control | 10,000 × 1,000: auto → aligned 256 KiB | 100,000 × 100: auto → aligned 256 KiB |
| --- | ---: | ---: |
| Public complete-system write | 33.992 → 5.240 s | 19.853 → 5.587 s |
| Public complete-system load, fresh-load fix in both arms | 8.620 → 0.984 s | 4.892 → 1.543 s |
| Private complete-structure read | 35.29 → 4.51 ms | 43.32 → 11.95 ms |
| Private two-atom/four-structure read | 11.06 → 7.39 ms | 12.22 → 9.21 ms |
| Whole H5MSM file | 97.684 → 81.033 MB | 110.389 → 88.665 MB |

The automatic chunks were `(32, 313, 1)` and `(4, 3125, 1)`, compared with
`(1, 10000, 3)` and `(1, 10922, 3)`. Changing only coordinate layout while
holding the reader fix constant isolates the layout contribution. In both
arms, the public-load traced peaks were about 242.582 MB and 259.748 MB,
respectively: eliminating the extra native snapshot accounts for the reduction
from the original approximately 482.608/501.228 MB peaks; chunk alignment
primarily changes access cost and file size. This does not mean total RSS
halved: the original benchmark source, imports and other resident data remain
outside the incremental traced-operation peak.

**Implemented / contract-tested:** new 0.5 coordinate datasets now use this
bounded aligned layout. The private `_coordinate_chunks` helper belongs to
the existing structures codec; there is no public tuning parameter, new
schema, dependency or scientific method. Boxes and other series retain their
existing layout. Empty axes retain automatic HDF5 handling; readers accept
old automatic layouts. Appends preserve a dataset's existing chunks and can
touch partial edge chunks. The native 1 MiB geometry storage budget is unchanged.

`tests/form/file_h5msm/test_geometry_chunk_layout.py` checks actual raw chunk
bytes, whole xyz tuples and alignment of observed write boundaries under two
different small transfer budgets, with and without compression. Its four
layout guards fail on the old writer because real chunks exceed the configured
bound. It also forbids full protected-array assembly during write, append and
codec read, then verifies selected values/units after an unaligned append and
checks both empty-axis cases. The study keeps an independent experimental
chooser to reproduce alternatives; it is not an alternate runtime provider.

**Production remeasurement:** the original resident benchmark tool was rerun
with only its public H5MSM write/read operations and two timed repetitions:
[refined snapshot](../../benchmarks/baselines/native_copy_h5msm_refined_20261021.json).
This run uses the default runtime writer, without a dataset-creation override:

| Public runtime operation | 62 × 5,000 | 10,000 × 1,000 | 100,000 × 100 |
| --- | ---: | ---: | ---: |
| Write | 0.217 s | 5.243 s | 5.742 s |
| Resident load | 0.130 s | 0.951 s | 1.532 s |
| Incremental traced load peak | 8.626 MB | 242.582 MB | 259.747 MB |
| Whole H5MSM file | 3.553 MB | 81.033 MB | 88.665 MB |

The raw snapshots retain commit/dirty-state and file hashes. The controlled
studies used the fresh-load correction whose code is preserved in `760ea1905`,
before the later explanatory docstring addition. The refined production run
records that addition and the final codec/Structures hashes. Tool versions and
measured source bytes are recoverable without treating the base commit as the
entire dirty measured worktree. The layout and refined campaigns ran sequentially
without other benchmark/test campaigns during worker measurements. Support-library versions
remain development sources where recorded; none of these measurements qualifies
an installed release, other platform, cold physical disk or arbitrary chemistry.

Final integrated scope passed **881 tests**, no omissions, with 12 workers and
`pytest-receptor`; the 644 warnings are expected legacy deprecations. This adds
the physical-layout and study/benchmark guards to the fresh-load campaign.
The revised `convert` and `Structures.copy` docstrings pass **20 doctest
examples**. Foundations, Toolbox, Cookbook and course Module 04 explain the
resident load/copy distinction. Notebook code cells and saved outputs are
unchanged; no notebook execution claim is inferred from prose edits.

**Remaining #121 decisions:** direct attached-domain edit publication,
pandas/table alias and mutation policy, representative large mutable observables
and dense-analysis workloads, live-resource scope and installed-client adoption.
The observed H5MSM bottlenecks are addressed for the measured boundary; keep
the general issue active rather than calling native copying fully qualified.

### Historical ownership defect

The following probe reproduced the defect at the initial inspected source
before the molecular hooks. The current guard instead requires independent
topologies and unchanged original ownership; it must not reproduce these old
printed results. Run from the repository root at that baseline:

```bash
python - <<'PY'
import copy
from molsysmt.native import MolSys

source = MolSys(n_atoms=2)
assert source.topology._molsys_owner_ref() is source
clone = copy.copy(source)
assert clone.topology is source.topology
print(source.topology._molsys_owner_ref() is source)  # False at inspected source
print(source.topology._molsys_owner_ref() is clone)   # True at inspected source
PY
```

This is observable before any coordinate or bond edit. It is covered by this
copy-ownership theme rather than a second duplicate issue.

### Reproducing interaction reconstruction at the inspected baseline

This historical probe describes the source before the interaction hooks above;
it no longer reproduces reconstruction for current `Interactions` copies.

```bash
python - <<'PY'
import copy
import numpy as np
from molsysmt import Interactions

source = Interactions.from_records(
    [{"structure_index": 0, "interaction_type": "pair", "participants": [
        {"role": "first", "atom_indices": [0]},
        {"role": "second", "atom_indices": [1]},
    ]}], n_atoms=2, n_structures=2,
    evaluated_structure_indices=[0, 1], method="synthetic")
for operation in (copy.copy, copy.deepcopy):
    clone = operation(source)
    print(np.shares_memory(source.participant_atoms, clone.participant_atoms))
    print(clone.participant_atoms.flags.writeable)
# False, False for each operation at the inspected source.
PY
```

## What is measured and what is assumed

**Executed:** On small synthetic systems, generic shallow MolSys copying
reassigns the shared topology's owner; ordinary `.copy()` and `deepcopy()`
isolate coordinate buffers in the inspected examples. Editing a bond on the
shallow clone changes the original's bond table as expected from the sharing,
but ownership has already changed even without that edit.

**Executed:** Copying full, queried, invalidated and replaced interaction
results through both Python operations reconstructs numeric storage. The
queried example preserves occurrence order `[2, 0]`; the tested invalidated
and replaced results become ordinary `Interactions` objects. Their source
`_packed_result` remains absent after a fresh copy operation. Do not describe
this as a retained source cache or as measured occurrence-index corruption.

**Executed:** A minimal trusted construction of a `MolSys` subclass followed by
`.copy()` returns base `MolSys`, whereas `deepcopy()` preserves the subclass.
Custom application attributes on `MolSys` are discarded by its manual copy;
the generic deep copy preserves a test cycle and a repeated chemistry alias.
Those custom attributes are an extension-design observation, not a claim that
all arbitrary application payloads are currently supported scientific data.

**Inspected:** `Topology.__setstate__` contains migration and chemistry
normalization; `get_substructure_matches` already constructs a private
inventory view explicitly to avoid that shallow-copy restoration behavior.
Revisit this consumer after the new protocol is proven; do not remove the
workaround merely because hooks have been added.

At the initial diagnosis checkpoint, no representative timing, RSS/peak-memory,
large-trajectory or installed-client benchmark had been run for #121. The later
development campaigns above now provide bounded storage-layout measurements.
They do not qualify native complete-system copying or installed clients, and
the production interaction-copy guards establish ownership rather than a new
end-to-end performance ranking.

## What was refuted

- A plain Python shallow instance copy is already safe: contradicted by the
  owner-link reproduction.
- Reusing `remap()` is equivalent to copying: it is an index transformation,
  rejects query views and reconstructs relations/occurrences. Copy hooks need
  their own invariant-preserving native route.
- Serialization reconstruction is a harmless universal copy backend: it can
  execute migration logic, allocate columns and change lazy representation.
- A shallow molecular copy can share editable coordinates while independently
  guaranteeing interaction freshness: existing edit operations invalidate the
  edited owner, not every possible alias owner. A shared invalidation graph or
  copy-on-write engine would require a separate design and evidence.
- Every Python object under `native` should receive identical copy behavior:
  resident data, payload wrappers, configuration and live file resources have
  different ownership contracts.

## Scope and exclusions

First implement the seven resident data types and their interaction lifecycle;
then reconcile the five payload wrappers. Preserve partial and explicitly
absent domains. Decide the protocol semantics before adding signatures or
changing user documentation to promise them.

The implementation scope is pending the long-term design decision; native
copy-on-write is now a candidate to investigate under #121 rather than an
automatic post-1.0 exclusion. Do not silently introduce shared mutable views,
a general dependency tracker, file-resource cloning, another chemical store,
interaction compaction/remapping, or a new scientific detector.
Simulation and file-resource behavior stays an explicit follow-up, not an
unqualified claim that all native types are complete.

## Acceptance criteria

- Public calls preserve expected values, units, IDs, exact indices and partial
  domain presence; invalid options fail at the public validation boundary.
- Copying leaves the original's ownership, data, coverage and lazy state intact.
- Molecular edits through an independent copy invalidate only that copy's named
  observations. The original's coordinates and analyses remain unchanged.
- Standalone topology copies have no original MolSys owner; complete system
  copies bind the copied topology to the copied system and preserve the single
  chemical-state collection behind the compatibility facade.
- A shared memo preserves graph aliases and cycles; supported subclasses retain
  their type and extension state without calling ordinary constructors.
- Interaction hooks preserve parallel occurrence identity, reordered query
  views, invalidated/replaced results, metadata and periodic geometry. Assert
  independent mutable data/array metadata and safe immutable-byte sharing
  directly; a deep copy need not duplicate proven immutable bytes.
- The accepted `__copy__` contract either provides its documented ownership
  guarantees or rejects the operation before touching the source. If C is
  chosen, qualify the affected TopoMT route before rollout.
- If deferred independent copying is adopted, qualify every promised mutation
  and alias boundary before advertising it. Measure the storage granularity
  against real read/edit/persistence workloads; an isolated geometry prototype
  does not establish native-library support.
- No form discovery, inference, migration, encoding or disk I/O is needed to
  copy an ordinary resident object. Copying a lazy result does not pack it.
- Focused memory/timing probes use fixed data sizes and account for the allowed
  shallow sharing separately from full independent mutable storage.
- NumPy docstrings, native Foundations, Toolbox, Cookbook and the relevant
  course sections explain the chosen semantics with executable examples.

## Provenance

Inspected MolSysMT `3d47650271ea518042419b24de1a108a187415c4` and TopoMT
`c3f72a9177ab8a205b69fefc2963800a2d0b4feb` on 2026-10-21. Local probes used
Linux, Python 3.14.7, NumPy 2.4.6 and pandas 2.3.3 in the existing development
environment. TopoMT was read only. No runtime implementation was changed during
that initial source-inspection checkpoint; the interaction implementation above
was added in the subsequent phase on the same date.

The final reevaluation additionally inspected DockingMT
`7275377152d515792d4c971d3de7798a33e09b72`, MolSysViewer
`1d3fa6eddec5f06f21dee1e925445114c67fec38`, PharmacophoreMT
`a1ea9cc4025fefdbff5e30f3ecced2bcdfacd83d` and ElastNetMT
`8a54148945fa98df3b5c62c6152575eda08f32c3`. The consumer/sharing probes ran
against MolSysMT `1cf296319455526c548b5f9f99592dfac6d7e02a` in the same local
environment on 2026-10-21. Source observations do not qualify installed clients
or any replacement release candidate.

A bounded `suite_status.py` refresh of these five clients found local branch
divergence/lag in TopoMT, DockingMT, PharmacophoreMT and ElastNetMT, and unrelated
uncommitted documentation/sandbox work in MolSysViewer. All worktrees and branch
states were preserved. Read-only comparison against fetched `origin/main`
confirmed that the client copy routes cited above had no remote differences;
this study does not qualify other newer client code.

### Independent assembly boundary follow-up — 2026-10-22

The public-construction mismatch found during persistence qualification is
resolved separately under [uibcdf/molsysmt#396](../archive/resolved_bugs/validated_native_bioassembly_operations_cannot_round_trip_through_h5msm_0_5.md).
Assembly validation now retains operation arrays and unit-bearing translations,
without mutating caller metadata. Analytical direct/named/loaded assembly tests
also exercise the extraction consumer. This does not resolve #121's remaining
direct attached-domain mutation or table-alias decisions.


### Attached geometry publication — 2026-10-22

**Implemented:** A native `Structures` wrapper attached to `MolSys` has one weak
owner. `set_coordinates`, `set_box` and complete coordinate/box property
assignments prepare protected storage before publication, then stage the owner's
existing per-structure interaction invalidation. Calls through a domain alias
or `msm.set(molsys.structures, ...)` follow the same path. Every named analysis
loses occurrences and evaluated coverage on affected structures, including
previously evaluated-empty structures and atoms with no previous observations.
No scientific detector runs. Other structures, producer metadata, index maps
and previously obtained result/query snapshots survive.

The preflight reads lengths and shapes, without assembling protected geometry.
Partial writes still replace only affected storage blocks. Invalidation allocation
failure, invalid units/shapes/selections and incompatible attached-analysis axes
leave a direct native edit unpublished. Public `msm.set(molsys, ...)` retains its
conservative failure-after-delegation policy for extensions that may partially
write. Nested public/native invalidation reuses staged snapshots instead of
allocating them twice; broader nested scopes contribute to the same final
publication, including when delegation subsequently fails.

Standalone domain copies and pickles omit the weak owner. Complete native
copies and MolSys pickle restoration rebind the copied/restored domain to its
own system. Restoration accepts the former public `structures` state key.
Assigning an already attached domain to another MolSys copies its wrapper and
mutable metadata using deferred geometry allocation; it does not steal the
original owner or duplicate all coordinate bytes. Replacing a domain detaches
the previous wrapper. A retained domain does not keep its owner alive. Resident
representations read the new private storage key without validation or payload
materialization.

**Guard:** `tests/native/test_structure_owner.py` protects selected/nonconsecutive
and repeated edits, empty selections and evaluated-empty coverage, full native/
property/form assignment, clearing geometry, invalid dimensions/units/selections,
snapshot-allocation failure, eager/deferred owner isolation, weak lifetime,
standalone/system pickle and legacy restoration, H5MSM restoration, nondefault
unit policy, forbidden dense geometry access, one invalidation per analysis
through public delegation and nested scope/failure publication.

**Qualified locally:** The complete selection of `tests/native`,
`tests/form/molsysmt_MolSys`, `tests/form/molsysmt_Structures`,
`tests/form/file_h5msm` and `tests/interactions` passes **2,885 tests** with
Pytest Receptor and 12 workers, without omissions (41.69 s). Its 681 visible
warnings cover legacy H5MSM, intentional tiny-memory-budget probes, pandas
migration, unknown synthetic atom names and existing structural merge policies.
The 37 focused owner tests include one corrected test that originally passed
`indices` to native `get`, whose public contract uses `selection`; the final
full run uses the corrected query. Native ownership docstrings pass 16
examples. Ruff over the package and new guards, all 14 fast release gates,
public docstring fidelity and public signature stability pass. These are local
source checks, not installed-client or final-release qualification.

User Foundations, Toolbox,
Cookbook and Common Core modules 4/10/20 describe the same notification boundary;
notebook code and saved outputs remain unchanged. No dependency, scientific
method, attribution requirement, H5MSM schema or release identity is added.

**Still open under #121:** Whole-domain replacement and direct domain append/add
are outside this automatic notification boundary. Use coordinated MolSys
extraction/append/add for aligned axis changes. Other direct chemistry/table
mutations still need explicit owner invalidation; no array/DataFrame observer
or chemical dependency graph is implied. General table alias/subclass/object
cell policy, large mutable observable/resource workloads and installed-client
adoption remain outstanding. Do not close #121 on this checkpoint.


### Controlled chemical publication and authority ownership — 2026-10-22

**Implemented:** Chemical-state atom and scientific bond setters invoked on an
attached topology now notify the owning MolSys, including
`msm.set(molsys.topology, ...)`. Native bond addition/removal, full bond-table
replacement, and controlled component-membership assignment use the same staged
invalidation. Every covered structure in every named analysis becomes
unevaluated, including evaluated-empty structures and edits to atoms that had
no previous occurrence. Editing an explicitly selected nonreference chemical
state also uses this conservative all-structure rule. No detector runs and no
per-analysis chemical dependency graph is inferred.

Atom-column, bond-table and membership candidates are validated before
publication. An invalid partial atom assignment cannot materialize a new
missing-valued column before reporting its error. Failed input validation and
invalidation-allocation failure preserve chemical values and analyses. Bond
addition/removal rebuilds components after bond publication; a subsequent
rebuilding failure can leave the new bond table published, with analyses already
invalidated. Empty requests are no-ops. Bond IDs are labels: comparing scientific
columns excludes them without making two whole-table copies. Previous table
handles do not follow replacement. Nested MolSys/topology delegation reuses
staged invalidation and does not repeat it per analysis. Coordinate/box storage
is neither copied nor materialized by chemical publication.

Native bond tools now use ArgDigest and their existing `skip_digestion` argument.
Their native-boundary digesters reject malformed/noninteger/Boolean indices.
The decorators declare this context explicitly, so inherited bond methods keep
their validation contract when a subclass lives in another module; other form
routes retain their previous digestion behavior. The private storage
normalizer prepares canonical typed atom tables independently before publishing
instead of mutating a live partial column and validating afterward. Scientific
criteria and physical-unit conventions are unchanged.

**Ownership:** ChemicalStates has one weak MolSys owner, retained through the
single collection referenced by the system and topology facade. Attaching a
collection already owned by another system copies mutable chemistry instead of
sharing it between owners. Chemistry-only partial systems follow the same rule.
Replacement detaches the previous collection. Standalone copies and pickles omit
the weak link; complete system copying/restoration rebinds it. A retained
collection does not retain its former molecular system. Serialization retains
supported subclass slots. This is eager chemical-table independence, not table
copy-on-write. It adds no competing chemistry store.

**Guard:** `tests/native/test_topology_owner.py` covers real ionic observations,
evaluated-empty/unevaluated coverage, sparse provenance/maps and earlier views,
direct native/form chemical changes, bond labels and empty requests, malformed
and invalid writes, prepublication allocation failure, postpublication component
failure, nonreference states, component membership, standalone/system copy,
pickle/H5MSM restoration, cross-owner collection attachment, weak lifetime,
partial systems and slotted state serialization. Its geometry spies reject both
protected-array materialization and copying during chemical assignment.

**Qualified locally:** The final aggregate passes **4,246 tests**, without
omissions, with Pytest Receptor and 12 workers (58.34 s). Its selection is
`tests/native`, `tests/form/molsysmt_Topology`, `tests/form/molsysmt_MolSys`,
`tests/form/molsysmt_Structures`, `tests/form/file_h5msm`, `tests/interactions`
and `tests/topology`. All 47 focused owner tests pass. The 695 visible warnings
cover legacy H5MSM, deliberate low-memory probes, pandas migration, synthetic
unknown atom names and existing structural merge policies. All 14 fast release
gates, package/new-test Ruff, public docstring fidelity and signature stability
pass; native chemical ownership docstrings pass 16 examples. These are local
source checks, not installed-client or final-release qualification.

The expanded topological consumer tests use existing network-backed PDB examples: a sandbox run waited
in `download_with_retries` and was interrupted, rather than counted as passed.
The same consumer suite passed 1,314 tests when executed with network access;
its inputs and expectations were unchanged. The existing development environment
is used throughout. User Foundations, Toolbox, Cookbook and Common Core modules
4/10/20 describe the current boundaries. Course code and saved outputs are
unchanged. Ackredit is not applicable to these storage/validation changes;
scientific algorithms, producer provenance, dependency floors, H5MSM schema and
release identity are unchanged.

**Distinct finding:** Ordinary inherited constructors of externally declared
ChemicalStates/MolSys/Topology subclasses reject valid atom counts. This was
reproduced separately and reported as [uibcdf/molsysmt#404](https://github.com/uibcdf/molsysmt/issues/404).
The slotted serialization fixture uses known-valid trusted construction, as the
existing native subclass copy fixtures do; this is not evidence that ordinary
subclass constructor dispatch works. Resolve caller/receiver validation under
that owning issue without weakening native argument checks.

**Still open under #121:** Direct writes to DataFrames/Series/arrays,
other private ChemicalStates collection/record mutations, whole-domain replacement
and direct structure-domain axis changes are not observed by this boundary. Their callers
must invalidate explicitly or use a coordinated owning operation. Table
alias/subclass/arbitrary-object policy, large mutable observable/resource
workloads and installed-client adoption remain outstanding. Keep #121 active.


#### Preserving connectivity declarations during publication

Final review of the shared bond publisher found that construction-only
`reset_bonds(n_bonds=...)` must not inherit the valid-edge setter's promotion
from unavailable to partial connectivity. Empty reserved rows are not known
edges. Selected bond removal must also retain the original completeness flag,
as before this refactoring. Both routes now explicitly publish without
introducing a new connectivity declaration; actual validated bond replacement
retains the original partial-availability behavior. Added guards are
`test_reserving_empty_bond_rows_does_not_claim_known_connectivity` and
`test_removing_bonds_preserves_the_declared_connectivity_completeness` in
`tests/native/test_topology_owner.py`. This is part of #121's scientific-behavior
preservation, not a new chemical inference method.


### Chemical-state inventory publication (2026-10-22)

**Reproduced:** Public `ChemicalStates.append_state()` changed an attached
collection without invalidating its MolSys analyses. Eleven of the 16 new
regression cases failed before the correction. Adding a state can change the
interpretation of structures without explicit state associations, even when
coordinates stay fixed.

**Implemented / contract-tested:** The common append operation validates the
new record and prepares a list of state references before staged publication.
An attached collection marks every named analysis unevaluated, including
previously evaluated-empty structures. The first state becomes the reference;
later states preserve the reference. Explicit structure-to-state assignments
are unchanged. An absent association resolves to unknown when multiple states
exist; the append operation does not choose or assign a new state. Standalone
collections have no owner to notify. Repeated appends reuse already invalidated
analyses, and retained result/query snapshots remain historical snapshots.

No existing state record, chemical table or coordinate payload is copied.
Preparing the new reference list costs O(number of states) references; this is
not a new constant-time collection or a table copy-on-write design. Failure to
construct the new record or prepare invalidation preserves the collection and
original analysis handles. Appending preparation history still archives detached
evidence without applying chemistry, so attached analyses remain valid.

**Guard:** `tests/native/test_chemical_states_owner.py` covers empty/single/multiple
state inventories, nullable explicit and implicit structure associations,
prepublication allocation failure, geometry/state copy rejection, standalone
copies, system copy/deepcopy/pickle/H5MSM ownership, chemistry-only partial
systems, detached history and repeated invalidation. The nonreference-state
chemical-edit guard in `tests/native/test_topology_owner.py` now reattaches valid
analyses after setup, so the new inventory invalidation cannot hide a missing
notification from the subsequent edit.

**Qualified locally:** **4,262 tests passed**, without omissions, using Pytest
Receptor and 12 workers in the existing development environment (54.53 s).
The scope is native classes, native Topology/MolSys/Structures and H5MSM form
adapters, interactions and topology tools. The 694 visible warnings fall into
eight groups: legacy H5MSM reads, deliberate memory-budget probes, pandas
migration, synthetic unknown atom names and existing merge policies.
Foundations, Toolbox, Cookbook and Common Core modules 4/10/20 explain inventory
publication versus historical evidence; notebook code and saved outputs are
unchanged. Ackredit is not applicable to this storage lifecycle correction.
Scientific criteria, producer attribution, physical-unit policy, dependency
floors, H5MSM schema and release identity are unchanged.

All 14 fast release gates, package/new-test Ruff, public docstring fidelity
(247 functions) and public signature stability pass. ChemicalStates docstrings
pass 17 doctest examples. A direct comparison confirms that course modules
4/10/20 retain identical code cells, execution counts and saved outputs.

**Still open:** #121 retains its remaining alias/subclass/arbitrary-object and
resource-workload decisions and installed-client adoption. Raw record/table
writes, other private inventory operations and uncoordinated domain replacement
still require explicit owning invalidation. This phase does not close #121 or
qualify a release artifact.
