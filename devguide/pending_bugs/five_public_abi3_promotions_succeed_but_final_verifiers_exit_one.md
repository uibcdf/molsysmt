---
summary: Five public ABI3 promotions succeed but final verifiers exit one
issue: uibcdf/molsysmt#246
status: active
opened: 2026-09-25
closed:
severity: medium
verification: reproduced
area: [release, conda, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Five public ABI3 promotions succeed but final verifiers exit one

**Reported:** 2026-09-25, during MolSysMT 0.22.4 build-3 promotion.
**Status:** Active; public files verified independently, workflow defect open.

## What

The five native promotion runs `36128498551`, `36128498646`,
`36128498419`, `36128498721` and `36128498399` passed their exact-file
promotion action and uploaded receipts, then failed in the common final
`Independently verify the public package record` step. Each sampled final
step printed its expected public URL immediately before exiting 1.

## How

The precise exit-1 mechanism in `.github/workflows/promote_conda_package.yaml`
is not yet established. Make the public-record check independently rerunnable
without invoking label mutation again, then add a test for its complete
success path. Align the implementation with Viewer through
`uibcdf/molsyssuite#48` and the general release pattern in
`uibcdf/molsyssuite#27`.

## Why

An apparently failed release may lead operators to repeat a promotion or
misreport public availability. Both are avoidable when the mutation receipt
and read-only verification are distinct evidence surfaces.

## What is measured and what is assumed

Measured: all five action steps and receipt uploads passed; independent
`conda search --override-channels -c uibcdf` queries found all five exact
public filenames and SHA-256 digests. The public installed-pair matrix
`36129993869` passed 20/20 with explicit public provenance. The exit-1
mechanism remains a hypothesis, not a diagnosed root cause.

## What was refuted

No ABI3 file is missing from the public channel. The failed final step alone
does not negate the action's target-label check or the independent solver and
installed-pair evidence.

## Scope and exclusions

This report covers the false-red post-promotion verification. It does not
reopen candidate code, package bytes, or Zenodo archiving.

## Acceptance criteria

All five exact public files can be checked by a read-only workflow or command
without repeating promotion; a focused test catches a successful record
being reported as failure. The behavior is coordinated with Viewer #105.

## Provenance

GitHub-hosted Ubuntu promotion runs and a local Linux Conda search on
2026-09-25; MolSysMT 0.22.4 build 3, Viewer 0.23.4 build 5.
