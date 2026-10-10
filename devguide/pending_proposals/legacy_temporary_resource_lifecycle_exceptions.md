---
summary: Complete legacy bridge and native-probe temporary-resource lifecycles.
issue: uibcdf/molsysmt#374
status: partial
opened: 2026-10-10
closed:
verification: reproduced
area: [form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Legacy temporary-resource lifecycle exceptions

**Reported:** 2026-10-10, owner review in uibcdf/molsysmt#371.
**Status:** Eager runtime bridges and generated output failure custody repaired
before 1.0; temporal native-probe lifetime remains deferred.

## What

Complete failure/lifetime cleanup in legacy optional file bridges, generated
file-returning outputs before successful return, and the standalone temporal
native-library benchmark. Successful returned files are caller results and must
remain available. This adds no molecular capability or scientific method.

## How

Source inspection of `70d1400b9514904fbf9b1a5ca126ddf4591e63dc` identifies:

- `molsysmt/form/openmm_Simulation/to_pdbfixer_PDBFixer.py`: intermediate PDB
  removal occurs only after both conversions complete.
- `molsysmt/build/get_missing_bonds.py`, optional pytraj branch: its intermediate
  PDB is not retired after eager topology conversion.
- File-returning writers/downloads using generated paths: define failure custody
  before the path is returned, preserving successful result ownership and caller
  destinations. Inspect partial-write/download behavior before changing it.
- `devtools/scripts/benchmark_interactions_temporal.py::rust_query`: temporary
  directory and loaded-library lifetime rely on the returned resource tuple and
  finalization, without a surrounding explicit preparation/query failure scope.

Prefer existing managed contexts and owner-local lifecycle operations. Respect
actual eager reader and loaded-library lifetimes; do not invent a generic
cleanup abstraction or delete returned results.

## Why

These independently owned operations need their remaining lifecycle debt visible.
The reproduced current memmap/LEaP defects are repaired under uibcdf/molsysmt#372
and uibcdf/molsysmt#373. This follow-up concerns legacy optional/research routes
outside the selected pre-1.0 qualification scope; source inspection is not a
scientific regression or executed platform-leak claim. Shared policy ownership
remains uibcdf/molsyssuite#104.

## Bounded implementation exception

- **Owners:** dprada/LMMV.
- **Review:** 2026-10-24, or before the next affected invocation.
- **Reason:** provider/reader/native lifetimes and failure output semantics need
  independent guards; the standalone probe is research tooling, not the runtime.
- **Interim:** select an exclusive process scratch root through TMPDIR before
  interpreter startup. Retain it through error inspection; retire it after
  children, readers and loaded libraries end. Use explicit output filenames
  when file-creation failure must be recoverable.
- **Removal condition:** execute success, preparation/conversion/start/query failure,
  caller-custody and visible-retirement-error guards for the actual owning routes.
  Loaded DLL lifetime requires relevant platform evidence before a Windows claim.

## What is measured and what is assumed

The initial review inspected the listed source without executing optional
engines, native compilation or an all-platform failure reproduction. Executed
runtime evidence is recorded in the implementation checkpoints below. No native
probe qualification, historical resource deletion or complete-compliance claim
is made.

## What was refuted

Successful files located under a temporary root are not automatically disposable.
Managed Python finalization is not the same evidence as explicit success/failure
retirement of a still-loaded native library. Linux unlink behavior is insufficient
for Windows lifetime guarantees.

## Scope and acceptance criteria

Close only after the explicit owners establish the listed lifetimes and outcome
semantics without changing scientific criteria or deleting caller results. Preserve
public validation, form/unit behavior and dependency direction. No heavyweight
universal matrix, blanket disk cleanup or release rebuilding is required merely
to register this debt. See [the owner contract](../temporary_resource_operations.md).

## Partial implementation — 2026-10-10

**Contract-tested.** The Simulation/PDBFixer bridge and optional PyTraj
missing-bond branch now own their intermediate PDBs inside explicit
TemporaryDirectory contexts. Reading, writing and extracting pairs occur before
exit. Success and exceptional paths retire only that owned scratch; caller
results are preserved, and retirement errors propagate. No new generic resource
helper, dependency or scientific criterion is introduced.

Addressable guards:

- `tests/form/openmm_Simulation/test_bridge_resource_lifecycle.py` verifies
  write/read failure, original exception identity, successful object return,
  caller-file preservation and visible removal failure. Its real OpenMM/PDBFixer
  case confirms that the eager result is usable after scratch retirement.
- `tests/build/get_missing_bonds/test_pytraj_resource_lifecycle.py` injects
  write/read/pair-extraction/removal failure at provider boundaries. Its eager
  topology stand-in demands a live input during extraction, and independently
  expected pairs survive successful retirement. It does not certify an installed
  PyTraj engine or its scientific criteria.

Before repair, the eight-test lifecycle selection fails seven cases and passes
one success control. After repair plus #379's real-writer box correction,
13 tests pass on Linux/Python 3.14.7:

```bash
python -m pytest --receptor=llm -n12 tests/form/openmm_Simulation/test_bridge_resource_lifecycle.py tests/form/openmm_Simulation/test_pdb_export.py tests/build/get_missing_bonds/test_pytraj_resource_lifecycle.py tests/build/get_missing_bonds/test_get_missing_bonds.py::test_get_missing_bonds_with_selection_preserves_pairs
```

The real-engine test exposed a separate pre-existing current-box shape error,
now tracked and repaired under uibcdf/molsysmt#379. One expected LegacyH5MSMWarning
comes from the existing selected-bond fixture. Foundations, both Toolbox cards,
conversion Cookbook, Common Core module 12 and the maintained resource-owner
table now describe the lifetimes. The three changed docstrings render through
strict Sphinx without RST errors; the missing-bond docstring executes all three
example statements. Napoleon emits deprecation warnings, and the example
correctly warns about its legacy H5MSM input.

At this checkpoint the issue remains open/partial: generated file-returning
writer/download failures and loaded temporal-library lifetime still need
owner-specific evidence. Their
original bounded exception, review date and Windows exclusions remain in force.
No frozen artifact, tag, heavy matrix or publication is changed by this phase.

Focused Ruff checks and `git diff --check` pass. All 14 fast release gates
pass, including adapter delivery, dependencies, devguide integrity, shared
course structure and public smoke. These checks are development evidence,
not heavy or installed-artifact candidate qualification.

## Generated output custody — 2026-10-10

**Contract-tested.** The shared RCSB downloader now writes each attempt inside
owned staging beside its destination. It publishes with `os.replace` only after
the response and writer close. HTTP/streaming failure and cancellation retire
staging without deleting or truncating a pre-existing destination. Retry count,
warning context, default basenames and successful generated-result custody stay
unchanged. The previous `_cleanup_partial` could delete caller data even on an
HTTP 404 before opening the destination, and hid removal failures.

All five PDB-ID file converters and both AlphaFold file converters retain owned
staging through extraction. A rejected selection no longer publishes the download
or replaces caller evidence. PDB-text and UniProt FASTA writers retire only their
automatically generated outputs on write/close failure or interruption. Explicit
writer destinations are retained and may contain partial writes. FASTA descriptor
wrapping failure also closes the allocated descriptor before retiring its path.
No network endpoint, retry profile, scientific method, dependency or public
signature is added. Shared download staging belongs to the existing private
download owner; compound operations retain owner-local managed contexts.

Before the download repair, the 19-case lifecycle selection fails 16 cases and
passes three controls. Before the compound-converter repair (with the downloader
already corrected), its 26 cases fail 19 and pass seven. These are offline
controlled executions, not remote-provider availability or chemical-parity claims.

Addressable guards:

- `tests/form/test_download_resource_lifecycle.py`: all five RCSB adapters,
  terminal/transient HTTP errors, interrupted streams, cancellation, retry success,
  generated success custody and visible retirement failure.
- `tests/form/test_remote_file_publication.py`: real selection rejection in all
  five PDB-ID file adapters; absent/existing/default destinations; unchanged
  successful names; both AlphaFold adapters with controlled download failure,
  real extraction rejection and success.
- `tests/form/test_generated_writer_lifecycle.py`: generated versus explicit
  output custody on write/close failure, descriptor preparation failure, original
  exception identity, visible retirement errors, validated direct-adapter success
  and high-level conversion with explicit filenames. PDB text uses a bundled real
  system; UniProt responses are controlled offline fixtures.

The destination parent must be writable for staging. Atomic replacement changes
the destination inode rather than writing through it. This does not guarantee
power-loss durability, concurrent-writer serialization or rollback on a cleanup
error after publication. User Guide Foundations, PDB/FASTA Toolbox cards,
conversion Cookbook, Common Core module 12 and the maintained owner table describe
these exact limits. High-level `convert` still requires an explicit filename for
file targets; generated-path support belongs to the corresponding form adapters.

The only remaining #374 exception is the loaded temporal native-library probe.
Its original owner/review date and requirement for actual platform lifetime
evidence remain in force. No frozen candidate, artifact, tag or release changes.

The complete repaired runtime lifecycle selection passes **86 tests**, with no
skips, on Linux/Python 3.14.7 and twelve workers:

```bash
python -m pytest --receptor=llm -n12 tests/form/test_download_resource_lifecycle.py tests/form/test_download_diagnostics.py tests/form/test_remote_file_publication.py tests/form/test_generated_writer_lifecycle.py tests/form/openmm_Simulation/test_bridge_resource_lifecycle.py tests/build/get_missing_bonds/test_pytraj_resource_lifecycle.py
```

The new PDB-text docstring executes seven example statements; all fourteen
changed docstrings render through strict Sphinx without warnings. Documentation
edits preserve all notebook code, saved outputs and execution metadata; their
execution is not repeated or newly qualified. Focused Ruff, the exact-base public
signature comparison and all fourteen fast development gates pass. These are
bounded source checks, not heavy or installed-artifact qualification.
