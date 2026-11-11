(user-foundations-performance-chunked-execution)=
# Chunked Execution

Chunked execution processes supported molecular structure sequences in coordinate blocks. Each operation has its own input, selection, and output limits; streaming coordinates does not guarantee that its complete result fits in RAM.

---

## The Memory Wall Problem

A single-precision coordinate array for a 1-million-atom system across 10,000 structures occupies approximately 120 GB of RAM. Loading such a system using standard eager allocation exceeds the memory capacity of most workstations.

MolSysMT's canonical coordinate buffers use float64, so the same array occupies approximately 240 GB. Supported operations can read selected coordinate blocks instead of materializing the whole sequence.

---

## Eager Path vs. Heavy Path

MolSysMT manages execution through the `ChunkedExecutor` engine:

- **Eager Path**: The selected coordinate array is loaded into RAM and supplied to the reducer in one block.
- **Heavy Path (`ChunkedExecutor`)**: For large structure sequences, MolSysMT streams coordinate blocks in bounded chunks, passes each chunk to the analysis kernel, and accumulates partial results iteratively.

---

## Controlling Execution (`heavy_mode`)

The public chunked route is available for `get_center`, `get_rmsd`, `get_distances`, `get_radius_of_gyration` and `get_rmsf`, subject to each function's supported combinations. The experimental ionic detector also accepts a keyword-only `heavy_mode`, supporting native MolSys and H5MSM 0.5 paths with integer atom-index selections or `'all'`.

### Session Configuration vs. Function Override

```python
import molsysmt as msm

# 1. Global session configuration
msm.configure.chunk_size = 500       # Set global chunk size to 500 structures
msm.configure.max_ram_usage = 8 * 1024**3 # Numeric working budget in bytes

# 2. Per-function call argument override
# Auto mode: MolSysMT decides based on estimated memory footprint
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='auto')

# Force chunked path explicitly for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='force')

# Force eager path for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='off')
```

Configuration sets working estimates rather than an operating-system memory cap. `auto` selects a route using input footprint estimates; ionic calculation also considers its selected coordinate workspace. Unsupported combinations either retain their documented eager route or fail
explicitly; `force` is not a universal out-of-core guarantee.

## Owning disk-backed results

When a supported operation returns a disk-backed result handle, manage its
lifetime with a context or explicit `cleanup()`. Automatically created backing
files are removed on cleanup and on failed mapping construction. A path supplied
by you stays under your control and is not deleted by those operations. Cleanup
errors propagate so that failed disk retirement remains visible. Avoid copying
the complete result into RAM unless it fits your working budget.

## Keeping length observables consistent

Radius of gyration and RMSF use canonical nm coordinates inside their reducers.
The returned lengths are converted to the active PyUnitWizard standard, preserving
physical values across eager, automatic and forced execution. Changing units
changes numerical magnitudes and labels together. Radius-of-gyration weights
remain aligned with the selected atoms. Repeated structure indices contribute
repeated observations to RMSF; the tool does not align structures automatically.

## Distance endpoints and output storage

Flat atom populations within one system retain their own memberships on the
heavy route, including unequal population sizes. Explicit structure lists are
paired positionally with equal lengths; they are not a Cartesian product of
structures. The second endpoint is read only for the current first block when
its structure list differs. PBC uses the first endpoint box. Numeric nm blocks
are converted to the active length standard before storage.

The scalar output shape is the selected structure count × first population
size × second population size. It is preallocated in RAM or stored in a
`PersistentResultHandle` if its numeric size exceeds the configured budget.
A quantity can therefore have a disk-backed magnitude. Access that magnitude
in blocks and release it with `cleanup()` after use. The estimate is not a
process-RSS cap: input metadata, the caller's source and runtime caches remain
separate. A single pair slab must fit the numerical work budget; atom-axis
tiling is not implemented. Centers, explicit atom pairs and two-system
calculations retain the existing eager route.

## Ionic analyses and H5MSM 0.5

For supported file calculations, the ionic detector prepares topology, chemical states, and association metadata once, without reading all coordinates or stored analyses. It then projects eligible participant atoms in blocks. Atom-axis identity must be declared, and structure-assigned chemistry must resolve to one known state for the selected structures.

The complete `Interactions` result remains in memory. Coordinate, candidate, and sparse-result working estimates are checked separately; they exclude caller-owned coordinates, full chemistry tables, runtime caches, and Python object overhead. Conservative candidate bounds can reject a calculation even when actual contacts are sparse. There is no incremental result writer or checkpoint/resume interface for this detector.

See {ref}`Getting ionic interactions <Tutorial_Get_ionic_interactions>` for an executable comparison of eager and chunked execution, and {ref}`Saving ionic interactions <Cookbook_Saving_ionic_interactions>` for recalculating directly from H5MSM 0.5 and saving a named analysis. Choose eager execution when the selected input and result fit comfortably; use blocks to control coordinate workspace when necessary. Smaller blocks can add I/O and orchestration cost.

---

## Custom Chunking Scripts with Iterators

If you need to program a custom analysis script or building pipeline that processes large structure sequences in chunked blocks, you do not need to rewrite low-level file parsing. You can build custom chunked execution loops directly using MolSysMT's `Iterator` objects:

```python
import molsysmt as msm

# Stream a large file in chunks of 200 structures
iterator = msm.Iterator('large_system.h5msm', chunk=200, coordinates=True)

for chunk_index, coordinates in enumerate(iterator):
    # Process each chunk of coordinates independently with custom logic
    print(f"Processing chunk {chunk_index} with shape {coordinates.shape}")
```

Requesting coordinates or other attributes explicitly avoids converting stable
domains for each chunk. With no explicit attributes, native `MolSys` and
`Structures` outputs are independently owned selected conversions. Geometry,
other observations, chemical-state associations and named-analysis maps follow
the selected structure positions together, including a shorter final chunk.
Keeping an earlier native chunk does not make it change when you advance;
keeping every chunk can still materialize trajectory-sized data. Other output
forms retain their existing reusable-container behavior. See
{ref}`Tutorial_Iterator` for both output styles.

---

## Memory Pressure Monitoring

MolSysMT integrates with **SMonitor** to track Real Resident Set Size (RSS) memory pressure during execution. If RAM consumption exceeds `molsysmt.configure.memory_pressure_threshold`, a `MemoryPressureWarning` is emitted, allowing workflows to adapt dynamically.

## Sparse searches still need a budget

The native positive-cutoff cell search bounds head tables by reference
population (at most four heads per reference atom), coarsening cells when
necessary. Coarser cells only broaden the candidate search: the requested
inclusive distance criterion and reduced-cell minimum image remain unchanged.
Empty spatial volume and smaller valid cutoffs do not create unbounded grids.

The selected numeric input blocks, retained grids, row bookkeeping, controlled
thread scratch and actual observed CSR entries have checked working estimates
against `configure.max_ram_usage`. Output is charged after a query's actual
neighbor count is known, rather than rejecting sparse queries by their maximum
possible pairs. Packed/per-query output coexistence is included. A refusal
raises public `msm.MemoryBudgetExceededError` (catalog MSM-ERR-HVY-003), without
changing the source or scientific criterion. Checked size overflow and
unsupported native allocation also fail before that allocation.

This numerical allowance is not process RSS, an operating-system cap or a
resource reservation. Native/source domains, unit/coordinate preparation and
foreign-library allocations have their own costs. The eligible cell search
still receives the selected structures eagerly; this does not make all neighbor
queries streaming. Dense/fixed-count fallbacks retain their separate contracts.

Boolean contact maps remain dense resident results. Their storage is reserved
before native search; eligible search and filling share the remaining allowance.
Using a sparse candidate search does not make a dense map sparse. See the
{ref}`neighbor tutorial <Tutorial_Get_neighbors>` and
{ref}`contact tutorial <Tutorial_Get_contacts>`.


## Compatibility output

Neighbor/contact output also needs memory beyond the numerical search. Default
threshold neighbor arrays retain a view header and object slot for each row of
indices and distances. These costs are admitted before native search, and the
PyUnitWizard constructor retains distance views without per-row multiplication
copies. Eligible `get_neighbors(..., output_type='csr')` avoids those row objects.

Contact pair output still requires a dense Boolean map. Its actual pair count,
Python lists/integers, label arrays and bounded packing slabs are admitted before
boxing; conversion avoids whole-map triangular and pair-array intermediates.
These estimates remain separate from allocator arenas, runtime initialization,
source domains and RSS. Use smaller Iterator/selection blocks for a refused
representation. Dense-distance fallbacks have their own execution policy.

## Observed secondary-structure assignments

{func}`molsysmt.structure.get_secondary_structure` retains complete backbone
context while selecting output groups. Its native/H5 heavy path uses the shared
executor, with ordered/repeated source structures and an admitted resident U2
label array. Eager foreign forms retain their public conversion route; force
or large requests without a registered chunk contract are refused. This is
MDTraj DSSP assignment, without implicit periodic reconstruction, and its normal
float32 provider coordinates apply. Output/topology/foreign-runtime costs remain
explicit; the numerical estimate is not total RSS or a resource reservation.
