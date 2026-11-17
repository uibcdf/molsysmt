---
summary: Potential energy decomposition drops terms and ignores live OpenMM context state
issue: uibcdf/molsysmt#773
status: resolved
opened: 2026-11-17
closed: 2026-11-17
severity: high
verification: reproduced
area: [api]
guard: tests/molecular_mechanics/get_potential_energy/test_get_potential_energy.py
normative:
blocked_by: []
supersedes: []
---

# Potential energy decomposition changes its input and can give incorrect terms

The public OpenMM-backed `get_potential_energy(decomposition=True)` path can
report a sum different from the energy of the same live context. It also changes
the source System's force groups. Found during the
[OpenMM capability study](../../pending_proposals/openmm_openmmtools_capability_review_20261117.md).

## Reproduction

Observed on MolSysMT `a57f4c51b4feafc54cad2677c862cae85c4e2534`, Python 3.14.7,
and the development environment's installed OpenMM 8.6.1 CPU platform.
The three independent two-particle contexts use only custom bond forces.
No integration steps are needed. Numbers below are in kJ/mol.

| Model and analytic value | Public total | Decomposed terms | Source groups before → after |
| --- | ---: | --- | --- |
| Two forces named `bond` with constant energies 2 and 5 | 7.0 | `bond: 5.0` | `[6, 9]` → `[0, 1]` |
| `U=k r`, distance 0.5 nm, Context `k=9`, System default `k=2` | 4.5 | `scaled: 1.0` | `[4]` → `[0]` |
| Periodic `U=r`, separation 2.6 nm, live cubic side 4 nm, System default side 6 nm | 1.4 | `periodic: 2.6` | `[3]` → `[0]` |

The repeated-name case can be reproduced with the following command in the
existing development composition. The two-particle model and its expected sum
are independent of MolSysMT's decomposition.

```python
import molsysmt as msm
import openmm as mm
from openmm import unit

system = mm.System()
for _ in range(2):
    system.addParticle(12)
for constant, group in [(2, 6), (5, 9)]:
    force = mm.CustomBondForce(str(constant))
    force.setName("bond")
    force.setForceGroup(group)
    force.addBond(0, 1, [])
    system.addForce(force)
platform = mm.Platform.getPlatformByName("CPU")
context = mm.Context(system, mm.VerletIntegrator(0.001), platform, {"Threads": "1"})
context.setPositions([mm.Vec3(0, 0, 0), mm.Vec3(0.25, 0, 0)] * unit.nanometer)
puw = msm.pyunitwizard
print(puw.get_value(msm.molecular_mechanics.get_potential_energy(context), to_unit="kJ/mol"))
terms = msm.molecular_mechanics.get_potential_energy(context, decomposition=True)
print({key: puw.get_value(value, to_unit="kJ/mol") for key, value in terms.items()})
print([force.getForceGroup() for force in context.getSystem().getForces()])
```

The successful witness used one CPU, a 1 GiB memory cap, zero own swap, a
45-second ceiling and 107.5 MiB peak. Earlier attempts failed in the witness
before evidence was collected: the first assumed unit conversion returned a
NumPy scalar, and a Reference retry aborted during context construction under
a 32-task cap. The CPU retry used one OpenMM thread and a 128-task cap.
Those earlier attempts do not establish a separate provider defect.

## Cause

`molsysmt/molecular_mechanics/get_potential_energy.py` aliases the supplied
OpenMM System, assigns group numbers directly to its forces, creates a second
Context and sets only positions. A dictionary indexed by `force.getName()`
overwrites earlier terms when labels repeat. The temporary Context starts from
System defaults for the box and global parameters. Live per-force parameter
updates also need an explicit support decision if an implementation reconstructs
a Context. Existing native-input parity tests do not exercise these three cases.

## Acceptance criteria

- Keep the source System and Context intact even if evaluation raises. Check
  groups, positions, live parameters, box and energy across repeated calls.
- Preserve all contributions, with accurate identity and deterministic handling
  of duplicate names. Keep the established dictionary keys for supported models
  whose names are unique. Resolve duplicate labels without silently losing energy.
- Verify against independently calculated values and the live Context total for
  each admitted model. Use the live box and active parameters. If a given runtime
  model cannot be reproduced faithfully, report that limitation before returning
  scientific values. A clone alone does not establish live-state equivalence.
- Review direct and reciprocal terms, the force-group count limit, engine
  properties and custom force classes. Each unsupported case needs an explicit
  diagnostic. Never present a partial sum as a complete decomposition.
- Cover supplied Context and Simulation routes as well as the existing native
  route. Preserve public units and validation, and exercise the MolSysViewer
  addon if the returned terms or diagnostic contract changes.

Prefer the existing owned mechanics adapter and its validation and diagnostic
facilities. OpenMMTools' inspection and context-compatibility patterns inform the
review. This issue's repair has no dependency on OpenMMTools.

## Resolution — 2026-11-17

The adapter queries each force's groups directly on a supplied, initialized
OpenMM Context, including the Context of a Simulation. This reads the current
positions, box, global parameters and force parameters. Direct and reciprocal
groups belonging to one force contribute to one entry. A repeated force name
gets its zero-based force index, with further disambiguation for literal name
collisions. Results keep dictionary order and the caller's PyUnitWizard units.

Supplied models require distinct groups for distinguishable forces, with
group assignments matching the initialized engine state. A shared group yields
one energy for all its forces. The adapter raises an actionable diagnostic
and the total-energy query remains available. For internally constructed
models with overlapping groups, a separate Context on the same platform
uses an independent System copy and the captured positions, box and global
parameters. This path supports up to 32 forces. The original force groups
remain intact in either route. The adapter checks that the sum of the terms
reproduces the finite Context total. This check detects missing energy from
stale groups in the guarded example. Users must assign groups before
initialization for the group-to-force map to be authoritative.
[OpenMM Context](https://docs.openmm.org/latest/api-python/generated/openmm.openmm.Context.html)
and [NonbondedForce](https://docs.openmm.org/latest/api-python/generated/openmm.openmm.NonbondedForce.html).

The first focused run has eight passes and one failure. Its overlap diagnostic
loses the actionable detail in the default SMonitor template. Passing an
explicit message resolves that failure. The corrected run passes nine cases.
The expanded run passes all 60 cases, with 32 expected legacy H5MSM warnings.
The independent oracles cover duplicate names and a literal collision, active
global and per-bond parameters with a different live box (15.6 kJ/mol), a
separate Ewald reciprocal group, and source integrity. The cohort includes
native construction, the platform/model-recipe contract and the MolSysViewer
addon's two unit profiles. The 8.2.0 upstream wrapper and group APIs were
inspected. Runtime checks used OpenMM 8.6.1 on CPU and Python 3.14.7.
Pytest Receptor and JUnit agree with the native exit. The expanded run used
one CPU and a 2 GiB enforced limit, with a 410 MiB peak and zero own swap.

Ruff and the public API, dependency, docstring, course and notebook schema
checks pass. The tutorial was executed and its terms checked against the
total in kJ/mol. The four course notebooks and Cookbook retain their
committed code and outputs. A strict full Sphinx build produced 1,401 HTML
files with zero warnings, and the six links to the revised tutorial resolve.
This is bounded local source evidence. Platform, installed pair and final
candidate qualification remain part of #334.
