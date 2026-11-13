---
summary: MDTraj HDF5 iteration fails on optional fields and incomplete chunk delivery
issue: uibcdf/molsysmt#738
status: active
opened: 2026-11-12
closed:
severity: high
verification: reproduced
area: [form, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reading selected MDTraj HDF5 structure blocks

## What

The form-specific StructuresIterator unconditionally accesses optional PyTables
nodes during construction. A genuine MDTraj HDF5 file with coordinates and
embedded topology, but no box, cannot even iterate coordinates. A complete
file also leaves requested structure_index, velocities and total_energy as
None rather than delivering its available series. Direct node access assumes
canonical storage units instead of interpreting each dataset's unit metadata.

```python
import molsysmt as msm

# molsys is an open mdtraj.HDF5TrajectoryFile reader.
blocks = msm.Iterator(molsys, structure_indices=[2, 0, 2], chunk=2,
                      coordinates=True, structure_index=True)
```

The original minimal fixture raises NoSuchNodeError for cell_angles. The
complete-fixture guard detects missing structure positions. This supported
streaming path must not require a full-file native conversion as a workaround.

## How

The owner is molsysmt/form/mdtraj_HDF5TrajectoryFile/iterators.py. Constructor
node discovery ignores optional absence; next handles only some requested
fields and ignores dataset unit metadata. The default all selector also uses
len('all') when determining the traversal stop. Its separate inventory stub
cannot accept the public dispatch arguments and lacks the normal unavailable
iterator diagnostic.

The correction delegates each selected row to MDTraj's public read(1), which
already decodes units and optional series. Sorted unique read atom positions
are mapped back to the requested query order and repetitions. Coordinates and
observables remain chunk-bounded; PyUnitWizard applies the application policy.
A finally block restores the caller's cursor even on a failed read. The caller
continues to own the handle. Inventory iteration remains unavailable with a
catalogued NotImplementedIteratorError; no new inventory iterator is supplied.

## Why

A supported file may legitimately omit time, box, velocity or thermodynamic
series. Requiring those fields breaks coordinate-only streaming. Losing source
positions or returning undecoded physical values can misalign or misinterpret
analysis. This is an admitted correctness/documentation repair under #727,
not a new trajectory API or scientific algorithm.

## What is measured and what is assumed

A five-structure, four-atom deterministic fixture is written by MDTraj itself.
The valid original contract baseline has four failures and four passing
trajectory-projection controls. After repair, eighteen focused controls pass,
including public dispatch, nonconsecutive/repeated query positions, nullable
series, all/empty traversal, stored angstrom/fs metadata, pm/fs output policy,
one-row provider reads, failure restoration and DCD/XTC geometric controls.

The initial eight-failure test draft also demanded duplicate atom inventory
extraction and omitted temperature/energy standard-unit dimensions. Those
were test-contract mistakes, not eight software defects. Their raw failures
are preserved separately. Valid unique unsorted trajectory extraction already
produced coherent geometry; passing sorted positions to MDTraj now avoids its
unnecessary monotonicity warning without accepting duplicate inventory atoms.

The first complete MDTraj selection is interrupted at its explicit 180-second
wall limit (native -15), with no input changes, about 219 MiB peak and no memory
pressure. This is incomplete evidence, not a pass or a RAM failure. The separate 360-second receiving completes all 836 selected cases in
233.86 seconds, with about 252 MiB peak and two retained provider warnings
about dummy PDB CRYST1 boxes. No input changes, OOM or memory pressure occur.

## Scope and exclusions

This repair covers the existing HDF5 coordinate/observable iterator. It does
not change basic.Iterator, H5MSM, provider versions, chemistry, native kernels
or dependency floors. Available unrequested fields may also be decoded by
MDTraj for each selected row. The selected index list and returned output
still consume memory. Eager HDF5 getters/converters retain their existing
full-file read behavior. Other iterator attributes are explicitly unsupported.
No final-candidate, installed-pair or minimum-provider qualification is claimed.

## Acceptance criteria

- Minimal and complete files yield correct selected chunks with nullable fields.
- Stored physical units are decoded before applying the application unit policy.
- Source structure positions and query atom order/repetitions are conserved.
- All and empty traversal, shorter final chunks and explicit traversal controls work.
- Provider reads stay bounded and restore the caller's cursor on success/failure.
- Public unavailable inventory iteration has a structured diagnostic.
- Relevant adapter tests, source/docstring checks and actual documentation receiving pass.

## Provenance

2026-11-12, shared Linux host, Python 3.14.7, MDTraj 1.11.1, frozen development
runtime with PyUnitWizard 0.29.2, SMonitor 0.21.0, ArgDigest 0.15.0,
DepDigest 0.15.1 and Pytest Receptor 1.2.1. Sequential tests are capped at one
CPU, 1.5 GiB RAM and zero own swap, with a conservative 6.5 GiB host reserve.
The final receiving record retains exact inputs, exits and provider identities.
