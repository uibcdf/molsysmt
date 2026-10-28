---
summary: Convert amino-acid sequences to native topology without synthetic atoms.
issue: uibcdf/molsysmt#517
status: resolved
opened: 2026-10-28
closed: 2026-10-28
verification: reproduced
area: [form]
guard: tests/form/test_sequence_only_topology.py
normative:
blocked_by: []
supersedes: []
---

# Convert amino-acid sequences to native topology without synthetic atoms.

## What

Add public Topology and MolSys conversions for the one-/three-letter sequence
forms, and replace FASTA's implicit representative-CA construction with declared
groups and molecular occurrences. Use one private native constructor beneath
the public adapters, existing code tables and native type classification.
No atom, bond, coordinate, protonation or complete molecular identity is inferred.

## Bounded first delivery

The maintainer accepts deferring the concrete atom-free hierarchy limitations
in uibcdf/molsysmt#518. Store known group names/types and group-to-molecule
membership, source record labels and separate molecule/entity/chain slots.
The existing native schema cannot store/query group-chain membership without
atoms; do not invent temporary parallel schema fields or claim full sequence
hierarchy fidelity. No broad selector/builder/schema redesign is included.

Strings support group-position selection using the existing sequence-selection
contract. Three-letter decoding retains caps and other recognized group names.
Unknown one-letter symbols, stops/gaps and incomplete three-letter tokens must
not silently become atoms or concrete amino acids. Empty declared occurrences
remain partial inventories, not physical chemical realizations. FASTA retains
its existing optional normalized SeqRecord reader; #513's source-preserving
reader remains independent and unchanged.

## Acceptance

Public/direct conversion tests check zero stored atoms/bonds/structures, exact
group names/order/types, strict source group selections, labels and repeated/
empty FASTA occurrences. Preserve the existing normalized and raw FASTA paths.
String conversion works with Bio imports blocked. Copy and supported H5MSM
round trips retain the represented tables. Document source slots versus chemical
identity, missing atom inventory, global multisequence string concatenation and
unsupported group/chain selection/extraction in #518.

## Scope

This is converter delivery before a FASTA handler; no streaming/indexed handler,
new sequence class, inference of equality between records, atomic builder change
or package/release publication is included. The handler will reuse this base
and the source-preserving parser. Existing atomic construction remains explicit.

## Resolution — 2026-10-28

Accepted and implemented with the explicitly bounded scope above. Two new
string adapters provide direct Topology and MolSys targets. A private native
constructor fills existing canonical tables from group records; it never adds
an atom or invokes atomic rebuilding. Native code tables interpret one-letter
canonical, rare and ambiguous codes; direct three-letter decoding preserves
caps, recognized group names and unresolved alphabetic names. Unsupported
one-letter symbols/stops/gaps and incomplete/nonalphabetic three-letter tokens
raise instead of silently becoming placeholders. Known group classification
and molecule typing reuse their owning native tools. The initial unknown-name
test used ZZZ, which is an actual catalogue entry; the corrected fixture JJJ
is independently unregistered and retains unknown type.

FASTA's existing optional normalized Bio reader is retained. Its topology
conversion now reuses the same constructor, removing the former CA-per-position
projection; a new direct MolSys route keeps all records, including repeats and
empty declared occurrences. All represented IDs are strings. Empty occurrences
are unpopulated record-level declarations, not complete chemical realizations;
entity slots are not a sequence-equality deduplication policy. Numeric group
selection on strings keeps order/repetitions. FASTA atomic selections and all
coordinate-structure requests reject explicitly. Its original positional
arguments/defaults remain; the intentional keyword-only structure_indices=all
addition is registered for signature review.

### Validation

- Initial native red run: 32 failures. First bounded delivery: 32 passed.
- Expanded native string/FASTA suites and all six new/updated converter doctests:
  150 passed with Pytest Receptor and 12 workers.
- Final selection including native Topology/hierarchy/operation regressions,
  source notebook schemas and heading guards: 717 passed, zero failures. The
  14 legacy-H5MSM warnings remain visible; they are unrelated to the new routes.
- Direct string conversion to MolSys is independently tested with every Bio
  import blocked in a fresh process. Existing Bio codecs, record parsing and
  source-preserving readers remain covered by the retained suites.
- Explicit expected names, cap types, molecular memberships, source labels,
  empty atom/bond/structure tables, invalid inputs, copy and H5MSM persistence
  are asserted. The tests do not accept native limitations as correct behavior;
  those remain open separately in #518.
- The new course example is executed independently. Existing biological course
  cells/outputs are preserved. The two string form pages and FASTA page keep
  their six-cell layout, old routes and updated conversion inventories.
  Foundations and Cookbook explain the represented/physical inventory boundary.
  Strict parallel Sphinx compilation has no warnings or notebook errors.

This is represented-table contract/parity coverage, not atomic chemistry or
scientific profile qualification. No persistent schema, native selector/builder
behavior, package floor, release or atomic construction tool is changed.
Remaining hierarchy limits are retained in #518 and the resource-owning handler
is separately scoped in #519. No new public sequence class is introduced.

The final focused 40-case pass additionally checks unavailable chemical
connectivity/component completeness and distinguishes an empty FASTA document
from a retained empty declared record. The FASTA native route keeps its existing
amino-acid interpretation; raw ingestion remains alphabet-agnostic. No automatic
DNA/RNA-versus-peptide disambiguation is claimed.
