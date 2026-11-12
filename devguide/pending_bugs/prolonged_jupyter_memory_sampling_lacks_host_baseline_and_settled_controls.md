---
summary: Prolonged Jupyter memory sampling lacks host baseline and settled controls
issue: uibcdf/molsysmt#723
status: partial
opened: 2026-11-11
closed:
severity: medium
verification: measured
area: [tests, diagnostics]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_plain_jupyter_memory_baseline
normative:
blocked_by: []
supersedes: []
---

# Qualifying prolonged Jupyter memory observations

## What

MolSysViewer reports memory growth in plain Jupyter controls without molecular
imports, and a difference between the receiver's raw same-task heap observation
and later settled/CDP samples. The receiver currently calls exposed GC, reads
performance.memory and dereferences weak controllers in one page evaluation.
Those values alone do not establish molecular retention or complete retirement.

## How

Source inspection confirms the same-evaluation GC/heap/WeakRef sequence in
prolonged_session_jupyter.mjs. The independent consumer reports plain-host
controls, default-host versus cell-toolbar diagnostic ablation, a separately
received JupyterLab wheel and three scientific diagnostic cycles. Those
experiments have not been independently rerun here. Their GC timing and heap
API comparison change two factors together; causal contributions remain open.
Original functional and raw measurement results retain their actual scope.

## Why

Receive the method before interpreting memory deltas. MolSysMT owns this
receiver; consumer lifetime attribution remains uibcdf/molsysviewer#315/#356.
This follows #718's corrected input readiness, without reopening its accepted
functional guard or explaining #615's original initialization timeout. Preserve
scientifically correct implementations and distinguish metrology uncertainty
from a proven molecular leak.

## Intended receiving and acceptance

1. Add a bounded plain-Jupyter control with actual package/application identity
   and extension settings; preserve default-host and diagnostic-ablation scope.
2. Observe post-retirement state through a defined asynchronous sequence with
   positive retained-witness and negative retired-object controls. Compare heap
   APIs at the same sampling point before attributing a difference to timing.
3. Keep scientific/window/session assertions, original deadlines and recorded
   resource limits. Receive a concrete owner-reviewed correction and actual
   GUI regressions before another comparable long campaign. No blind replay.
4. Preserve failures, raw/settled method labels, exact unchanged inputs, native
   identity and owned-process retirement. Do not disable routine user extensions
   or upgrade the shared environment to make a gate pass. External upstream
   publication retains its separate prior-authorization requirement.

## Scope and next action

Admitted under #334's P4 polishing intake. Review the concrete bounded receiver
proposal from the reporter; independently receive the measurement method before
selecting long-run inputs. #718 is a separate readiness/provenance closure.
No public molecular API, scientific algorithm, dependency floor or new score
weight is requested. Candidate construction, hosted qualification and
publication remain paused; installed/final-pair and human acceptance stay open.

## Provenance

2026-11-11 local intake. The owning issue records the reported c5115dff client,
matched aee7aa65 scientific Python bytes, canonical 4ffb82e4 native binary,
PyUnitWizard development copy, host controls and diagnostic scopes. Source
inspection alone does not independently validate all reported experiments.


## Owner method increment — 2026-11-12

A private Chromium sampler now records paired performance.memory/CDP heap/DOM
windows before task barriers, after two tasks, and after two explicit CDP
collections separated by tasks. Windows and API order are explicit; their
values are not treated as simultaneous instants, RSS or complete process
memory. A real browser guard retains an independent witness and a deliberately
held object/buffer, releases an unrelated object/buffer, then drops the held
control. The strengthened guard removes ordinary strong locals from the
creation-job WeakRef control and observes an approximately eight-MiB decrease
in the CDP backing-storage metric. It does not require equal heap APIs.

The affected cohort passes 63 cases, including the real Chromium control,
fresh-provider observer guards, runtime-file lifecycle, bounded host-group
arguments and actual-log identity parsing. The original one-case pilot is
retained, with its later-strengthened creation-job oracle. A plain-kernel
host-memory mode is implemented with three groups of three executions and
actual package/application path/file receipts, page configuration and toolbar
settings read before/after. Real Jupyter receiving of that mode remains pending
at this checkpoint. It does not import molecular/AnyWidget providers in the
control kernel or disable a routine extension.

At this checkpoint the long scientific receiver and its original raw measurements
are unchanged.
The method is a bounded contract-tested increment, not full #723 acceptance.
The [operational method](../jupyter_memory_sampling_method.md) records its
sequence, sources, commands and remaining host/scientific/long-run boundaries.


## Default-host receiving — 2026-11-12

Clean db1706f8a passes the final 63-case control cohort and one actual
Jupyter baseline: nine ordinary toolbar executions, with MolSysMT,
MolSysViewer/the addon and AnyWidget absent in the notebook kernel at setup
and completion. JupyterLab Python/frontend both report 4.6.4; actual startup
package/application paths, selected file hashes, page configuration and
cell-toolbar settings are observed unchanged before/after. No extension is
disabled. Default schema values are not confused with effective overrides.

After the defined collection method, nodes increase by 4,415 and event
listeners by 13,906; CDP heap increases by 4,470,140 bytes. Eleven observed
No active debugger session errors remain in the receipt. The workflow's
execution/exclusion/sampling assertions pass; it does not certify error-free
Jupyter or attribute growth to that debugger or a specific retaining chain.
This independently confirms host-side growth without a molecular workload,
not the cause of every prior molecular campaign delta.

The host service has two CPUs/three GiB/no own swap, peaks near 695 MiB and
keeps at least 12.32 GiB host available memory. The selected envelope is
unchanged and source is clean before/after. The [method receipt](../../devtools/data/jupyter_memory_method_receiving_723_20261112.json)
owns all paired API windows, non-additive counts, oracle refinement, source
and runtime identity, expected scope and raw diagnostic observations.

The guard above protects this partial baseline only. At this checkpoint #723
remains partial and the scientific receiver is byte-identical to the earlier
source. The next increment below receives the concrete molecular integration
before a comparable long campaign; no whole-current-main, installed or final-pair
qualification or publication is implied.


## Molecular receiver integration received — 2026-11-12

The owner integration preserves the original legacy raw observation, labels
its method, and adds the received three-window sampler after actual frontend
disposal. Weak native targets cover the notebook's initial/recovered molecular
controllers, structures, models, coordinate axes and backing buffers. An
independent molecular witness is intentionally retained as the positive owner,
with its coordinate signature checked. Retired rows are discarded only after
their observations pass and are preserved in the per-cycle receipt. Popup
functional assertions remain; this is not a census of every popup realm/object.

Source inspection also identifies a receiver-owned ElementHandle in bind()
that was not explicitly disposed. The integration releases owned root/result
handles; the actual Chromium control proves deliberate remote-handle retention
and collection after disposal. This is observer hygiene, not a demonstrated
cause of the original molecular/host growth. The affected 63-case cohort
passes. Original Python scientific fixture bytes, assertions and deadlines
remain unchanged; the producer inserts a passive loaded-provider snapshot
into the existing closing cell before its completion marker, without adding
a scientific calculation or warming absent modules.

The bounded actual molecular pilot passes on clean 1a899f9f0. The original
scientific fixture is byte-identical to 95bac785e; both popups, scientific
calculations, coordinate edits, stale-analysis rejection, coherent recovery
and requested active playback pass. In the defined after-collection window,
all six selected targets and each 3,720,000-byte buffer clear for the initial
and recovered 62-atom views. The independent 3,983-atom witness, its 47,796-byte
buffer and coordinate signature survive. The separate remote-handle control
also distinguishes retained from disposed subjects.

All eight actually loaded module hashes after the workload match the frozen
selected input envelope, including the addon and Rust binary. Generated
module-version labels are retained as observations, not used as source
identity. The 4,913-file selected envelope stays unchanged before/after, with
clean source on both sides; MolSysViewer is the independently matched c5115dff
source and the composite snapshot uses published PyUnitWizard 0.29.2. This is
not the original aee7aa65/PyUnitWizard 0.29.4dev thirty-cycle composition.

The three-CPU/3.5-GiB/no-own-swap service peaks at 2.18 GiB and preserves at
least 11.20 GiB host available memory, with no resource stop/OOM. Sampling
adds 1,003.314 ms. Eight No active debugger session page errors are retained;
the baseline list overlaps them. Successful scientific assertions do not
certify error-free Jupyter or identify the retaining chain.

The [molecular receipt](../../devtools/data/molecular_memory_receiving_723_20261112.json)
owns observations, actual inputs, command/results, resources and the correction
to the raw wrapper's inherited Chromium-only description. Its command actually
selects the scientific prolonged-popup guard; the raw record remains preserved.
#723 remains partial until a comparable long campaign with explicit frozen
composition and comparison question. Retention attribution, #615/#713,
installed/platform/final-candidate gates and publication pause keep their scope.
