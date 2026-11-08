---
summary: Topology and Structures composition rejects explicit copy_if_all
issue: uibcdf/molsysmt#656
status: open
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [convert, basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit copy policy fails in a native two-domain shortcut

**Reported:** 2026-11-08 while preparing a sequence-fit reference under #421.
**Status:** open; the Viewer consumer uses ordinary independent composition.

## What

`msm.convert([topology, structures], copy_if_all=False)` raises
`TypeError: molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_MolSys() got
an unexpected keyword argument 'copy_if_all'`. The same public composition
without that option succeeds. Public conversion notes describe explicit native
copy-policy behavior; this shortcut cannot receive that keyword.

## How

The existing two-domain shortcut receives the keyword from public conversion
without admitting it. A minimal independent reproduction to retain is:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures, Topology

coordinates = msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
msm.convert([Topology(n_atoms=2), Structures(coordinates=coordinates)],
            copy_if_all=False)
```

## Why

General consumers cannot request the documented copy policy on this native
composition. The failure happens before result publication; no data loss is
observed. Sequence-reference preparation now uses the admitted default instead
of adding a second domain-composition implementation.

## Evidence and limits

The `sequence-panel-directed-context` capped source attempt reproduces this
TypeError through the consumer. Public conversion implementation is unchanged
from source `6dbfb5048`; the consumer is a declared working tree. Its first
case passes and its external-reference case fails during Review. No clean
minimal-case qualification, True-policy case or complete conversion matrix is
yet claimed. The preceding projection failure and fixture corrections are
separate observations, retained under #421.

## Acceptance criteria

Admit the documented True/False copy policy through the existing owner, retaining
independence/default behavior and single-owner domain constraints. Guard both
item orders, source immutability, selected axes and already owned/unowned native
domains. Verify malformed options remain rejected. Do not silently ignore a
copy request or bypass existing validation.

## Scope

Two-domain Topology/Structures composition and its general public copy contract.
No new scientific algorithm, schema, optional engine or release permission.
No change to unrelated composition routes or frozen gate weights is implied.

## Provenance

Linux/Python 3.14 development source, published PyUnitWizard 0.28.1 and
Pytest Receptor 1.2.1; observed 2026-11-08 under one-CPU/two-GiB service limits.
Exact runtime, raw logs and source fingerprints remain with #421 receiving.
