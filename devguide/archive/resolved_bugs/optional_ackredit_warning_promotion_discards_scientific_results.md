---
summary: Optional Ackredit warning promotion discards scientific results.
issue: uibcdf/molsysmt#305
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: measured
area: [diagnostics]
guard: tests/test_ackredit.py
normative:
blocked_by: []
supersedes: []
---

# Optional attribution warnings can replace scientific outcomes

**Reported:** 2026-10-03, during fixed-state preparation validation.
**Status:** Resolved and guarded at the shared MolSysMT attribution boundary.

## What

A failure of optional Ackredit tracking can discard completed chemical preparation
when Python promotes warnings to exceptions. Scope cleanup can likewise replace
an original scientific exception with an attribution warning.

```python
import runpy
import warnings
from molsysmt import _ackredit
from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

fixture = runpy.run_path('tests/physchem/test_chemical_template.py')
def broken_provider():
    raise RuntimeError('controlled attribution failure')
_ackredit.backend = broken_provider
warnings.simplefilter('error', AckreditTrackingWarning)
fixture['msm'].physchem.apply_chemical_template(
    fixture['_source'](), **fixture['_options'](None))
```

Before correction this exits with `AckreditTrackingWarning` although the detached
output chemistry is already prepared. Use an isolated process for this reproduction.

## How

`molsysmt/_ackredit.py::_failed` warns through the catalog-backed SMonitor bundle.
SMonitor emits the diagnostic and then correctly applies the Python warning policy.
The promoted `AckreditTrackingWarning` escapes the optional provider boundary.
The same helper is used at provider startup, crediting and scope cleanup.

## Why

All MolSysMT tools using this boundary are affected in strict-warning clients.
The optional-attribution contract requires preserving completed science, portable
host bibliography and original scientific exceptions independently of provider
health. The consumer owns the isolation failure; this is not a SMonitor defect.

## What is measured and what is assumed

**Reproduced:** The isolated command above fails under the strict filter on
Python 3.13.14. Existing tests cover ordinary warnings but not their promotion.
Other attribution consumers share the same helper; their susceptibility follows
from source inspection rather than individual end-to-end reproductions.

## What was refuted

- A caught provider exception alone does not prove optional tracking is harmless:
  its diagnostic can itself be promoted to an exception.
- Globally ignoring warnings would also suppress unrelated scientific diagnostics.
- Changing SMonitor's warning policy would alter a correctly functioning provider.

## Scope and exclusions

Catch only the promoted MolSysMT attribution warning after diagnostic emission.
Retain ordinary warning behavior and SMonitor events. Do not change warning filters,
suppress scientific errors or adopt unpublished Ackredit capture APIs.

## Acceptance criteria

- Startup, registration, tracking and cleanup failures preserve the completed result
  under strict warning filters and retain a catalog diagnostic.
- Cleanup failures cannot replace the original scientific exception.
- Ordinary attribution warnings remain observable.
- Public chemical preparation keeps its detached bibliography and successful output.

## Provenance

2026-10-03, Linux source checkout at `c19a47ada0c2279029abfa296cf915560610ad9a`,
Python 3.13.14 under migration exception uibcdf/molsysmt#237. The reproduction uses
the published ArgDigest 0.13.0 source snapshot at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` in `PYTHONPATH`; it simulates provider
failure rather than claiming a defect in an installed Ackredit release.

## Resolution — 2026-10-03

The shared boundary retains the catalog diagnostic and catches only promotion of
that same `AckreditTrackingWarning` instance. It does not change global/local
warning filters, suppress unrelated warnings or consume scientific exceptions.
Ordinary warning delivery is unchanged.

The guard observes real SMonitor events through `MemoryHandler` and requires the
attribution catalog code for backend, scope-entry, registration, tracking and
scope-exit failures under an error filter. It also requires the original scientific
exception by identity and propagation of unrelated scientific warnings. The public
preparation regression separately verifies successful chemistry and detached
bibliography with both ordinary and strict warning policies.

The pre-fix focused run had eight failures and three passes (including two real
EST controls). The corrected combined regression completed **98 passed in 34.94 s**:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/test_ackredit.py tests/physchem/test_chemical_template_est.py \
  tests/physchem/test_chemical_template.py tests/physchem/test_get_cip_stereochemistry.py \
  tests/interactions/test_scientific_attribution.py
```

Two existing pandas FutureWarnings originate in the H5MSM chemical-state reader;
they are unrelated to this defect. Ruff checks pass. This is source evidence on
the temporary Python 3.13 route, not certification of the required 3.14 matrix.
