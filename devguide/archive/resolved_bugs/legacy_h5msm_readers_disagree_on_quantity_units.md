---
summary: Legacy H5MSM readers disagree on quantity units and silently guess missing metadata.
issue: uibcdf/molsysmt#240
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [form, units, h5msm]
guard: tests/form/file_h5msm/test_legacy_unit_contract.py
normative:
blocked_by: []
supersedes: []
---

# Legacy H5MSM readers disagree on quantity units and silently guess missing metadata

**Reported:** Existing upstream issue, rechecked locally on 2026-10-02.
**Status:** Resolved with executable regression guards.

## What

On main 78981d6c1, a legacy dataset declaring angstrom under a root declaring nm was read as 1 nm by get and 0.1 nm by conversion. Missing units also fell back silently to nm, ps, or square nanometers.

## How

The legacy getters, converter, and iterator selected different metadata. The shared private resolver now validates populated structural datasets when opening a legacy handler. Dataset declarations are considered first, then explicit group/root declarations. All available declarations must agree physically; synonyms are accepted. Invalid dimensions, missing declarations, and conflicting scales raise the catalog FormatError before exposing the handler, which is closed on failure. Velocity units can derive from explicit length/time; B-factor units require an explicit B-factor declaration: the legacy writer chose their unit independently of its coordinate length unit.

## Why

The same coordinates must retain the same physical meaning in every read, query, iteration, and migration route. A tenfold difference is a scientific defect.

## What is measured and what is assumed

The old failures were reproduced against main 78981d6c1. The focused tests
exercise the corrected paths. No unit is inferred from numerical values.

## What was refuted

Coherent bundled files do not demonstrate safety for contradictory metadata.
Always preferring a dataset or always preferring the root would make readers
agree but still silently choose one physical scale. Duplicate declarations
are therefore checked rather than resolved by precedence alone.

## Scope and exclusions

Parity covers coordinates, box, velocities, B factors, time, temperature, and both energies; get, conversion, iteration, and migration; dataset-only and container-only metadata; and a nondefault angstrom/fs policy. Existing coherent legacy fixtures remain supported with their deprecation warning. New public writes already use the 0.5 dataset-local units and strict canonical schema checks. The future integrity codec remains owned by uibcdf/pyunitwizard#82 and uibcdf/pyunitwizard#83; no tamper-proof digest or codec adoption is claimed.

## Acceptance criteria

The addressable guard `tests/form/file_h5msm/test_legacy_unit_contract.py` must pass and fail when its reported mechanism
returns. The public documentation and affected course modules describe the
observable behavior.

## Provenance

Linux x86-64, CPython 3.13.14, NumPy 2.4.6, Pandas 2.3.3, h5py 3.16.0;
2026-10-02. Focused pytest runs use the repository's Pytest Receptor profile.
