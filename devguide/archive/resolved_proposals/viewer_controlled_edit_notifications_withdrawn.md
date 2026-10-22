---
summary: Withdraw the general Viewer observation request after choosing explicit reconciliation
issue: uibcdf/molsysmt#413
status: withdrawn
opened: 2026-10-22
closed: 2026-10-22
verification: inspected
area: [api, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# Viewer withdraws the general controlled-edit notification request

**Reported:** 2026-10-22 by the MolSysViewer consumer in uibcdf/molsysmt#413.
**Status:** Withdrawn following the consumer's design decision, not implemented.

## What

The original request proposed a public MolSysMT coordination boundary for supported
controlled molecular edits: notifications, edit outcomes, correspondence, consumer
lifetimes and optional pre-edit recovery. It reported a design need rather than a
reproduced defect in a supported setter. Arbitrary array/table mutation remains
separate under uibcdf/molsysmt#407.

## How

MolSysMT proposed explicit Viewer reconciliation after composing public scientific
operations directly on `view.molsys`; an independent returned system would be
incorporated explicitly. A copy is optional, and unrecorded in-place mutation
provides no molecular Undo guarantee.

The consumer's [withdrawal](https://github.com/uibcdf/molsysmt/issues/413#issuecomment-6353744305)
confirms that no general native observer/subscription API is currently needed.
Operations initiated through a future tools integration can coordinate their own
scientific edit and scene update; direct Python calls retain explicit reconciliation
responsibility. Additional editing and preparation tools are intended for a redesigned
MolSysMT tools add-on on the Viewer side. That add-on is not implemented or qualified
by this decision, and the retired legacy add-on is not restored.

Viewer owns qualification of same-object reconciliation versus replacement,
correspondence, scene applicability, partial-write failures and optional pre-edit
recovery. Current `apply_system_edit` defaults are not certified as a lossless
refresh. Equal axis counts do not establish correspondence. A concrete missing
provider operation or public outcome/map can be reported separately with consumer
evidence; that possibility does not retain the generic request as an open dependency.

## Why

The requesting consumer explicitly permits closure as withdrawn after the revised
product boundary. Closing records that the general provider deliverable is no longer
required; it does not claim an observer API, redesigned add-on or new synchronization
contract has been implemented. MolSysMT's existing ownership, units, validation,
scientific invalidation and return semantics remain the public tools consumed.

## What is measured and what is assumed

Source of the decision: the consumer comment dated 2026-10-22 at 23:39:25 UTC.
No runtime measurement or new implementation is claimed. Viewer #259 retains its
separate receiving/ownership work; the consumer reports Viewer #262 fixed separately.
Those outcomes are not requalified here.

## Scope and exclusions

This is the disposition of uibcdf/molsysmt#413 only. It does not change dependency
floors, freeze a new pair, authorize a release, or complete the remaining acceptance
under uibcdf/molsysmt#250, uibcdf/molsysmt#254 and uibcdf/molsysmt#334. The publication
pause and preserved historical package identities remain in effect.

## Closure

Archive this decision and close #413 as withdrawn. No regression guard is invented
for an observer implementation that was never added. Future bounded provider needs
require their own evidence and ownership, reusing an existing issue when appropriate.
