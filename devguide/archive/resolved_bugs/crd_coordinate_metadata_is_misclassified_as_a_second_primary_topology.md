---
summary: CRD coordinate metadata is misclassified as a second primary topology
issue: uibcdf/molsysmt#388
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: reproduced
area: [basic, form]
guard: tests/_private/test_molecular_system_validation.py::test_crd_with_partial_topology_is_complementary_to_psf
normative:
blocked_by: []
supersedes: []
---

# CRD coordinate metadata is misclassified as a second primary topology

**Reported:** 2026-10-13, during the full local #382 adoption suite.
**Status:** Resolved in source with the existing CRD classification guard.

## What

Public conversion of the bundled complementary POPC CRD+PSF pair raises
MultipleMolecularSystemsError. The existing classification guard and three
structure flip/principal-axis controls fail before scientific execution.

```python
import molsysmt as msm
msm.convert([msm.systems['POPC']['popc.crd'], msm.systems['POPC']['popc.psf']])
```

## How

The CRD adapter pipes its atom/group metadata through molsysmt.Topology for
bulk delivery. The general classifier uses that pipe as its default evidence
of a primary topology when provides_primary_topology is absent. CRD carries
coordinates and partial labels, while PSF supplies the primary topology. A
conversion pipe does not establish a second independent molecular system.

Set the existing provides_primary_topology host flag to False in the CRD
adapter. Keep its topology pipe and converters, so atom-count consistency and
metadata delivery remain available. Reuse the existing general classifier;
do not add a filename-specific exception to it or remove CRD capabilities.

## Why

The defect refuses an established complementary-input workflow, including
public conversion and structure operations. It does not demonstrate coordinate
or connectivity corruption: the classifier refuses input before those operations.

## What is measured and what is assumed

The full Python 3.14 local suite reports four CRD-related failures. All four
reproduce in isolation. Restoring the five changed #382 runtime modules from
9ae0f8102 reproduces the same failures; the prepared modules are then restored
byte for byte. This establishes an existing defect, not an indexed-loader
regression. An unrelated PDB canonical-spelling assertion also fails in both
runtimes and is accounted for in the #382 validation record.

## What was refuted

Changing the registry or suppressing the multi-system error does not fix the
classification evidence. Removing the topology pipe would discard a supported
metadata-delivery route. Changing the general classifier to accept every pair
would admit actual competing primary topologies and inconsistent atom axes.

## Scope and exclusions

One adapter admission flag. No parser, chemical inference, molecular selection,
coordinate geometry, units, IDs or other form classifications change. This source
repair does not qualify a new installed release candidate.

## Acceptance criteria

The existing CRD+PSF classification guard must fail before repair and pass
with SINGLE/VALID and both actual atom counts afterward. The three existing
structure controls must execute and retain their literal coordinate/axis truth.
CRD getter/converter and genuine-multiple/inconsistent-complementary controls
must remain valid.

## Provenance

Linux, Python 3.14.7, shared development environment, 2026-10-13. Source baseline
9ae0f81028ef3914a4eef2d126dbe602e120221e; provider runtime identical to admitted
DepDigest 0.15.1. Bundled POPC inputs; no downloads or new environment.

## Resolution — 2026-10-13

The CRD adapter now declares provides_primary_topology=False while retaining
its metadata pipe and supported converters. 90 nearby classification, structure,
CRD and PDB-identifier tests pass with twelve workers and pytest-receptor. The
existing primary guard protects the SINGLE/VALID result and checks both actual
atom counts; genuine competing-topology and inconsistent-axis controls remain.
The three geometry tests execute their original numerical assertions.
No general validation rule is relaxed and no new dependency is introduced.
