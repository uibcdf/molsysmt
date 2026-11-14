---
summary: Native copy client probe still requires chemical storage on Topology.
issue: uibcdf/molsysmt#751
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: low
verification: reproduced
area: [tests, native]
guard: devtools/tests/test_qualify_topomt_native_copy.py
normative: devguide/native_copy.md
blocked_by: []
supersedes: []
---

# A native-copy client probe requires retired topology chemistry

**Reported:** 2026-11-14, during the finite pre-1.0 technical handoff review.
**Status:** corrected and received in the bounded source scopes below.

## What

The documented `python -m devtools.scripts.qualify_topomt_native_copy` command
contains a stale ownership assertion: it accesses
`copied.topology._chemical_states_domain`. Current Topology deliberately
rejects that attribute, including when attached to MolSys. Chemistry belongs
to the independently attached `MolSys.chemical_states` domain. A correct
native copy therefore fails the probe instead of receiving its actual domain
ownership. This is a developer-tool defect, not a defective molecular copy.

## How

Extract the existing six ownership assertions into the private
`_check_domain_ownership` helper, called at the same point in the original
probe. With its original assertion unchanged, the seven-case molecular
regression has six failures and one pass: five cases encounter the retired
attribute, and a deliberately injected retired store is incorrectly accepted.
The helper introduces no new production copy path or public molecular API.

The correction checks independent chemistry through the MolSys domain,
retains real weak-owner checks for copied topology, structures and chemistry,
and refuses the four retired chemical attributes on Topology. All original
coordinate sharing, independent registry/metadata, geometry edit, evaluated
coverage and occurrence assertions remain in the probe.

## Why

An advertised developer command must exercise the maintained native-domain
contract. Requiring a removed competing chemical store blocks useful receiving
and can misdirect a contributor toward restoring invalid ownership. The
severity is low because the normal molecular operations and release tests do
not depend on this optional source-client probe.

## What is measured and what is assumed

The original ownership clause has a discriminating seven-case failure witness.
The corrected clause and existing copy, benchmark and hierarchy tests pass
170 cases without failures, skips or warnings. Source inputs remain unchanged
during each bounded run. This is local Linux/Python source receiving, not a
new TopoMT scientific, installed-package or current-remote qualification.

The local TopoMT checkout is preserved: clean, one commit ahead and 227 behind
its fetched upstream. It is not silently merged or used as evidence for that
newer upstream. Any literal client probe records its actually imported source
and scope separately. The literal command also passes both eager/deferred
copy paths on that preserved historical checkout; it does not receive the
227-commit newer upstream. Its source state and four inspected client-file
hashes remain unchanged.

## What was refuted

Restoring chemical storage or a bonds/components facade on Topology would
contradict the accepted independent-domain design. Removing all ownership
assertions would make the command accept a copied domain bound to the wrong
system. Real corruption controls instead retain those refusals.

## Scope and exclusions

Only the developer probe, its focused guards and operational explanation are
changed. No runtime API, native binary, scientific criterion, dependency,
third-party source, package, release or publication permission changes.
Historical 2026-10-22 TopoMT measurements remain historical. Representative
additional client workflows remain owned by #408 and their consumers.

## Acceptance criteria

- The probe accepts both eager and deferred real native copies.
- Wrong domain owners, shared source chemistry and a resurrected topology
  chemical store are refused.
- Existing registry, coordinate, occurrence and invalidation checks remain.
- Relevant tests, documentation/governance checks and Ruff pass before the
  fix is published and the issue closes.

## Execution record

The [receiving receipt](../../../devtools/data/native_copy_probe_receiving_751_20261114.json)
retains the original six-failure clause, successful 170-case cohort, literal
historical-client command, source identities and bounded-resource observations.
Each execution uses one CPU, a 2-GiB limit, no own swap and a 6.5-GiB host
reserve. Final checks and publication retain their actual identities; no
complete current-client or final-pair claim follows.
