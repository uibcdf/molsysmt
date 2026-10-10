---
summary: Simulation PDB export passes a structure-axis box to OpenMM
issue: uibcdf/molsysmt#379
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [form, convert, units]
guard: tests/form/openmm_Simulation/test_pdb_export.py
normative:
blocked_by: []
supersedes: []
---

# Simulation PDB export passes a structure-axis box to OpenMM

**Reported:** 2026-10-10, a real-engine scratch-lifetime test under #374.
**Status:** Resolved at the existing external adapter boundary.

## What

`openmm.Simulation` to PDB/PDBFixer conversion fails on an ordinary one-atom
Reference-platform simulation with finite coordinates and a valid context box:

```python
msm.convert(simulation, to_form='file:pdb', output_filename='simulation.pdb')
# ValueError: First periodic box vector must be parallel to x.
```

The same writer runs inside the PDBFixer bridge. The lifecycle test
`tests/form/openmm_Simulation/test_bridge_resource_lifecycle.py::test_real_fixer_remains_usable_after_scratch_retirement`
reproduces this through real OpenMM and PDBFixer, without a patched writer.

## How

`molsysmt/form/openmm_Simulation/to_file_pdb.py` obtains the canonical MolSysMT
box shape `(1, 3, 3)`, then passes the whole quantity to OpenMM's topology setter.
That setter expects one `(3, 3)` box in OpenMM units. Normalize this consumer
boundary by selecting its single current structure and converting explicitly
to nm/OpenMM units. The existing getter must retain its general structure axis
and active-unit policy. Reuse PyUnitWizard conversion rather than a new box store
or a geometry helper for an adapter-specific dimension conversion.

## Why

Existing advertised export and fixer routes cannot complete this ordinary
conversion. The defect predates the #374 lifetime repair. It is independent of
scratch cleanup, atom chemistry and candidate criteria. Public export needs
both the current context's box and coordinate pose, even if a source topology
contains older box vectors.

## What is measured and what is assumed

Linux/Python 3.14.7, source ae0ad2404e5e1550cc5da791c67f0529d7377483 plus
uncommitted #374 scratch changes: the real-engine test fails at the unchanged
box setter. Ten other lifecycle/selected-bond tests pass. This does not certify
another platform or an installed candidate. No trajectory or dynamics run occurs.

## What was refuted

The box is valid: the getter preserves the required general structure dimension,
while the external consumer requires one box. Changing that getter to omit its
structure axis would break the MolSysMT data convention. Stubbed file readers
cannot establish successful scientific conversion through the real writer.

## Acceptance criteria

- Export the single current pose and context box, with unchanged source topology.
- Retain explicit unit conversion under a non-default session length policy.
- Verify the real eager fixer remains usable after intermediate retirement.
- Preserve signatures, selected atoms and explicit caller-file custody.
- Document the boundary and name an addressable regression guard.

No new simulation, interaction detector or public format is introduced. Frozen
candidate selection, refs and publication remain paused under #334.

## Resolution — 2026-10-10

**Contract-tested.** The writer selects `box[0]` and uses PyUnitWizard's explicit
nm/OpenMM conversion for the topology setter. A copied topology receives the
current context box; the source topology remains intact. The unnecessary
structure_indices delegation to a topology-only converter is removed without
changing either signature. The coordinates already use the existing explicit
OpenMM conversion in the final text writer. No getter axis/unit convention changes.

The guard module independently asserts coordinates and periodic box after parsing
actual PDB output, a different retained source topology box, selected atom pose,
atom count and caller path. Both nm and angstrom session policies fail before
repair with the same OpenMM ValueError and pass after repair. The real PDBFixer
lifecycle case also succeeds without patched converters. The combined #374/#379
selection above passes **13 tests**; three changed docstrings pass strict Sphinx
rendering. Napoleon deprecation warnings do not represent rendering errors.

Public writer notes, Foundations file guidance, Simulation Toolbox, conversion
Cookbook and shared Common Core module 12 describe the current-context and unit
boundary. This is source validation on Linux/Python 3.14.7, not installed-candidate
or cross-platform qualification. The frozen release identities remain unchanged.

Focused Ruff checks and `git diff --check` pass. All 14 fast release gates
pass, including adapter delivery, dependencies, devguide integrity, shared
course structure and public smoke. These checks are development evidence,
not heavy or installed-artifact candidate qualification.
