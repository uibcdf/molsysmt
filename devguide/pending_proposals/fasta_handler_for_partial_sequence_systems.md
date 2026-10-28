---
summary: Add a resource-owning FASTA handler for partial sequence systems.
issue: uibcdf/molsysmt#519
status: open
opened: 2026-10-28
closed:
verification: inspected
area: [form]
guard:
normative:
blocked_by: []
supersedes: []
---

# FASTA handler for partial sequence systems

## What

Provide a public FASTAFileHandler, its molecular-system form and per-form
iteration, building on source-preserving #513 and the bounded native sequence
conversions in #517. A collection of sequences can be one partial molecular
system with separate declared molecular occurrences. A FASTA record is never
a coordinate structure.

## Proposed boundary

The read-only handler owns the source resource and deterministic close/context
semantics. Sequential record/block access must avoid materializing the complete
file. Optional indexed access uses source record positions and guarded byte
ranges. Keep byte offsets distinct from the decoded-character source spans in
molsysmt.fasta_source@1. Changes/replacement of the source invalidate stale
indexed reads; this is source binding, not chemical authentication.

Reuse one shared parser for raw text, file records and the handler; do not add a
third independent FASTA interpretation. Whole-system queries expose genuinely
available groups/molecules/labels. Iteration can provide sequence subsystems or
blocks of them. Preserve duplicate/empty records, opaque headers and source
maps. Keep literal raw input separate from explicit normalized molecular views.

## Scope and dependencies

#517 supplies the native partial table construction. #518 completes the ordered
chain/group relation, native queries and selectors, hierarchy extraction,
construction and dictionary/H5MSM persistence without atoms. Reuse those tools
rather than reconstructing hierarchy in the handler. Resource/indexed I/O,
streaming record iteration and source binding remain this proposal's work;
none may create CA atoms, infer coordinates or merge molecular identities. A new sequence value class remains separate under #242.

## Acceptance

Qualify form discovery and truthful attributes, supported get/info/conversion
parity, resource/copy/close lifetime, bounded iterator reads, source mutation
rejection, byte/character correspondence and repeated/empty records. Measure
memory, first/indexed query costs and block sizes with identified inputs.
Document public methods, existing-reader delegation and known native limits.
No release or installed-package qualification follows from source exposure.
