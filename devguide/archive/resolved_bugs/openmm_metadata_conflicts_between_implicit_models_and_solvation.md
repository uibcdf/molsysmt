---
summary: OpenMM attribution metadata conflicts between implicit models and solvation.
issue: uibcdf/molsysmt#583
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, convert]
guard: tests/build/solvate/test_scientific_attribution.py
normative:
blocked_by: []
supersedes: []
---

# OpenMM attribution metadata conflicts between implicit models and solvation

**Reported:** native receiving during PR #543, reproduced on 2026-11-05.
**Status:** resolved; canonical metadata and contextual uses are contract-tested.

## What

Constructing an OBC1/OBC2 model and independently solvating the same source in
one application-owned Ackredit session produces an attribution conflict. Both
scientific operations finish, but the second capture loses the OpenMM use.

```bash
python -m pytest tests/build/solvate/test_scientific_attribution.py -k alternative --receptor=llm -n 2
```

On source `e614ba36762b536448cc25688428fee3840d18c3` with the newly added guard,
all four order/model combinations fail: the provider reports incompatible records
for `software:openmm:8.6.1`. No engine calculation failure is demonstrated.

## How

`credit_implicit_solvent` reads the common `SOFTWARE` registry. The native-ion
solvation branch creates a second record with lowercase title `openmm` and no
project URL for the same versioned identifier. Ackredit correctly rejects that
conflict. Solvation must reuse the registry, retaining its distinct execution
context and detached preparation-history record.

## Why

Applications can compare physical models, prepare multiple systems or change
their physical recipe in one workflow. Separate captures must include the
software actually reached even when another operation already credited it.
Suppressing the provider diagnostic or inventing operation-specific software
identities would conceal inconsistent provenance.

## What is measured and what is assumed

Baseline: four failures, 4.83 s, Python 3.14.7 / OpenMM 8.6.1 on Linux. The
22-atom alanine fixture produces independent implicit and explicit outputs.
The guard exercises actual OpenMM construction and solvent placement, separate
captures, an enclosing capture and native ion-replacement child attribution.
This is source receiving, not an installed/platform release qualification.

## What was refuted

This is not a conflict between OBC1 and explicit-water physics: the record that
conflicts describes their shared executable, not their scientific criteria.
Ackredit conflict detection remains enabled. Metadata-only force-field lookup
must still produce no executed-software credit.

## Scope and exclusions

Canonical metadata and contextual credit in the existing OpenMM/native-ion
solvation branch; no detector, force field, charge model, coordinates, public
signature or schema change. The full implicit-minimize, physical-recipe change,
explicit-solvate and dynamics workflow remains unqualified. Ordinary unseeded
provider ion placement is not newly attributed by this correction.

## Acceptance criteria

- Both operation orders and both OBC models retain identical software records
  and distinct contextual uses, with no tracking conflict.
- OBC paper/model/resource context and native ion-replacement uses remain intact.
- Solvation retains canonical detached provenance without changing scientific
  results or the original molecular input.
- Optional-provider absence/failure preserves completed science and bibliography;
  failure emits the existing catalog diagnostic.

## Provenance

The baseline command above uses the shared Python 3.14 development environment,
published Pytest Receptor and two workers with engine/BLAS thread limits of one.
The receiving receipt will record exact versions, public support floors and checks.

## Resolution and receiving

Solvation reads the common `SOFTWARE["openmm"]` record and adds its producer
version. Its use context records the engine, translated force-field resources,
water model and charge source; it does not share the implicit criterion's
physical context. No provider workaround or new registration API is introduced.

The six new real-engine cases pass. Both operation orders and OBC variants retain
their distinct captures and enclosing workflow uses. The native ion-replacement
child remains present. The saved solvation software item agrees with the actual
provider record, portable attribution round-trips without new calculation credit,
and metadata-only lookup remains uncredited. Actual solvent construction retains
151 atoms, 43 waters and zero ions for this fixture; the 22-atom source tables
and coordinates are unchanged. Absent and failing optional tracking give the
same coordinates and detached preparation report as the successful-provider run.

Receiving passes 1,232 affected cases, 54 published-support-floor cases and
569 documentation/doctest cases. These suites overlap. The three edited
notebooks retain their original executable cells, outputs and metadata; only
prose changes. Dependency imports, Ruff, docstrings, API stability, course and
developer-guide checks pass. Exact commands, versions, hashes and boundaries
are in the [receipt](../../../devtools/data/openmm_attribution_receiving_583_20261105.json).
Hosted controls and installed/platform release qualification remain separate
under #334; no tag, Release, promotion or complete dynamics workflow is claimed.
