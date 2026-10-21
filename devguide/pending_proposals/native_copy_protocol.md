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
and public signatures are not frozen; no native copy-on-write API is delivered
for complete molecular systems yet. `Interactions` and standalone `Structures`
now provide resident copy boundaries, described below. Their complete-system
owner coupling remains pending.

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

### Remaining native integration

Do not close #121 on this boundary. `MolSys.copy()` still reconstructs domains
and remaps analyses; its generic Python shallow fallback still steals the
topology owner. Molecular-container copy hooks, owner/edit publication, pandas
mutation/alias policy, whole-system use of shared-coordinate storage, other resident types
and payload wrappers remain pending. The interaction helper is deliberately
private and ownership-neutral while other domains establish compatible
ownership semantics. Their hooks must propagate one memo, but a generic state
copier alone cannot rebind molecular domain ownership correctly.

### Reproducing the ownership defect

Run from the repository root in the existing development environment:

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
