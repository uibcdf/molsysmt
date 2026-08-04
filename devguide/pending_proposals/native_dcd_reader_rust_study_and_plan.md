# Study and implementation plan: a MolSysMT-owned DCD reader and writer in Rust

**Status:** engineering study; **no approval to start**.
**Written:** 2026-08-03, at the maintainer's request. Extended the same day after
reading MDAnalysis's independent implementation, which changed several conclusions.
**Relationship to existing proposals:** this is the concrete study that
[`rusterization_parallel_trajectory_io.md`](rusterization_parallel_trajectory_io.md)
deferred to "Phase 2: DCD production decision", and it inherits the adoption gates of
[`native_format_parsers_post_1_0.md`](native_format_parsers_post_1_0.md). Neither is
superseded. Whether the work happens at all is still governed by their go/no-go
criteria; this document exists so that decision can be taken with a real design in
front of it rather than an intuition.

---

## 1. What the reader has to deliver

Not "parse DCD": deliver the MolSysMT structural contract for the `file:dcd` form.
Everything below is what the current MDTraj-backed adapter already provides and what
a replacement must match exactly.

| surface | contract |
|---|---|
| `coordinates` | `(n_structures, n_atoms, 3)`, nm, through PyUnitWizard |
| `box` | `(n_structures, 3, 3)`, nm; `None` when the file carries no cell |
| `structure_id` | source frame index |
| `time` | ps, derived from `ISTART`, `NSAVC` and `DELTA` when meaningful |
| `n_atoms`, `n_structures` | without decoding coordinates |
| atom subset | `atom_indices` applied during decode, not after |
| structure subset | arbitrary index lists, not only ranges |
| iteration | `StructuresIterator` with `chunk`, `start`, `stop`, `step` |
| cursor | metadata access must not consume the read position |
| lifetime | explicit `close`; no descriptor leak on error |

The table is a list of values, and reading it as one is the mistake section 7.0
documents. What matters as much is **which of them can be answered without decoding
the trajectory**: `n_atoms`, `n_structures`, the presence of a cell and the frame
stride are header questions, and `time`, `structure_id` and `box` need no coordinate
record at all. A backend that cannot answer them cheaply forces the adapter into the
shape it has today.

Two behaviours are contract, not implementation detail, because MolSysMT already
depends on them:

- **DCD carries no topology.** `forms_and_conversions.md` fixes the read scope: a
  standalone DCD may produce an index-only native topology and must leave semantic
  atom IDs and chemical attributes missing rather than invent them.
- **Coordinates cross the MDTraj boundary in angstroms** today and are normalized
  once. A native reader removes that boundary: it must convert at exactly one place
  and document that DCD stores angstroms.

---

## 2. Three libraries, two lineages, and they disagree

| library | DCD implementation | lineage |
|---|---|---|
| MDTraj 1.11 | `mdtraj/formats/dcd` | VMD molfile plugin |
| Biotite 1.4 / biotraj 1.2 | `biotraj/src/dcdplugin.c` | VMD molfile plugin, forked |
| MDAnalysis | `lib/formats/libdcd.pyx` + `include/readdcd.h` | independent rewrite |

Biotite reads DCD through biotraj, which is MDTraj's format readers spun off; for this
format it is the **same lineage**, not a third opinion. MDAnalysis rewrote its reader
and is the only genuinely independent implementation of the three.

They do not agree, and the disagreements are exactly on the hard cases. This is the
most useful thing in this study and it was found by reading, not by benchmarking:

| capability | VMD lineage (MDTraj, Biotite) | MDAnalysis |
|---|---|---|
| cell as angle cosines | yes | yes |
| cell as degrees | yes | yes |
| **cell as a box matrix** (newer CHARMM) | **no** | **yes** |
| **fixed atoms** (`NAMNF != 0`) | **yes** | **no**, declined in the docstring |
| 4D coordinates | skipped | declined |
| time unit of `DELTA` | treated as ps | declared **AKMA**, overridable |

**Each implements what the other does not.** A triclinic DCD from a recent CHARMM is
read differently by MDTraj and MDAnalysis; a trajectory with fixed atoms is readable
by MDTraj and not by MDAnalysis; and the two produce different time axes for the same
file. No third implementation exists to break the tie.

There is no maintained specification document. The two lineages *are* the
specification, and they contradict each other.

## 3. The format, as the reference implementations actually read it

Taken from `biotraj/src/dcdplugin.c` and from MDAnalysis's `libdcd.pyx` and
`readdcd.h`, all of which ship their source.

### 3.1 Record framing and endianness

DCD is a sequence of Fortran unformatted records: each is *length, payload, length*
with 32-bit markers, except that CHARMM built with `-i8` writes 64-bit markers. The
detection reads two 32-bit integers and branches:

| first two integers | meaning |
|---|---|
| sum == 84 | 64-bit record markers, native endianness |
| `[0] == 84` and `[1] == 'CORD'` | standard 32-bit markers, native endianness |
| the same after byte-swapping | as above, opposite endianness |
| anything else | not a DCD |

With 64-bit markers a further read must find the `CORD` magic. **Four combinations of
marker width and byte order have to be supported**, and a reader that assumes
little-endian 32-bit will silently misread files from other machines.

### 3.2 Header

After the marker comes an 80-byte header buffer read as a block and then indexed:

| offset | field |
|---|---|
| 0 | `NSET`, number of frames as written |
| 4 | `ISTART`, first timestep |
| 8 | `NSAVC`, steps between saves |
| 32 | `NAMNF`, number of fixed atoms |
| 36 | `DELTA`, timestep — **`float` for CHARMM, `double` for X-PLOR** |
| 40 | non-zero: an extra block per frame, the unit cell |
| 44 | `== 1`: a fourth dimension per frame |
| 76 | non-zero: CHARMM file, and its version; zero: X-PLOR |

Then a title record (`NTITLE` lines of 80 chars) and a record with the atom count.

`NSET` is not trustworthy on a file still being written or truncated. The frame count
has to be cross-checked against the file size and the computed frame stride.

### 3.3 Frames

Per frame, in order:

1. the unit cell record, six doubles, only when the extra-block flag is set;
2. three records of `n_atoms` `float32`: all X, then all Y, then all Z;
3. a fourth-dimension record when that flag is set, to be skipped.

Coordinates are **structure-of-arrays on disk** and **array-of-structures in the
MolSysMT contract**. The transpose is the reader's job and is the one place where a
native implementation can be meaningfully faster than a generic one, because the
X/Y/Z streams can be interleaved directly into the output buffer.

Fixed atoms (`NAMNF != 0`) change everything: the first frame carries all atoms, and
subsequent frames carry only the free ones, with a free-index record mapping them.
Neither bundled test file exercises this.

### 3.4 The frame count is never trusted

Neither implementation believes `NSET`. MDAnalysis computes it from the file size with
an explicit stride, and the VMD lineage cross-checks similarly:

```
first frame:  (n_atoms + 2)             * n_dims * 4 + extra_block
later frames: (n_atoms - n_fixed + 2)  * n_dims * 4 + extra_block
n_frames    = (file_size - header - first) / later + 1
```

The `+ 2` is the pair of Fortran record markers around each coordinate array. This is
also what makes a file written by a running simulation readable: the count follows the
bytes on disk, not the header. A native reader must do the same, and should **report**
when `NSET` and the file size disagree, which neither library does.

### 3.5 The unit cell, and the single largest scientific risk

The six doubles are stored as `A, ?, B, ?, ?, C`, and the three remaining slots are
**one of three things**, depending on which program wrote the file, with no flag to say
which. The VMD lineage knows two of them and guesses between them:

```c
if (unitcell[1] >= -1.0 && unitcell[1] <= 1.0 &&
    unitcell[3] >= -1.0 && unitcell[3] <= 1.0 &&
    unitcell[4] >= -1.0 && unitcell[4] <= 1.0) {
    /* CHARMM, or NAMD > 2.5: cosines */
    ts->alpha = 90.0 - asin(unitcell[4]) * 90.0 / M_PI_2;
    ...
} else {
    /* likely NAMD 2.5: degrees */
    ts->alpha = unitcell[4];
    ...
}
```

MDAnalysis adds the third case, which the VMD lineage does not implement at all:

```python
elif np.any(uc < 0.) or np.any(uc[3:] > 180.):
    # might be new CHARMM: box matrix vectors
    e1, e2, e3 = H[[0, 1, 3]], H[[1, 2, 4]], H[[3, 4, 5]]
    uc = triclinic_box(e1, e2, e3)
```

So the six doubles may be **angle cosines**, **angles in degrees**, or **the packed
symmetric box matrix**. MDTraj and Biotite read a recent triclinic CHARMM file
differently from MDAnalysis, and neither raises.

The heuristic is ambiguous exactly where it matters: a cell with an angle of
**1 degree or less**, or a cosine near ±1, satisfies more than one branch. Such cells
are pathological but not impossible, and the wrong branch produces a plausible-looking
box rather than an error. MDAnalysis says so in its own class documentation:
*"Check the unitcell dimensions, especially for triclinic unitcells."*

A native reader **must not silently reproduce a guess**. This is the strongest
argument in the whole study for owning the parser, and it has nothing to do with
speed. What to do instead is in section 7.

### 3.6 The time unit is not a property of the format

`DELTA` is a number without a unit. CHARMM and NAMD write it in **AKMA** time;
other writers write picoseconds. MDAnalysis declares `units = {'time': 'AKMA'}` and
lets the caller override `dt`; the VMD lineage treats it as picoseconds. The same file
therefore yields two different time axes depending on which library reads it, silently.

MolSysMT normalizes time to ps through PyUnitWizard. Doing that on an unlabelled
number is the same class of mistake as the unit cell, and section 7 treats it the
same way.

---

## 4. Rust design

### 4.1 Where it goes

The repository already ships a private extension: `rust/` builds `molsysmt._rust`
through `setuptools-rust`, pinned to Rust 1.97.1, PyO3 0.29 with `abi3-py311`, and
`numpy` 0.29. A DCD reader is a new module in that crate, not a new artifact:

```
rust/src/dcd/
    mod.rs        public Rust API, no PyO3
    header.rs     record framing, endianness, header fields
    frames.rs     frame stride, seeking, decoding, transpose
    cell.rs       unit-cell interpretation, including the ambiguity
    errors.rs     typed errors mapped to MolSysMT exceptions at the boundary
```

Keeping PyO3 out of everything but `lib.rs` matters here more than for the numeric
kernels: it is what lets `cargo test --no-default-features` run the parser tests
without a Python interpreter, and the parser is the part that most needs fuzzing.

### 4.2 Dependencies

**None beyond `std`** for parsing. Explicitly rejected:

- a memory-mapping crate: DCD frames are read sequentially or by seek, and mapping a
  file MolSysMT does not own complicates the "no descriptor leak" contract for no
  measured gain. Revisit only if profiling shows syscall overhead dominating.
- a binary-parsing crate: the format is four integer reads and three float records.
  A dependency would be larger than the code it replaces.
- Rayon inside the reader: I/O is the bottleneck, and the existing kernels already
  own thread-pool policy. Parallel *decoding* of an already-buffered chunk is a later
  measurement, not a design assumption.

### 4.3 The Python boundary

Two functions and one object, all private:

```
_rust.dcd_open(path)             -> handle with header metadata
_rust.dcd_read(handle, structure_indices, atom_indices) -> (coordinates, cell, ok)
_rust.dcd_close(handle)
```

Returning `numpy` arrays allocated in Rust and handed over with `IntoPyArray`, as the
existing kernels do. Coordinates come back in **angstroms and float32 as stored**;
unit conversion and the PyUnitWizard wrapping stay in the Python adapter, where they
already are and where they are already tested. The reader converts nothing, and it
**interprets nothing**: the six cell doubles cross the boundary raw.

That split is not an invention of this study. It is what MDAnalysis does — its C layer
copies the six doubles out untouched and the interpretation lives in Python, next to
the issue number that motivated it — and it is the opposite of the VMD lineage, which
bakes the guess into C where no caller can see or override it. Between the two
existing designs, the independent rewrite chose the separation, having been burnt.

**Diagnostics are the caller's.** Recorded as a requirement in
`native_format_parsers_post_1_0.md` after MDTraj's DCD reader was found printing to
the C standard output on every open and every read: the native reader takes a
verbosity argument, routes every message through the MolSysMT catalog, and never
writes to standard output. That the current backend cannot be quietened without
redirecting a file descriptor is precisely the failure not to repeat.

### 4.4 Errors

One typed Rust error per failure mode — bad magic, unsupported marker width,
truncated record, atom-count mismatch, ambiguous cell — mapped at the boundary to the
existing MolSysMT exceptions rather than to `ValueError`. A truncated file must be
distinguishable from a corrupt one, because the first is normal for a running
simulation and the second is not.

---

## 5. What the corpus has to cover, and what exists

The repository ships **two** DCD files: `popc_membrane.dcd` (4.7 MB, 5 structures,
78,974 atoms) and `traj_chicken_villin_HP35_solvated.dcd` (1.0 MB, 20 structures,
4,369 atoms). Both are standard 32-bit, native endianness, CHARMM, with a unit cell.
That is **one point in a space of at least sixteen**, and it is the single largest
gap between this study and an implementation that could be trusted.

Fixtures can be **generated**, and that matters more than it looks: DCD is as easy to
write as to read, and MDAnalysis ships a writer. The corpus is therefore work, not a
blocker — it does not depend on finding files in the wild.

Required before any production decision:

| dimension | cases |
|---|---|
| record markers | 32-bit, 64-bit `-i8` |
| byte order | native, opposite |
| flavour | CHARMM, X-PLOR (changes `DELTA`'s type) |
| cell | absent, orthorhombic, triclinic, cosines, degrees |
| fixed atoms | none, some |
| fourth dimension | absent, present |
| damage | truncated mid-record, truncated mid-frame, atom-count mismatch, empty |

Provenance of every fixture must be recorded, because a corpus written by one writer
produces a parser that only reads that writer's files. Where redistribution is not
permitted, the case must be listed as unverified rather than quietly dropped.

### The real blocker: no independent oracle for the hard cases

Section 2 says each lineage implements what the other does not, and that lands here.
**Fixed atoms can only be checked against MDTraj. The box-matrix cell can only be
checked against MDAnalysis.** For the two cases where a reader is most likely to be
wrong, there is exactly one implementation to compare with, and
`rusterization_parallel_trajectory_io.md` already rules that out as evidence:
"agreement between a new Rust implementation and a MolSysMT Python prototype is
implementation parity, not independent scientific truth". The same applies to
agreement with a single library.

For those cases the validation has to be **against the format itself**: fixtures whose
byte layout is constructed deliberately, with the expected values known because we
wrote them. That is defensible and it is what a specification-level test looks like,
but it must be stated rather than passed off as differential testing.

---

## 6. Plan

Each phase ends in a decision the maintainer can take on evidence. **Any phase may
end the effort**; that is a success, not a waste, provided its finding is recorded.

### Phase 0 — Corpus and baseline

Build the fixture set of section 5 with recorded provenance and hashes. Measure the
current MDTraj path: cold and warm open, sequential throughput, arbitrary-frame
access, atom-subset access, peak RSS, descriptors. Extract a golden reference for
every fixture, read by **both** MDTraj and MDAnalysis, and record the cases where the
two disagree.

Two disagreements are already known from section 2 and should be confirmed first,
because they are the ones that would change how MolSysMT reads real files today:
a recent triclinic CHARMM file, where only MDAnalysis applies the box-matrix branch;
and any file at all, where the two libraries produce time axes differing by the
AKMA-to-picosecond factor. Confirming those two is worth the phase on its own,
**whatever is decided about Rust**: if MDTraj is reading either of them wrongly for us,
that is a live defect in the current adapter, not a future one.

Measure the getter table of section 7.0 as well, and then repeat it against a version
of the adapter whose getters do **not** route through `to_molsysmt_Structures`. The
difference is how much of the current cost is the external parser and how much is the
adapter's own shape. If most of it is the adapter, the native backend loses its
cheapest argument and the right work is a rewrite of the getters against MDTraj.

*Exit:* a corpus, a baseline table, a list of upstream disagreements, a decision on
whether the current adapter has a defect, and the split between adapter cost and
parser cost.

### Phase 1 — Reader in Rust, read-only, no integration

`rust/src/dcd/` per section 4, exercised only by `cargo test` against the corpus
fixtures with the golden values embedded. No PyO3, no adapter changes.

A minimal writer is built in this phase as a **test instrument**, not a feature: it is
what makes the byte-identical round trip of W1 testable, and the round trip is the only
check that proves the reader understood a file rather than produced plausible numbers.

*Exit:* every fixture decoded, or the unsupported variants named explicitly; and
`write(read(f)) == f` byte for byte on every fixture.
Differential agreement with the oracles to the tolerance of the stored precision —
DCD holds `float32`, so equality is exact for coordinates and the tolerance question
only arises for the derived cell.

### Phase 2 — Fuzzing and damage

`cargo-fuzz` on the header and frame readers. Every malformed input must produce a
typed error, never a panic, never a wrong-but-plausible frame count, never an
unbounded allocation from a corrupt record length.

*Exit:* a fuzz corpus in the repository and a clean run of an agreed duration. **This
is a hard gate.** A parser that panics on hostile input is worse than a dependency.

### Phase 3 — Python boundary, behind a switch

PyO3 wrapper and an adapter that can use either backend, selected by
`configure.dcd_backend`, defaulting to MDTraj. The whole existing `file:dcd` test
suite must pass under both.

*Exit:* identical public behaviour on both backends across the suite, and the
benchmark table repeated against the Phase 0 baseline.

### Phase 4 — Decision

Adopt as default only if Phases 1-3 pass **and** the go/no-go criteria of
`rusterization_parallel_trajectory_io.md` section 7 are met: 1.5x representative
throughput, or 25% lower peak memory, or a materially lighter dependency, without a
serious regression elsewhere. Ambiguity handling and diagnostics ownership count as
"demonstrably safer resource and corruption handling" and may carry the decision on
their own, provided that is stated rather than smuggled in.

If adopted, MDTraj remains available as an explicit compatibility backend for at
least one release cycle, per that proposal.

### Not in scope

XTC, which is a different problem: compressed frames, a bit-packing decoder, and a much
larger fuzzing surface. Parallel decoding.

Writing DCD was excluded by the earlier proposal and is **reconsidered** here: section
7.2 argues that the round-trip test is the strongest evidence the reader is correct, so
a minimal writer earns its place inside Phase 1 as a test instrument. Promoting it to a
public writing capability remains a separate decision with its own review.

---

## 7. Where a MolSysMT reader and writer would actually be better

"Better" has to mean something checkable. Not "in Rust", not "ours": a behaviour that
can be demonstrated on a fixture and that no existing implementation provides. Speed is
deliberately last, because it is the weakest of these claims.

### 7.0 The point: not another DCD parser, but the one this form needs

Every claim below is secondary to this one. MolSysMT does not need a general-purpose
DCD library — three of those already exist and two of them are maintained by larger
teams than this one. What it needs is a backend shaped like the questions the
`file:dcd` adapter is actually asked, and today that shape is wrong in a way that has
nothing to do with the parser being written in C.

**Every getter of `file:dcd` decodes the whole trajectory.** Without exception:

```python
def get_n_structures_from_system(item, structure_indices='all', ...):
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)   # decodes everything
    return aux_get(tmp_item, structure_indices=structure_indices)  # then slices
```

`get_n_atoms_from_system`, `get_box_from_system`, `get_box_lengths_from_system`,
`get_time_from_system`, `get_structure_id_from_system`, `get_coordinates_from_atom`
and the rest are the same four lines with a different `aux_get`. The `structure_indices`
and `indices` arguments never reach the reader; they are applied to the fully decoded
result.

Measured on the two bundled files, best of three:

| request | popc, 78,974 atoms x 5 | villin, 4,369 atoms x 20 |
|---|---:|---:|
| `n_atoms` | 40.7 ms | 88.2 ms |
| `n_structures` | 39.6 ms | 87.6 ms |
| `box` | 40.5 ms | 89.4 ms |
| `coordinates`, all structures | 43.5 ms | 90.2 ms |
| **`coordinates`, one structure** | **85.1 ms** | **173.4 ms** |

Three things in that table, and each is an argument on its own.

**Counting frames costs as much as reading them.** `n_structures` is a header field
and a division by the frame stride — bytes that section 3.4 already describes. It is
being paid for with a full decode. So is `n_atoms`, which is one integer at a known
offset. So is `box`, which needs six doubles per frame and decodes every coordinate to
get them.

**Asking for less costs twice as much.** One structure out of five costs 85 ms against
43 ms for all five, because the full decode happens either way and the slicing is
added on top. A user who samples a trajectory is penalised for sampling it. This is
the clearest possible statement that the adapter and the backend are not shaped alike.

**The cost follows the frame count, not the data volume.** Villin is one fifth the
size of popc and takes twice as long: 4.4 ms per frame against 8.1 ms, for eighteen
times fewer atoms. Roughly 4 ms of every frame is fixed overhead — a seek, a read
call, and a trip through the intermediate object — independent of how many atoms it
holds. Extrapolating that fixed part alone, a 5,000-frame trajectory spends about
**20 seconds before a single coordinate is used**, and pays it again for every
attribute requested.

None of this requires Rust to fix; part of it is adapter work that could be done
against MDTraj today. But it does say what the native backend has to be built around,
and it is the difference between a parser that is merely ours and one that earns its
place:

- **header-only queries.** `n_atoms`, `n_structures`, the flavour, the presence of a
  cell and the frame stride come from the first 100 bytes and the file size. Constant
  time, no frame decoded.
- **`structure_indices` pushed into the reader.** Arbitrary index lists, resolved by
  seeking to the computed offsets. Reading one frame of five thousand touches one
  frame.
- **`atom_indices` pushed into the decode.** The record must be read whole, but only
  the requested atoms are written into the output buffer, which is what R7
  measures.
- **attribute-selective decoding.** `box` reads the cell record and skips the three
  coordinate records by seeking past them. `time` and `structure_id` need no frame at
  all.
- **one traversal per request, no intermediate object.** The current path builds a
  full `molsysmt.Structures` in order to answer a question about a header.

That list is not performance tuning. It is the adapter's public surface expressed as
the backend's API, so that what MolSysMT asks and what the reader does are the same
operation. Any of these on their own is worth more to MolSysMT than being faster at
decoding a full trajectory, which is the only thing a general-purpose parser optimises.

**A caveat that keeps this honest.** The adapter is written the way it is because
delegating to `to_molsysmt_Structures` was the cheapest way to satisfy the form
contract with an external reader. Rewriting the getters to be lazy is possible
*without* a native backend, and Phase 0 should measure how much of the table above
survives that rewrite. If most of it does, the native reader has to justify itself on
sections 7.1 to 7.2 alone, and this section becomes an argument for fixing the adapter
rather than for writing a parser. That would be a good outcome, and finding it out is
cheap.

### 7.1 Reader

**R1. The cell convention is decided and declared, never silently guessed.**
The boundary returns the six raw doubles plus the convention the reader inferred —
`cosines`, `degrees`, `box_matrix` or `ambiguous` — and the caller may override it. A
file whose values satisfy more than one branch is reported as `ambiguous` instead of
being resolved by argument order. The chosen convention travels as provenance, so a
system built from a DCD can say how its box was obtained.

Nobody does this. The VMD lineage decides in C where it cannot be seen; MDAnalysis
decides in Python where it can be read but not changed, and tells the user to check the
result by hand. *Checkable:* a fixture with an angle of 0.5 degrees must be reported
ambiguous by us and is silently mis-resolved by both.

**R2. The union of what the two lineages support, which is what neither has.**
Fixed atoms *and* the box-matrix cell. A trajectory with fixed atoms written by recent
CHARMM is currently readable in full by no library at all. *Checkable:* one fixture
with `NAMNF != 0` and a box-matrix cell.

**R3. Time is not manufactured from an unlabelled number.**
`DELTA` is AKMA for CHARMM and NAMD, picoseconds elsewhere, and nothing in the file
says which. MolSysMT's own contract is ps through PyUnitWizard. The reader therefore
reports `time` only when the flavour determines the unit, takes an explicit unit when
it does not, and otherwise returns `None` with a diagnostic — rather than producing a
time axis that is wrong by a factor of about 48.9. *Checkable:* the same fixture read
by MDTraj and by MDAnalysis already yields two different time axes; we yield one
answer or none, and say why.

**R4. Truncated is not corrupt.**
A file whose last frame is incomplete because the simulation is still running is
normal and must read up to the last whole frame. A bad record marker in the middle is
damage. These are different typed errors, and neither library distinguishes them:
both simply compute a frame count from the file size and continue. *Checkable:* two
fixtures, one truncated mid-frame and one with a corrupted interior marker; the first
reads N-1 frames with a note, the second raises.

**R5. `NSET` disagreeing with the file size is reported.**
Both libraries silently prefer the file size. That is the right value, but the
disagreement is information — a partially written or concatenated file — and throwing
it away is a choice nobody documented. *Checkable:* a fixture with `NSET` deliberately
wrong.

**R6. Diagnostics belong to the caller.**
A verbosity argument, every message through the MolSysMT catalog, nothing written to
standard output ever. This is a direct response to MDTraj printing two lines on every
open and every read, which cannot be turned off and had to be suppressed by
redirecting a file descriptor. *Checkable:* trivially.

**R7. The atom subset is applied while decoding.**
MDAnalysis materializes the full `(n_atoms, 3)` frame and slices it afterwards
(`xyz_tmp[c_indices]`). The disk read is the same either way — a coordinate record is
contiguous and must be read whole — so the saving is in allocation and copying, not
I/O. On the bundled membrane, selecting 294 phosphorus atoms out of 78,974 currently
allocates 268x more than it keeps, per frame. *Checkable, and to be measured rather
than assumed:* this is the only performance claim here, and it is bounded.

### 7.2 Writer

The existing proposal put writing out of scope. It is worth reconsidering, because the
strongest single claim available is a writer claim.

**W1. Round-trip fidelity as a contract.**
Read a DCD and write it back unmodified, and get a **byte-identical file**: same
marker width, same byte order, same flavour, same title records, same cell convention,
same `NSET`. No existing library promises this, and none can, because they all discard
the information needed for it during reading — the VMD lineage resolves the cell in C,
and MDAnalysis normalizes to its own dimensions representation. Keeping the raw six
doubles and the inferred convention (R1) is exactly what makes it possible.

This is the cleanest acceptance test in the whole document: for every fixture,
`write(read(f)) == f` byte for byte. It is also the strongest scientific argument,
because a format round trip that loses nothing is the only proof that the reader
understood the file rather than merely produced plausible numbers.

**W2. The writer declares its cell convention instead of picking one.**
An explicit argument, defaulting to whatever the source file used when the system came
from a DCD, and to a documented choice otherwise.

**W3. The writer refuses what it cannot represent.**
A system with a triclinic cell that the chosen convention cannot express, or with
per-structure atom counts, is rejected with a typed error naming the loss — not
degraded silently. This follows the existing MolSysMT rule that conversion losses are
reported.

**W4. The mutating surface of the form is currently unimplemented.**
`append_structures`, `add` and `merge` on `file:dcd` all raise
`NotImplementedMethodError`. DCD is an append-only record stream, so appending
structures is the one mutation the format supports naturally and cheaply: seek to the
end, write the records, update `NSET`. A native writer would close that gap for the
form rather than adding a capability nobody asked for, and it is the only way MolSysMT
can write a trajectory incrementally without holding it in memory.

**W5. A file left behind by a crash is still readable.**
Because the frame count is computed from the file size (3.4), a writer that appends
frame by frame and updates `NSET` on close produces a file that remains valid if the
process dies. That should be tested deliberately, not inherited by luck.

### 7.3 What we would *not* be better at, and should not pretend

**Field exposure.** MDTraj and MDAnalysis have been fed millions of real files, from
writers that no longer exist, for over a decade. A generated corpus cannot buy that,
and the first genuinely strange file from a user will find something. This argues for
keeping an established reader available as a fallback and for treating the native
backend as the default only after real trajectories have gone through it.

**Breadth.** They read dozens of formats. This is one.

**Maintenance surface.** Every variant supported is a variant to keep working, on
every platform in the wheel matrix, forever.

---

## 8. Honest assessment

**What owning the parser actually buys.** Section 7 lists it as seven reader claims
and four writer claims, each with a fixture that would demonstrate it. The three that
carry the decision are R1 (the cell is declared, not guessed), R3 (time is not
manufactured from an unlabelled number) and W1 (byte-identical round trip). All three
are correctness, not speed. The only performance claim, R7, is bounded and unmeasured.

**What it costs.** A binary format with no specification, four framing combinations,
two writer conventions for the cell, fixed-atom frames that no bundled file
exercises, a permanent compatibility corpus, a fuzzing obligation, and the parser
becoming a platform-specific artifact in every wheel.

**What must not be the reason.** The noise on standard output. It cost one context
manager to remove. It is evidence about diagnostics ownership and it is recorded as
such; it is not a justification for owning a binary parser, and this document should
not be read as one.

**The framing that should survive this document.** MolSysMT does not want one more
DCD parser. It wants a backend whose API is the `file:dcd` adapter's surface, so that
counting frames costs a header read, asking for one structure costs one structure, and
asking for the box does not decode coordinates. Section 7.0 shows that today none of
that is true, and that a general-purpose parser — however good — cannot make it true,
because it optimises the operation MolSysMT performs least: decoding an entire
trajectory in one go.

**The order.** Phase 0 has value regardless of what follows: the corpus and the
oracle disagreements improve the *current* adapter's tests whether or not a line of
Rust is ever written. If the effort is to start anywhere, it starts there, and the
decision to continue can be taken afterwards with more evidence than exists today.
