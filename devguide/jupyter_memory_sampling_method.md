# Receiving Jupyter memory measurements

**Role:** operational method under uibcdf/molsysmt#723, 2026-11-12.
This is private receiving tooling, not a public molecular API or a claim that
a memory leak has been identified or fixed. The scientific
receiver preserves its original raw sampler and now has a separate integrated
three-window observation received in one actual molecular pilot. Original
functional outcomes and diagnostic experiments keep their
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
The 63-case owner control receiving and one actual nine-execution Jupyter
baseline pass on clean db1706f8a. The integrated molecular pilot passes on
clean 1a899f9f0, with its own 63-case control cohort. The comparable long
campaign remains pending; these overlapping cohorts are not additive coverage.

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

The default-host baseline below is received within its stated scope. Keep
diagnostic-ablation comparisons separate. The concrete molecular integration
is now received below; agree the frozen composition and comparison question
before another long campaign. A passing
synthetic control alone does not establish which objects Jupyter retains or
qualify molecular memory behavior. #615's original initialization cause,
installed/platform and final-candidate acceptance remain separate.


## Observed owner checkpoint — 2026-11-12

The [receipt](../devtools/data/jupyter_memory_method_receiving_723_20261112.json)
records all three API windows for zero/three/six/nine executions with matching
4.6.4 package/application metadata and unchanged observed configuration.
After collection, the plain-host node/event/CDP-heap deltas are +4,415 /
+13,906 / +4,470,140 bytes. The eleven No active debugger session errors
remain visible evidence; successful cell assertions are not a clean-Jupyter
claim or proof of that error's causal role. Collection is an intervention:
its timing envelope can be derived from the first window's start through the
last window's end, including barriers/GC. Do not compare normal cycle latency
without accounting for it. The original raw observation and scientific fixture are retained; the new
molecular sampling adds its own separate evidence.


## Molecular observer ownership

`prolonged_native_lifetimes.mjs` records weak native owners for the initial
and recovered notebook views. The witness snapshot is explicitly retained
for a positive control; retired snapshots have no intentional strong owner.
Actual controller disposal is received before the fixed collection method,
then selected controller/structure/model/axis/backing-buffer reachability and
witness values are checked. Rows are pruned only after recorded acceptance.
This does not inventory every historical structure, popup realm or renderer
allocation. The original scientific/window/session assertions remain.

The receiver releases its owned ElementHandle and readiness-result handles
after binding. [Playwright handles](https://playwright.dev/docs/api/class-jshandle)
can otherwise keep their referenced objects alive. An actual retained/disposed
remote-handle control receives that behavior without molecular assumptions.
Historical raw values keep their original scope; this correction does not
establish what caused their growth. Sampling overhead is separate from
functional cycle time. The existing closing notebook cell also records
providers actually loaded after scientific work; it does not force an import.

## Actual molecular pilot — 2026-11-12

Clean 1a899f9f0 passes one actual 5,000-structure scientific cycle with both
popups, coordinate edits, stale-analysis rejection, session recovery and active
playback. After the defined collection method, all six selected native targets
and the 3,720,000-byte coordinate buffer clear for both the initial and recovered
62-atom views. The independent 3,983-atom witness and its 47,796-byte buffer
remain reachable, with unchanged coordinates. These are selected native owners,
not a census of popup realms, renderer allocations or total memory retention.

The existing raw measurement is retained. Sampling adds 1,003.314 ms in this
cycle; its window timestamps and both heap APIs remain separate. Eight observed
No active debugger session errors are retained (the baseline list overlaps);
the passing workload does not certify error-free Jupyter. The actual after-use
kernel snapshot matches all eight selected provider/module file hashes, including
the Rust binary and addon, without forcing their initial import.

The [molecular receipt](../devtools/data/molecular_memory_receiving_723_20261112.json)
owns the exact client/provider composition, private artifact hashes, preserved
fixture and observations. The three-CPU/3.5-GiB/no-own-swap service peaks at
2.18 GiB, keeping at least 11.20 GiB host available memory. #723 remains partial
until the comparable long campaign; original #615/#713 causality, installed
qualification and the final-pair publication pause are unchanged.
