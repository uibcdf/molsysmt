# Proposal: Native DCD and XTC trajectory I/O

**Status:** proposed and re-scoped (2026-07-15).
**Decision:** consolidate MolSysMT first; evaluate DCD before XTC.
**Expected effort:** DCD medium; XTC high.
**Expected impact:** high for dependency independence, streaming, and startup reliability.

## 1. Objective

Evaluate and, if the evidence is favorable, implement MolSysMT-owned readers
for DCD and XTC trajectories. The readers must deliver the existing MolSysMT
structural contract directly: coordinates with shape
`(n_structures, n_atoms, 3)` in nm, boxes with shape
`(n_structures, 3, 3)` in nm, and time in ps.

This proposal does not approve an immediate rewrite. MDTraj and MDAnalysis
remain independent readers and compatibility oracles until the native backend
passes all acceptance gates. Existing adapters remain available as fallbacks
during migration.

## 2. Why this is worth evaluating

The current `file:dcd` and `file:xtc` paths delegate parsing and iteration to
MDTraj objects. This gives MolSysMT mature format support, but it also means:

- core trajectory access depends on an optional third-party parser;
- MolSysMT does not control cursor ownership, indexing, or resource lifetime;
- intermediate objects and unit conversions can add allocations;
- parser behavior and supported variants can change outside MolSysMT;
- a parser failure may be reported through another library's exception model.

On 2026-07-15, a curated XTC conversion exposed a concrete ownership defect:
coordinates, time, and box were read sequentially from the same stateful MDTraj
handle, so the first full read exhausted the cursor and later attributes were
empty. The adapter was corrected to preserve its cursor and conversion was
changed to use one read. This bug does not prove that a native parser will be
better, but it demonstrates the value of owning and testing the complete I/O
contract.

## 3. Why DCD comes before XTC

### 3.1 DCD feasibility

DCD is a record-oriented binary format and is the lower-risk first target. A
reader still has to handle real variants rather than one nominal layout:

- little- and big-endian records;
- standard and CHARMM/NAMD headers;
- fixed-atom trajectories where applicable;
- optional periodic-cell records and their differing conventions;
- 32-bit record markers and safe overflow checks;
- truncated records, inconsistent atom counts, and missing frames;
- efficient sequential iteration and indexed frame access.

A small Python reference parser can establish the format contract. A production
reader may then move to Rust if profiling shows a material gain in throughput,
memory use, GIL independence, or packaging reliability.

### 3.2 XTC complexity

XTC is not just an array of float coordinates. A conforming reader must decode
the GROMACS/XDR representation, including compressed integer coordinates,
precision metadata, variable-size frame payloads, bit packing, small-difference
encoding, boxes, steps, and times. Random access requires a trustworthy frame
offset index or a scan; arbitrary frames cannot be assumed to have fixed byte
offsets.

For that reason, XTC should begin as a specification and corpus study. A
production implementation is better suited to a memory-safe compiled backend,
with Rust as the leading candidate, than to a large pure-Python bit decoder.

## 4. Architecture

The backend should fit the existing form system instead of introducing a new
public molecular-system form solely for implementation details.

```text
file:dcd / file:xtc
        |
        v
MolSysMT-owned reader ---- optional established-reader fallback
        |
        +-- metadata: n_atoms, n_frames, time, box
        +-- read_frames(indices, atom_indices)
        +-- iterator(start, stop, step, chunk)
        +-- close / context manager
        |
        v
molsysmt.Structures or ChunkedExecutor payloads
```

The reader API must have explicit ownership semantics:

- construction opens or maps the file;
- context-manager exit and `close()` are idempotent;
- metadata queries do not silently consume the frame cursor;
- random reads either preserve the sequential cursor or document cursor change;
- iterators close resources they own and never close borrowed readers;
- errors use catalog-backed MolSysMT diagnostics with the original cause.

The first implementation should return contiguous NumPy-compatible buffers.
Apache Arrow is not a prerequisite: trajectory coordinates are dense numeric
tensors, and adding a columnar layer must be justified independently by a
measured consumer benefit.

## 5. Delivery plan

### Phase 0: corpus and contract

1. Inventory bundled DCD and XTC artifacts and their writer provenance.
2. Add small generated fixtures for each supported variant where redistribution
   is permitted.
3. Record hashes, atom/frame counts, step, time, box, and coordinate precision.
4. Define resource ownership, random-access, truncation, and corruption behavior.
5. Benchmark current MDTraj-backed eager and chunked paths as the baseline.

### Phase 1: DCD read-only reference backend

1. Parse header and record markers with strict bounds checks.
2. Detect endianess and supported CHARMM/NAMD flags.
3. Read coordinates, optional cells, and selected frames.
4. Implement `n_atoms`, `n_structures`, iteration, `seek`, `tell`, and `close`.
5. Convert units at one explicit boundary into canonical nm and ps.
6. Reject unsupported variants with a precise diagnostic rather than guessing.

### Phase 2: DCD production decision

Compare the reference backend with a Rust/PyO3 prototype. Adopt Rust only if it
provides a meaningful advantage after wheel size, build complexity, startup,
and maintenance cost are included. Keep the Python parser as executable format
documentation if it remains small and trustworthy.

### Phase 3: XTC feasibility spike

1. Implement only frame-header and offset scanning first.
2. Validate the index against at least two independent readers.
3. Decode a minimal uncompressed/small-coordinate case, then compressed frames.
4. Fuzz malformed lengths, integer ranges, and truncated bit streams.
5. Measure whether native decoding materially improves the current adapter.

Only after this phase should a full XTC backend be approved.

### Phase 4: integration and optional writing

Read support must stabilize before writers are considered. A writer adds
precision-policy, compatibility, and reproducibility decisions and therefore
needs a separate acceptance review. If approved, native readers become the
preferred `file:dcd` or `file:xtc` route while established libraries remain
explicit compatibility backends for at least one release cycle.

## 6. Scientific and compatibility validation

Every supported format variant must be checked against independently read data:

- coordinates, frame order, atom subsets, and arbitrary frame subsets;
- boxes, including orthorhombic and triclinic cases;
- steps and time in ps;
- eager versus chunked parity;
- cursor preservation and repeated metadata access;
- truncated, corrupt, empty, and atom-count-mismatched files;
- file-descriptor stability under repeated open/read/close cycles.

MDTraj and MDAnalysis should both be used where they independently support the
variant. Agreement between a new Rust implementation and a MolSysMT Python
prototype is implementation parity, not independent scientific truth.

Numerical tolerances must follow source precision and writer behavior. The
reader must not claim a universal dtype or precision for all DCD or XTC files.

## 7. Benchmarks and go/no-go criteria

Measure cold and warm startup, sequential throughput, sparse-frame access,
atom-subset access, peak resident memory, allocations, file descriptors, and
wheel size. Use at least a small file, a representative trajectory, and a file
large enough to exercise chunking.

Proceed with DCD production integration only if all correctness gates pass and
at least one of these is material without a serious regression elsewhere:

- lower hard/soft dependency burden for core reading;
- at least 1.5x representative throughput;
- at least 25% lower peak memory;
- demonstrably safer resource and corruption handling;
- removal of a significant startup or packaging constraint.

Proceed from XTC feasibility to production only if the supported corpus is broad
enough to avoid a one-writer parser and maintenance ownership is explicit.

## 8. Risks and boundaries

- Binary-format edge cases can silently corrupt coordinates if validation is weak.
- XTC decompression is substantially more difficult than DCD parsing.
- A compiled extension increases wheel, platform, and release complexity.
- Parallel I/O is not automatically faster on compressed or storage-bound files.
- Memory mapping is not a substitute for decoding variable-size compressed frames.
- This work must not delay higher-priority 1.0 contract and scientific consolidation.

The proposal is successful even if the final decision is to retain third-party
parsers, provided the decision is supported by corpus tests, benchmarks, and a
clear ownership contract for the adapters.
