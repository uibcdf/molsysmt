---
summary: Selection expression evaluation wraps resource failures as argument errors.
issue: uibcdf/molsysmt#756
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: medium
verification: reproduced
area: [basic, selection]
guard: tests/basic/select/test_resource_failures.py
normative:
blocked_by: []
supersedes: []
---

# Selection mistakes resource exhaustion for invalid input

**Reported:** 2026-11-14 by BindingMT during its fixed native selection-snapshot work.
**Status:** corrected; public identity/cause guards, full selection suite, doctest and strict documentation receiving pass.

## What

BindingMT reports that public `msm.select` wraps injected `MemoryError` and
`OSError(errno.ENOMEM)` in `ArgumentError`. The original resource exception
remains its cause, but its type and identity no longer reach the consumer.
`KeyboardInterrupt` and `SystemExit` already propagate unchanged. The exact
consumer source/native identity and synthetic reproducer are in #756; this
owner record does not relabel that upstream run as local execution.

## How

Inspection confirms the shared expression-evaluation try/except in
`molsysmt/basic/select.py` preserves ArgumentError/CatalogException and wraps
other Exception instances. Preserve the original object with a bare raise
for MemoryError and only the ENOMEM case of OSError. Keep ordinary parser
exceptions, their causes and provider/catalog argument diagnostics intact.
Exercise the real public boundary with normal digestion, all applicable
syntax dispatches and any affected direct inventory/bond evaluation paths.
Private backend injection is test instrumentation, never a consumer workaround.

## Why

Capacity failure is not evidence of invalid selection input. Client error
handling and shared-resource disposition need the real exception identity;
consumers should not unwrap causes or add competing selectors.

## What is measured and what is assumed

The original handler is locally inspected. Owner synthetic reproduction uses
one atom at the real public boundary; detailed outcomes are recorded below. No real memory exhaustion,
large allocation, native build, installation or held client campaign is needed.

## Scope and exclusions

Correct exception propagation and its public diagnostics/guards. Do not change
selection syntax, numerical results, units, ordering, chemistry or provider
floors. Preserve the separate client receiving and final-pair requirements.

## Acceptance criteria

- Real public calls preserve the same MemoryError and OS ENOMEM objects.
- Other OSError/parser failures retain ArgumentError and their original cause.
- Catalog/provider argument errors and process-control exceptions still propagate.
- Focused tests use synthetic failures without allocation pressure; applicable
  documentation and local quality checks pass.

## Reproduction and correction — 2026-11-14

The original 37-case public-boundary cohort has sixteen genuine failures and
21 passes. MemoryError/OS ENOMEM identities fail across all three syntax
dispatches, native Topology/ChemicalStates/H5MSM inputs and direct inventory/bond
routes; ordinary parser/catalog/process-control behavior already passes.
The expanded evaluator probe confirms failures at actual Pandas/MDTraj
methods. Two initially chosen MDAnalysis cases do not reach their evaluator:
they request the explicitly unimplemented native MolSys-to-Universe conversion.
Those failures remain harness precondition failures, not resource-route proof.
A targeted inspection receives that NotImplementedConversionError. The final
MDAnalysis case constructs its supported Universe form from the bundled PDB
before injecting the method failure. No new conversion is implemented or claimed.

The public selector re-raises MemoryError alongside its existing ArgumentError
case and re-raises OSError only when errno equals ENOMEM before ordinary
parser wrapping. Both are bare raises. Existing catalog exceptions and ordinary
parser-error causes retain their previous handling. No new public function,
dependency, numerical criterion, native kernel or consumer workaround is added.
The existing ArgDigest/chemical-state/SMonitor boundaries remain active.

## Final receiving

The full selection suite and public select doctest pass **244 cases, no skips,
failures or errors**, including 45 focused exception cases. The supported
receptor reader agrees with same-invocation JUnit. Nine existing legacy-H5MSM
warnings are retained. The controls cover plain and pre-chained resource
objects, their notes/causes, the reporter's explicit state/structure request,
all registered syntax dispatches, direct/native/file routes, actual evaluators,
ordinary invalid expressions/other OSError and unchanged catalog/process-control
exceptions. No actual memory exhaustion is induced.

The first corrected broad run has 240 passes and two unsupported-input fixture
failures; it is not relabelled as passing. The final supported-input cohort,
then the added exact plain-error controls, receive their own executions. A fresh
strict full-site build produces 1,400 pages without Sphinx warnings. Five actual
API/foundations/tool/cookbook/course articles contain the new contract. Existing
notebook code and stored outputs are retained; narrative-only changes do not
manufacture new execution marks or notebook receiving.

The final selected session uses one CPU, peaks below 0.5 GiB under its 2-GiB
limit and preserves more than 16 GiB host-available memory. The isolated Sphinx
build has its separate 2-GiB cap and exceeds neither the host reserve nor its
own limit. Raw unsuccessful outcomes, exact runtime/source identities and
scope are in the [receiving receipt](../../../devtools/data/selection_resource_receiving_756_20261114.json).

## Client and release boundary

BindingMT #111 still owns its exact-source end-to-end receiving at the public
consumer boundary. This owner closure does not accept that client path, restart
held populations or qualify a published package/native/installed pair. No native
rebuild or environment change is required by this Python-only correction. The
original source qualification and final-pair gates keep their actual identities;
the new runtime delta does not inherit exact-head qualification from an older
source. Candidate, hosted, tag and publication operations remain paused.

## Client receiving — 2026-11-14

BindingMT #111 publishes actual public-consumer receiving at
`8ebca138486f374d6530431c0486ef4f7c36039c`, against exact owner fix
`6deb0200cd7e384128eded46caaf751a57e65bc6`. The published account reports 20
failures/109 passes on original 27ba3d4c and 129 passes under each ordinary and
pm/fs policy on the correction. Its 48 additional controls leave the public
selector intact and exercise first/recheck failures, inventory/one structure,
atom/group outputs, actual Pandas evaluation and unchanged parser diagnostics.
The selected consumer cohort reports 1118 passes per policy with no skips.

The [owner review](../../../devtools/data/binding_resource_client_review_756_20261114.json)
independently verifies both published document/test Git blob identities and
inspects the actual BindingSite.from_selection guard. Raw XML, origin and
resource receipts remain in the client's custody and are not replayed here.
This accepts that finite public-resource boundary. The client's unchanged
2dbcf13d native file differs from the owner's 4ffb82e4 reference; neither this
Python-only receiving nor the account authenticates the whole native ABI.
#256's distinct storage/default profile, #615, installed/platform qualification
and the final coordinated pair remain separate. No held work or publication is
resumed by this receiving.
