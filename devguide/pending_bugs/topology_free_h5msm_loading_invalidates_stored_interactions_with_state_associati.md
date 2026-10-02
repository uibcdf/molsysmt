---
summary: Topology-free H5MSM loading invalidates stored interactions with state associations
issue: uibcdf/molsysmt#291
status: active
opened: 2026-10-02
closed:
severity: high
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Topology-free H5MSM loading invalidates stored interactions with state associations

**Reported:** 2026-10-02, integrated local full-suite validation.
**Status:** Corrected; final integrated validation pending.

## What

Reading a H5MSM 0.5 containing structures, chemical states, named analyses and
explicit frame-to-state associations erases the analyses' evaluated coverage
and observations when no topology layer is present.

```bash
python -m pytest --receptor=llm tests/form/file_h5msm/test_topology_free_molsys_v05_probe.py
```

## How

`read_topology_free_molsys_file` attached the stored analyses before restoring
frame-to-state assignments. The chemical assignment setter correctly invalidates
existing analyses, but reconstruction is not a user edit. Reconstruct and
validate the assignments first, then attach the stored analyses, matching the
complete-system reader's order.
The synthetic fixture also now establishes chemistry before attaching its analysis.

## Why

The reader silently loses valid scientific observations and evaluated-empty
coverage on a supported round trip. Public edits must continue to invalidate
stale analyses; suppressing invalidation in the setter would hide real edits.

## Scope and acceptance

The topology-free regression suite must preserve records, remapped queries,
chemistry associations, copy and pickle results. Geometry and chemistry edit
regressions must continue to pass. The correction changes reconstruction order
without changing the H5MSM schema or weakening association validation.

## Provenance

Linux x86_64, Python 3.13.14, local editable suite environment, 2026-10-02.
