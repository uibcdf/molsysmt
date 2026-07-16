# Reliable Performance Regression Gate

**Status:** Proposed

## Why

The current CI compares one current median with a stored median using a fixed
15% threshold on a hosted runner. It does not calibrate runner noise, compare
sample distributions, require identical benchmark keys, or verify scientific
outputs as part of the gate. New and missing metrics can escape enforcement.

## Proposal

Keep fast benchmark feedback, but distinguish an advisory noisy-runner signal
from a release-grade regression decision.

## How

1. Store raw samples and a benchmark schema/version.
2. Fail or explicitly approve added, removed, and renamed benchmark keys.
3. Add cheap correctness/parity assertions before timing.
4. Calibrate each run with stable controls and reject visibly unhealthy runners.
5. Use repeated interleaved baseline/candidate trials or a statistically sound
   comparison rather than unrelated dated medians.
6. Pin thread counts, precision, dependency versions, and cache state.
7. Write current results to CI artifacts, not a tracked baseline filename.
8. Use dedicated hardware or repeated confirmation for release-blocking claims;
   keep hosted-runner results advisory when variance is high.
9. Separate time, peak memory, and startup budgets.

## Acceptance criteria

- Identical code has a measured false-positive rate within an agreed budget.
- Deliberate controlled slowdowns are detected reliably.
- Schema/key drift cannot pass silently.
- Every timed result is scientifically validated.
- The report records enough environment and sample data to reproduce the call.
