# Advisory performance observations

This is MolSysMT's maintained performance-disposition policy, accepted by the
maintainer on 2026-11-09 under uibcdf/molsysmt#567. The
[benchmark contract](README.md) defines the required measurement record.

A scientifically correct implementation remains available even if slower than
a third-party implementation or an earlier MolSysMT version. Performance
observations guide improvement work; they do not determine public API admission,
automatically restrict a tool or waive correctness tests. Scientific validity,
units, index correspondence and data integrity retain their mandatory controls.

## Warnings and improvement issues

The default relative slowdown threshold is 15 percent. A consistent difference
above that threshold, established with equivalent tasks and compatible execution
conditions, warrants an efficiency-improvement issue or new evidence in its
existing owner. Record inputs, public route, source/runtime/provider versions,
thread/resource policy, repeated samples and uncertainty, timing and memory
costs, comparator identity, and the practical impact. Keep the correct tool
available while the issue is addressed.

Distinguish a MolSysMT change relative to its own reference from a same-workload
comparison with a third party and from a change in a direct third-party control.
A slower third-party control does not by itself identify a MolSysMT defect.
Differences at or below 15 percent generally need no efficiency issue. Material
resource costs or scientific-use constraints can justify investigation even
without crossing that timing threshold; the threshold is a review convention,
not proof of equivalence or acceptable resource consumption.

## Evidence is independent of admission

Missing, malformed or incompatible evidence is unevaluable. It cannot produce a
performance approval or justify attributing a slowdown to MolSysMT. Preserve
failures, original timings and baselines. Do not replace a reference before
comparison, silently drop slow paths, rerun until green or infer comparability
from matching benchmark names alone. Baseline renewal is a separate reviewed
operation with its own execution context and justification.

The comparer enforces the [declared session contract](comparable_sessions.md):
known compatible runtime/provider/resource/unit identities, actual workload and
measurement descriptors, and raw repetitions agreeing with their summaries.
Invalid, historical or incompatible evidence remains diagnostically unevaluable.
Complete comparable observations, including slowdown warnings, return zero;
partial or unevaluable evidence returns one. Compatibility is necessary evidence,
not causal attribution or a statistical confidence claim. No historical failed
run becomes a passing result under this policy.

The performance workflow is explicitly advisory: its job permits failure while
retaining native producer/comparison status, logs and available session artifacts.
It must not be a required correctness or release-performance gate. Failure of a
benchmark's numerical correctness checks remains evidence to investigate in the
owning scientific tests; advisory timing does not certify those results or waive
a mandatory scientific failure elsewhere. No workflow automatically disables a
public scientific implementation or automatically files an unreviewed issue.
