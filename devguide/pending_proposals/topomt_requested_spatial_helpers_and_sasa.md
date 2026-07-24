# TopoMT-Requested Spatial Helpers and SASA Configuration

**Status:** partially resolved — Part 1 (configurable probe radius) implemented; Part 2 (grid helpers) pending a module-taxonomy decision  
**Requester:** TopoMT  
**Owner:** MolSysMT

> **Part 1 — DONE.** `physchem.get_sasa` now accepts a unit-aware
> `probe_radius` argument (explicit default `'1.4 angstroms'`) and an
> `n_sphere_points` argument controlling the Shrake–Rupley sampling density, both
> honoured by the native `MolSysMT` engine (CPU JIT and the CUDA/Taichi GPU
> kernels, which already threaded both parameters) and the `mdtraj` engine. The
> sampling density was unified to a default of 240 sphere points across both
> engines (previously native 100 / mdtraj 960), a balance between speed and
> angular quantization error. Digesters were added under
> `_private/arg_digestion/argument/{probe_radius,n_sphere_points}.py`. Regression
> tests: `tests/physchem/get_sasa/test_get_sasa_probe_radius.py` and
> `test_get_sasa_n_sphere_points.py`. Both current engines support the arguments,
> so no capability-error path was needed; the `else` branch still raises
> `NotImplementedMethodError` for unknown engines. Follow-on accuracy/performance
> methodologies are tracked in `sasa_methodologies_and_acceleration_post_1_0.md`.
>
> **Part 2 — still pending.** The generic `grid_volume` / `overlap_matrices`
> helpers require first deciding whether MolSysMT owns generic spatial-analysis
> primitives (candidate `molsysmt.analysis` module) and confirming a second
> sibling consumer. Tracked below.

## Purpose

TopoMT has identified two capabilities that may belong in MolSysMT because they
are generic molecular-system or spatial-analysis services rather than
TopoMT-specific topology logic.

## 1. Configurable Probe Radius in `physchem.get_sasa`

### Use case

Pocketeer parity requires solvent-accessible surface area with a configurable
probe radius for classifying buried alpha spheres. The current
`molsysmt.physchem.get_sasa` public signature does not expose `probe_radius`, so
TopoMT cannot request the upstream method's polar-probe configuration through
MolSysMT.

### Current TopoMT workaround

TopoMT constructs a Biotite `AtomArray`, converts coordinates to angstroms,
calls `biotite.structure.sasa` with a configurable probe radius, and converts
the result back to standard area units.

### Desired contract

- expose an optional, unit-aware `probe_radius` argument;
- declare which SASA engines support it and raise a clear capability error for
  engines that do not;
- preserve output units and selection/index mapping;
- consider a reusable MolSysMT-to-Biotite conversion helper if Biotite remains a
  supported backend.

### Expected TopoMT cleanup

Remove the local Biotite construction path once the MolSysMT API supports the
required contract.

## 2. Generic Grid-Volume and Overlap Helpers

### Use case

TopoMT's AlphaSpace2 implementation contains numeric helpers for voxelized grid
volume and group intersection/union matrices. They operate on NumPy arrays and
do not depend on TopoMT semantics.

Candidate shared functions:

- `grid_volume(points, threshold, resolution)`;
- `overlap_matrices(groups, total_size)`.

### Decision question

Confirm whether MolSysMT intends to own generic spatial-analysis primitives and
whether another sibling project has a concrete reuse case. If accepted,
TopoMT should remove its local duplicates after parity tests pass.
