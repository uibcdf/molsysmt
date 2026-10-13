---
summary: Read gzip PDB inputs through the shared native parser.
issue: uibcdf/molsysmt#385
status: resolved
opened: 2026-10-13
closed: 2026-10-13
verification: measured
area: [form, convert]
guard: tests/form/file_pdb_gz/test_input.py
normative:
blocked_by: []
supersedes: []
---

# Reading gzip PDB inputs through the native parser

**Reported:** DockingMT's frozen 3PTB workflow, uibcdf/dockingmt#5 and #49.
**Status:** Resolved in source; contract-tested and parity-tested on Python 3.14.

## What

Recognize file:pdb.gz for strings and path-like inputs and decode it into the
existing native PDB handler. Compressed bytes, adjacent files and plain-PDB
chemistry/geometry semantics must be preserved.

## How

A distinct input adapter declares pdb.gz in the existing form catalogue and uses
gzip.open inside a context manager. Decoded text feeds the shared PDBFileHandler;
no duplicate atom/group parser, decompressed neighbor or temporary disk file exists.
Each read owns an independent decoded buffer. Handler conversion closes it on
success and failure; explicit returned handlers transfer ownership to their caller.
Malformed/truncated/CRC-invalid gzip or failed UTF-8 decoding raises FileContentError
with filename and original cause. Filesystem and parser failures propagate.

Native MolSys, Topology and Structures routes retain selected atom/structure indices,
units and explicit bond-inference policy. Plain decoded PDB text is a separate
public conversion. Attribute delivery pipes through the native handler; no
placeholder getters or untested external-engine routes are advertised.

## Why

DockingMT needs the provider's public route for independently retained structural
archives. The exact frozen 3PTB input is verified by its uncompressed SHA-256 before
use. Original counts and six deposited disulfide edges supply independent truth.

## What is measured and what is assumed

Initial bundled 181L conversion gives file:pdb.gz, 1441 atoms, 13 declared bonds and
one structure with get_missing_bonds=False. Public get returns native atom/structure
counts. A 38,653-byte frozen 3PTB archive is retrieved from DockingMT's exact public
commit; its decompressed digest matches the consumer's declared source.

Parsing is eager, as for the native plain PDB reader; memory stays proportional to
its decoded text and parsed records. No streaming or reduced-RSS claim is made.

## What was refuted

Treating gzip paths as ordinary file:pdb would advertise existing external file
converters that may not understand compressed paths. Staging a neighboring PDB
would break read-only inputs and concurrent readers. Reimplementing parsing or
inference inside the gzip adapter would duplicate native semantics.

## Scope and exclusions

Experimental Tier-3 input-only adapter: native forms, handler and decoded text.
No compressed writer, in-place editing, identity round trip, trajectory iterator,
new chemical inference or automatic native domain is included. Source tests do
not qualify a frozen published package. Plain PDB operations remain unchanged.

## Acceptance criteria

String/Path detection, real 3PTB truth, plain/compressed selected parity, active
length units, nonconsecutive/repeated structure indices, public get, explicit/default
connectivity policy, parallel read-only reads, gzip integrity and failure cleanup.
Form declarations, attribute delivery, docs, cookbook and course stay consistent.

## Provenance

2026-10-13, Linux / Python 3.14.7 development source. Frozen fixture from
uibcdf/dockingmt at a812916193064c04a6e52e119d4787ca22dd19af,
path devguide/validation/data/3ptb_prospective/3PTB.pdb.gz.
Compressed SHA-256: 75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be.
Decoded SHA-256: 288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2.

## Resolution — 2026-10-13

The input adapter delivers five actual native/text conversions through the shared
PDB parser, classified explicitly as experimental Tier 3. Structural form audit
passes 96/96 adapters; no delivered-attribute debt or identity-coverage baseline
is expanded to disguise a missing output operation. Public get uses the handler
pipe; conversion supports explicit atom and structure subsets.

95 tests pass with twelve workers and pytest-receptor on Python 3.14.7:

```bash
python -m pytest -n 12 --receptor=llm tests/form/file_pdb_gz \
  tests/form/file_pdb tests/form/test_catalogue_extension_detection.py \
  tests/test_form_plugin_conventions.py
```

The primary guard checks exact 3PTB scientific/axis truth, deposited connectivity,
all native targets, string/Path recognition, units and selected source metadata,
nonconsecutive/repeated structures, explicit/default inference forwarding,
argument-conflict refusal, raw decoded text, malformed header/truncation/CRC/encoding,
handler ownership/cleanup and concurrent reads under a read-only input directory.
Two ordinary cross-chain connectivity warnings remain from existing tests.

The five-example principal converter doctest passes. The new tutorial executes
with the existing Python-3.14 kernel. Foundations, file Toolbox navigation, the
chemical-preparation Cookbook and course Module 01 document the route. The HTML
Sphinx build succeeds without ERROR lines; existing unrelated warning debt remains
under #144. The source confirms that plain PDB parsing is eager, correcting its
previous streaming label in the affected Foundations table. Ruff, dependencies,
course/API registries and developer-guide validation pass.

No new package, released dependency floor, separate parser or temporary source
file is introduced. Caller-visible scientific criteria remain owned by the
existing PDB connectivity/preparation tools.

## Build-evidence correction — 2026-10-13

The initial resolution sentence claiming an HTML build without ERROR lines is
incorrect. The command exits 0, but logs twelve repeated notebook-JSON schema
errors from six pre-existing notebooks with nbformat minor 4 and cell IDs. They
are Common Core modules 08/10/19, Biophysics module 39 and the basic get/set
tutorials, all unchanged in this adapter work. The new gzip tutorial and modified
Module 01 are schema-consistent. The new page is generated and its code executes,
but the overall documentation build is not clean. This remaining documentation
validation debt belongs with uibcdf/molsysmt#144 and is not repaired by #385.

## Form-roster follow-up — 2026-10-13

A broader registry-adoption selection found four stale exact-roster assertions
that omitted file:pdb.gz. The detection battery now uses the frozen 3PTB fixture,
and all three supported-form rosters include the actual delivered adapter. Exact
set comparisons remain intact; no missing form is hidden by relaxing a check.
These roster changes belong to #385, independently of the pending #382 runtime
adoption and its provider requirement.

After restoring the published runtime, all ten selected roster, inspection and
dependency-architecture checks pass on Python 3.14.7 with twelve workers and
pytest-receptor. The provider checkout remains unchanged.
