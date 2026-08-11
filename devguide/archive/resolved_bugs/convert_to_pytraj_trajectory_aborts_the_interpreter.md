---
summary: Converting into pytraj.Trajectory kills the process with SIGABRT, uncatchable from Python.
issue: uibcdf/molsysmt#138
status: resolved
opened: 2026-08-08
closed: 2026-08-11
severity: high
verification: measured
area: [form, convert]
guard: tests/form/pytraj_Trajectory/test_conversion_contract.py::test_an_incompatible_pytraj_build_is_rejected_without_a_native_abort
normative:
blocked_by: []
supersedes: []
---

# Converting into `pytraj.Trajectory` aborts the interpreter

## What

The PyTraj 2.0.6 binary installed in the Python 3.13 development environment aborts the
interpreter when a `pytraj.Frame` is destroyed. That unsafe finalizer is reached by both
plain PyTraj and MolSysMT conversions into `pytraj.Trajectory`; it cannot be caught as a
Python exception.

MolSysMT also had independent adapter defects: the `molsysmt.MolSys` origin imported the
wrong topology converter, the PDB edge bypassed `PDBFileHandler`, the trajectory form did
not implement its structural getters, and two topology conversion edges used the wrong
source object or import alias.

## How

The upstream failure reduces to the following program on Python 3.13.14 with the
installed PyTraj 2.0.6 binary:

```python
import pytraj as pt

frame = pt.Frame(2)
del frame
```

It terminates with `double free or corruption` and exit status 134. The equivalent
Python 3.12 environment, using PyTraj 2.0.6 and NumPy 1.26.4, completes ordinary
trajectory construction, indexing, iteration, and RMSD calculation.

The working tree now detects the unsafe Python 3.13 binary before constructing a frame
and raises `NotSupportedFormError`. PDB input is first converted through the consensus
PDB/native route, and the corrected native-to-PyTraj path is used afterwards.

## Why

A declared conversion target must not be able to destroy a notebook, a test worker, or
a long-running analysis. This is especially important for generic form inventories and
conversion audits, where one unsafe native extension otherwise loses all results from
the process.

PyTraj remains a Tier 3 form. Pre-1.0 work therefore covers crash containment, honest
capability reporting, and basic interoperability; it does not promote PyTraj to Tier 1
or require its advanced extraction, append, merge, and iterator surface to be exhaustive.

## Investigation

### Measured environment

- Python 3.13.14, NumPy 2.4.6, PyTraj 2.0.6: the minimal `Frame` program aborts with
  exit status 134.
- Python 3.12, NumPy 1.26.4, PyTraj 2.0.6: the positive interoperability path passes.
- Direct `pytraj.load(pdb)` aborts without importing MolSysMT.
- `pytraj.iterload(pdb)` can return an object, but materializing or indexing it reaches
  the same unsafe frame lifetime and aborts.
- Constructing `pytraj.Trajectory(xyz=..., top=...)` is not a sufficient workaround:
  indexing, iteration, RMSD, or finalization can still enter the unsafe code.

The diagnosis is therefore upstream for the native abort, not merely inferred from the
MolSysMT call stack.

### Upstream source evidence

The installed extension exposes both `Frame.__del__` and `Frame.__dealloc__`. PyTraj
commit `50e48b403` ("Support Cython 3") removes `Frame.__del__`; current local source at
`~/repos@others/pytraj` contains only `__dealloc__`. This explains why the installed
binary can free the same native allocation twice.

This source inspection is strong causal evidence, but it is not an empirical claim that
current PyTraj builds successfully on Python 3.13: its upstream CI presently covers
Python 3.10--3.12, and building the current source requires Cython and cpptraj headers
that are not present in the active environment.

### Refuted hypotheses

- **MolSysMT supplies malformed coordinates.** Refuted by the two-line plain-PyTraj
  reproducer, which allocates no MolSysMT object.
- **Only `pytraj.load` is unsafe.** Refuted by direct `Frame` destruction and by the
  constructor-from-arrays path.
- **Avoiding explicit iteration is sufficient.** Refuted because object finalization
  alone can abort.
- **The `MolSys` `is_empty` exception has the same cause.** Refuted. It was an
  independent import error in the adapter and is fixed separately.

## Implementation checkpoint

The bounded pre-1.0 repair currently does the following:

1. Rejects a Python 3.13 PyTraj extension that still exposes the obsolete
   `Frame.__del__`, before native frame construction can occur.
2. Routes `file:pdb -> pytraj.Trajectory` through `PDBFileHandler` and the native
   consensus representation instead of calling `pytraj.load` directly.
3. Corrects the `molsysmt.MolSys -> pytraj.Trajectory` topology-converter import.
4. Supports non-periodic native systems whose box is absent.
5. Implements trajectory getters for coordinates, box, time, and structure count.
6. Corrects the trajectory-to-topology extraction and native-topology converter alias.
7. Declares the native topological and general pipe forms, resolving part of the
   accepted non-Tier-1 adapter debt.
8. Adds subprocess crash containment, positive Python 3.12 interoperability,
   selection, multi-structure ordering, non-periodic construction, round-trip, getter,
   and pipe tests.

The defect is resolved even though upstream Python 3.13 support remains unavailable:
the MolSysMT contract is that an incompatible native binary is rejected safely, not that
MolSysMT makes every PyTraj build compatible.

## Acceptance criteria

- An incompatible PyTraj extension cannot terminate a MolSysMT conversion process.
- A compatible PyTraj installation can convert a PDB and a native `MolSys` into a
  usable trajectory, including atom selection and requested structure order.
- Coordinates and boxes round-trip through PyTraj within numerical tolerance.
- A native system without a box produces a non-periodic PyTraj trajectory.
- `get_form`, direct getters, and topological piping report the form honestly.
- The form-adapter and conversion-fidelity ratchets gain no new debt.
- PyTraj remains Tier 3; advanced completeness is explicitly outside this issue.

## Residual risk and follow-up

- A PyTraj binary with a different native lifetime defect but without `Frame.__del__`
  would pass the targeted guard. The positive subprocess tests provide broader coverage
  in compatible environments, but native extensions cannot be made risk-free from
  Python alone.
- Current-source PyTraj on Python 3.13 has not been built locally. If PyTraj later claims
  Python 3.13 support, CI should add a positive job rather than weakening the safety
  guard.
- Exhaustive Tier 3 operations remain governed by the general non-Tier-1 form debt; they
  must not delay the 1.0 release or the paper.

## Verification commands

```bash
python -m pytest --receptor=llm \
  tests/form/pytraj_Trajectory/test_conversion_contract.py \
  tests/form/pytraj_Topology/test_conversion_contract.py

python devtools/scripts/validate_form_adapters.py
python devtools/scripts/audit_conversion_fidelity.py
python devtools/scripts/validate_dependencies.py
ruff check molsysmt tests/form/pytraj_Trajectory tests/basic/test_get_form_battery.py
```

Final verification on 2026-08-11:

- Python 3.13 broad conversion surface: 398 passed, 9 safely skipped.
- Python 3.12 positive PyTraj contract: 13 passed.
- Ruff, dependency validation, form-adapter validation, conversion-fidelity audit, and
  developer-guide validation: passed.
