---
summary: Native container guidance retains retired chemical authority and stale persistence emphasis
issue: uibcdf/molsysmt#725
status: active
opened: 2026-11-12
closed:
severity: low
verification: inspected
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native container ownership and persistence guidance

## What

The MolSys foundation still says that copied ChemicalStates shares chemical
authority with Topology, while the current Topology explicitly refuses bonds,
components and chemical states. The MolSys.topology docstring similarly promises
compatibility facades. Several native pages emphasize old 0.5/experimental 0.6
persistence without identifying the current default 1.0 writer. The ChemicalStates
page ends with an empty peptide-endpoint heading.

## How

Inspect the published source 9323111cff4e78509520c677e420c9470a635049:
MolSys topology and chemical-state binding are independent; Topology rejects
shadow chemical fields. Existing native owner tests exercise these semantics.
The H5MSM 1.0 tool page already executes the public default writer and preserves
unresolved mechanical requests rather than parameterizing a system. The native
foundations have not reconciled all of their earlier explanatory paragraphs.

## Why

Readers need one consistent account of stable inventory, state-local chemistry
and physical structures, especially when composing domains, copying them or
choosing a persistent representation. Documentation must not reintroduce a
removed chemical facade or imply that stored requests are prepared parameters.
This is bounded pre-1.0 instructional work under #334/#378, not a new design.

## Acceptance and limits

Correct the descriptions and link current default persistence while retaining
explicit older-format limits. Execute the actual native composition/copy/default
round-trip example, checking physical values, ordered/repeated source indices,
partial chemistry, independent domains and temporary-file cleanup. Receive the
existing default writer's mechanical example under nm/ps and pm/fs as well.
Verify course guidance, relevant native doctests, rendered articles and links.
Do not change scientific algorithms, storage schema, dependency floors, public
signatures or source/installed/final-pair qualification scope.

## Receiving

Source diagnosis is inspected, not an original runtime defect. Actual example
receiving and documentation build results will be recorded here with exact
source/runtime identity, failed attempts and conservative resource bounds.


## Bounded example receiving — 2026-11-12

The actual new foundation blocks and existing H5MSM 1.0 tool example pass four
initial cases under nm/ps and pm/fs. A later six-case cohort also executes six
unchanged Core04 cells (10, 13, 15, 17, 19 and 22) under both policies; no full
course execution or changed notebook output is claimed. Expected coordinates,
times, element symbols, repeated atom positions, reordered structures, partial
connectivity, independent chemical edits and preserved unresolved mechanical
requests are checked independently of the example's own assertions. Temporary
files are gone after loading while resident domains remain usable.

The native MolSys/ChemicalStates/Structures doctests plus existing chemical-owner
and Topology-tutorial context pass 34 cases. These overlap the example scope and
are not an additive full-suite count. Selected inputs remain unchanged during
each bounded run. Each service uses one CPU/1.5 GiB/no own swap; initial and final
example peaks are about 192/189 MiB, with at least 13.60/14.13 GiB host available
memory. Context peak is about 171 MiB, preserving at least 12.90 GiB.

The review also corrects a contradictory whole-domain replacement sentence:
controlled topology/chemical_states/structures replacements notify the MolSys
owner; raw table/private writes do not. The two code edits change docstrings
only. Public signatures, validation, unit management, scientific behavior,
mechanical status and dependency floors remain unchanged. Existing ArgDigest,
DepDigest, SMonitor and PyUnitWizard boundaries are used by the executed public
calls; there is no new scientific method requiring Ackredit registration.

Complete strict HTML and actual article/link inspection remain pending at this
checkpoint. This supplemental work earns no duplicate score credit and leaves
#723/#615/#713, complete-source/nightly and final-pair qualification separate.
