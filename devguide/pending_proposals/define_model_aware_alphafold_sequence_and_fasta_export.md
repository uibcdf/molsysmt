---
summary: Post-1.0 model-aware AlphaFold sequence and FASTA export
issue: uibcdf/molsysmt#733
status: open
opened: 2026-11-12
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Model-aware AlphaFold sequence export

## What

Post-1.0, define and implement sequence/FASTA export from AlphaFold identifiers
with explicit correspondence to the chosen model. #732 corrects an existing
false-success stub by refusing before I/O; that bug closure does not implement
a writer. This new capability is deferred under #334's finite handoff cutoff.

## How

First settle whether the request represents the selected model's groups, its
source accession's complete sequence, or an explicitly chosen alternative.
Do not assume these index spaces correspond. Review fragments, model versions,
chains, missing positions and source naming/selection semantics against the
authoritative provider contract. Record unknown correspondence instead of
silently substituting a sequence.

Reuse existing general sequence/group queries, source-preserving FASTA records,
native partial systems and resource-safe writer tools in their owning modules.
Provide any missing reusable capability there. Keep identifier-specific resolution
in the adapter, with ArgDigest, lazy optional providers and SMonitor diagnostics.
Avoid a second sequence parser or competing chemical-state store.

## Why

A registered function that returns a filename without writing is unsafe. Its
removal of false success is immediate correctness work; defining a trustworthy
model-aware export is a distinct scientific/API capability and must not become
an unplanned pre-1.0 expansion.

## Acceptance

Agree scientific sequence scope and index correspondence before implementation.
Qualify selected/reordered groups, versions/fragments, ambiguous or missing data,
metadata and remote failures. Use deterministic offline model/sequence fixtures,
plus a separately identified service receiving when justified. Verify actual
FASTA records, file creation, ownership, cleanup and atomic preservation on
failure. Document route availability and examples; only then replace #732's
explicit refusal and claim working direct export.

## Owner and revisit

MolSysMT owns the adapter and public contract. Revisit after 1.0 or an explicit
maintainer admission prompted by a demonstrated stable-scope requirement.
The current source study is inspected; no real network, sequence-alignment,
new writer, scientific or installed qualification is claimed.
