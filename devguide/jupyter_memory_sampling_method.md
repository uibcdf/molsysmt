# Receiving Jupyter memory measurements

**Role:** operational method under uibcdf/molsysmt#723, 2026-11-12.
This is private receiving tooling, not a public molecular API or a claim that
a memory leak has been identified or fixed. The existing long scientific
receiver still retains its original raw sampler; it does not yet use this
method. Original functional outcomes and diagnostic experiments keep their
source/runtime scope.

## Method and controls

The helper is `tests/molsysviewer_molsysmt/jupyter_memory_sampling.mjs`.
It observes three windows with the same API order:

| Window | Operations before measurement | Interpretation |
| --- | --- | --- |
| `raw` | Exposed GC and the page metric in one evaluation | Declared raw method, not evidence that every retired target collected |
| `after_tasks` | Two completed MessageChannel tasks | Task separation without an additional explicit CDP collection |
| `after_collection` | Two CDP collections separated by completed tasks | Defined bounded collection method, not universal proof of retirement |

Each window records performance.memory, Runtime.getHeapUsage and
Memory.getDOMCounters sequentially, then optional primitive lifetime
observations. Start/end times delimit the window. They are not simultaneous
API calls. Keep both metric values; do not add them, expect equality or
attribute their difference to collection timing alone. CDP backing-storage
bytes are distinct from its JavaScript heap and from operating-system RSS,
GPU memory and complete process-family accounting.

Subject observers return primitive values only. Do not retain Playwright
handles, remote objects or target objects in their returned evidence. A
WeakRef inspection can keep a target alive until its JavaScript job ends;
the helper crosses tasks after inspections before collecting again. The
sequence is fixed: there is no retry-until-clear or minimum-of-repeated-heap
selection. Missing required metric/GC capabilities fail the explicit control.

The browser control has independent retained-witness, deliberately retained
object/backing-buffer and actually released object/backing-buffer subjects.
After the deliberate reference is removed, both its WeakRefs must clear. The
retained witness and its sentinel data must survive throughout. A separate
CDP backing-storage observation must decrease when the eight-MiB control is
released (one-MiB tolerance for unrelated small allocations). The guard cannot
pass simply by reporting every target collected.

## Plain-host baseline

The private launcher accepts `--scenario host-memory --host-groups 3`; one
group is three ordinary toolbar executions with output clearing. The allowed
range is one through seven groups, checked before runtime files are created.
Only the controlled notebook kernel executes the baseline. It asserts that
MolSysMT, MolSysViewer, their addon and AnyWidget are absent from sys.modules
at setup and completion. This does not claim that their packages are absent
from the controller environment or that installed frontend extensions are
disabled.

The browser records its actual page configuration and cell-toolbar settings
before/after; equality is checked from those observations. It does not hide
cell toolbars or disable an extension. The server's own startup messages
identify the Python package and web application directories; selected files
are hashed before/after, with explicit unavailable/ambiguous states. These
are bounded application receipts, not every static asset or an installed-pair
qualification. Credential-bearing server logs remain private; the identity
extractor does not serialize unrelated lines or tokens.

## Commands and scope

Use the qualified development interpreter, existing browser/Playwright and
controlled provider roots. No shared-environment installation or user settings
change is needed.

```bash
python -m pytest --receptor=llm -n0 \
  tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_chromium_memory_sampling_retained_and_released_controls
python -m pytest --receptor=llm -n0 \
  tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_plain_jupyter_memory_baseline
```

Set `MOLSYSVIEWER_ROOT` to the declared frozen source/runtime. Missing
prerequisites fail when selected. These explicit browser guards remain
outside default scientific collection. Select shared-host CPU/RAM limits,
reserve, finite process deadlines and PID-safe cleanup before execution.
The 63-case owner control receiving is separate from the pending actual
Jupyter baseline, scientific integration and comparable long campaign.

## Technical basis and remaining work

The task/lifetime reasoning follows the
[ECMAScript WeakRef rules](https://tc39.es/ecma262/multipage/managing-memory.html#sec-weakrefderef).
The existing MolSysViewer lifecycle guard supplies prior receiving practice
for independent witness/model/backing-buffer controls; this extends that
approach with explicit API windows. See uibcdf/molsysviewer#315/#356 and
[Playwright's CDP interface](https://playwright.dev/docs/api/class-cdpsession),
[Chrome memory guidance](https://developer.chrome.com/docs/devtools/memory-problems)
and the protocol types shipped with the recorded Playwright installation.
No new molecular scientific method or Ackredit attribution is introduced.

Receive the actual plain-host baseline, compare default-host and diagnostic
ablation scopes separately, and agree the concrete scientific receiver
integration before selecting another comparable long campaign. A passing
synthetic control alone does not establish which objects Jupyter retains or
qualify molecular memory behavior. #615's original initialization cause,
installed/platform and final-candidate acceptance remain separate.
