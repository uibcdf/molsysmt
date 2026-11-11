---
summary: Fresh import-order timeout lacks pre-deadline child diagnostics
issue: uibcdf/molsysmt#713
status: partial
opened: 2026-11-11
closed:
severity: medium
verification: reproduced
area: [tests, api]
guard: tests/molsysviewer_molsysmt/test_element_utilities.py::test_import_timeout_preserves_original_error_and_child_diagnostics
normative:
blocked_by: []
supersedes: []
---

# Diagnosing the bounded fresh-import timeout

## What

The complete source session on `f0dbb58e0` executes 33,841 cases: 33,824 pass,
16 skip and one child-import check exceeds its existing 60-second deadline.
The failing parameter is `molsysmt.element.atom` in
`test_fresh_import_orders_preserve_native_exports_and_discovery`.
The receptor's canonical final record and native JUnit agree on that failure.
The earlier 49 schema/integration failures do not recur.

## What is known and unknown

A single isolated invocation of all three original import orders on the same
clean source and frozen providers passes three cases in 14.51 seconds. It keeps
the original program, assertions and child deadline. That is a different
session; it does not relabel the complete failed session or explain its cause.
No incorrect export/query result is observed. Import deadlock, environment
interference, I/O and resource scheduling have not been causally distinguished.

The complete run used three workers under 3-CPU/6-GiB/no-own-swap limits. The
application daemon restarted; native pytest survived but its original external
supervisor did not. A persistent rescue monitor retained the 6.5-GiB host reserve,
original finite deadline and unchanged source/client/provider hashes. Its
external child-wait status cannot be recovered. This custody gap is explicit
and separate from the genuinely failed test and its reported pytest exit 1.
This is not the #615 first-canvas timeout.

## Missing evidence and bounded correction

The old child emits only a final success sentinel. TimeoutExpired retains
partial streams, but the test does not expose them to the captured report.
The first stalled child therefore supplies no pre-deadline stack.

Arm the standard-library faulthandler at 45 seconds, retain the original
60-second subprocess deadline and all original first-application-import orders,
functional assertions and success sentinel. Cancel the diagnostic timer on
normal completion. On timeout, copy available text/byte child streams into
captured stderr and re-raise the same exception. Do not warm imports, expand the
deadline or infer environmental disposal from one isolated pass.

The original functional program AST and its two parent result assertions remain
unchanged. New negative controls protect diagnostic transport and exception
identity; actual fresh-process guards still run. The change affects tests only,
not library startup, scientific methods or public API behavior.

## Remaining acceptance

Diagnostics are a partial correction, not a causal resolution. The next deliberate
complete corrected-source receiving must retain any pre-timeout stack and runner
status through a durable supervisor. If the timeout recurs, use the new evidence
to identify its owning cause. A passing isolated rerun alone cannot close this
report or clear the failed full-suite backlog. Preserve the original deadline
until an explicit evidence-based scope decision says otherwise. Final installed,
platform and exact-candidate gates remain separately required under #334.

## Provenance

2026-11-11; Linux/Python 3.14.7, unchanged native ABI3 4ffb82e4, exact frozen
MolSysViewer 5164f13b and the same CI-pinned support overlays as the full session.
Pytest Receptor 1.2.1 validates the complete canonical stream; its phase-detail
cap and incomplete extension channel are retained explicitly. Related work:
#334 local receiving and #122 resource-aware test profiling. No source-science,
installed-package or publication acceptance follows from these diagnostics.

## Diagnostic receiving — 2026-11-11

The current complete element-utility module passes 134 cases with no omissions,
including the original three real fresh processes and two controlled byte/text
timeout transports. The original exception object survives, partial child streams
are surfaced and the child deadline stays 60 seconds. Static comparison confirms
the original functional program AST, import-order parameters and two parent
result assertions are unchanged. Only the standard-library pre-deadline stack
timer and timeout reporting are added. This completes the diagnostic increment;
causal or explicitly evidenced disposition of the full-run timeout remains open.
