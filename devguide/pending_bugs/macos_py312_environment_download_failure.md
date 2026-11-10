---
summary: Track the macOS Python 3.12 Conda download failure separately from tests.
issue: uibcdf/molsysmt#671
status: open
opened: 2026-11-09
closed:
severity: medium
verification: upstream
area: [ci, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# macOS provisioning failed before scientific execution

## What

The macOS/Python 3.12 job 129405812011 of run 42689572908 fails in Setup conda
env before imports, scientific evidence and full pytest. This cell has no
scientific certificate or JUnit. It cannot count as a pass, scientific skip,
numerical failure or rendering test.

## How

The owner independently inspected GH Run Receptor and native failed-step logs.
libmamba reports download error 28 for AmberTools 26.0 and statsmodels 0.15.0:
less than 30 bytes/sec transferred over 60 seconds. The process exits 1.
The later missing micromamba-shell cleanup error is secondary. A reason for
the slow transfer is not established; no upstream software defect is inferred.

## Why

The required platform/minor remains unexecuted. Preserve this failure separately
from #670's schema-fixture failure in the other full-suite cells and #669's
corrected source-artifact placement. The prior run's queued macOS/Python 3.14
cancellation is another distinct unexecuted attempt, not this download failure.

## Follow-up and acceptance

Receive macOS/Python 3.12 provisioning and all mandatory scientific/full-suite
steps at the next deliberately agreed corrected-source matrix checkpoint. Do
not launch duplicate matrices from both teams, omit AmberTools/science, relax
source integrity or raise scientific deadlines to label recovery. Investigate
recurrence with original metadata/logs. No local source fix or closure is
claimed for a one-off transfer failure; the pending external execution remains
owned here and in #334.
