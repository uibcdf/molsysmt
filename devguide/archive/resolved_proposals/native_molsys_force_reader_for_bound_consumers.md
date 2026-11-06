---
summary: Support native MolSys input in get_forces for primary-bound consumers.
issue: uibcdf/molsysmt#572
status: resolved
opened: 2026-11-05
closed: 2026-11-06
verification: measured
area: [api, molecular_mechanics, molsysviewer]
guard: tests/molecular_mechanics/get_forces/test_native_contract.py
normative:
blocked_by: []
supersedes: []
---

# Native MolSys force reader for primary-bound consumers

## What

Provide a scientific-owner route for molecular_mechanics.get_forces on a native
MolSys, or a supported public replacement with explicit conversion/model rules.
The existing implementation admits only OpenMM Context and Simulation inputs;
the Viewer tools addon binds the current native MolSys. This is a capability
request, not evidence that the existing OpenMM force numbers are incorrect.

## Reproduction

On published native basis 532d036228c9673c5ddd63beaa8093220b06b6b2 and contribution
04b9fbbda4654516c01d6c34e9c19ad17c1be0fb, Linux/Python 3.14.7 with OpenMM present:

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems["Trp-Cage"]["1l2y.h5msm"],
    to_form="molsysmt.MolSys",
    structure_indices=[0],
)
msm.molecular_mechanics.get_forces(molsys)
# NotImplementedError (empty message)
msm.molecular_mechanics.get_forces(molsys, skip_digestion=True)
# NotImplementedError (empty message)
```

Both calls are independently reproduced without importing Viewer. The legacy
H5MSM warnings are retained; the failure occurs in the explicit unsupported-form
branch, before molecular parameterization. A first draft probe used a nonexistent
pentalanine.pdb catalog key and was discarded; the final issue uses the actual
bundled Trp-Cage file above.

The positive control constructs a two-particle OpenMM System with one harmonic
bond, k=100 kJ/(mol nm²), equilibrium length 0.1 nm and actual separation 0.2 nm.
An explicit CPU Context with one thread returns the analytical [+10,0,0] and
[-10,0,0] kJ/(mol nm) forces through the native reader. Engine absence and an
incorrect existing Context result are thus refuted for this bounded control.

## Why

uibcdf/molsysviewer#264 and #421/#543 require expert mirrors to consume the
current view.molsys and delegate scientific work to MolSysMT. An always-rejected
bound method adds no useful capability; implicit consumer-side context creation
would also introduce scientific model/preparation decisions outside its owner.
The addon therefore keeps get_forces unexposed and continues other mechanical
queries without changing its denominator or claiming a complete force surface.

## Acceptance

Define which structures are read and whether selection returns forces in the
complete parameterized environment or in a rebuilt subsystem. Specify magnitude,
output axes/units, supported element levels, stored/default mechanics, periodic
conditions, explicit engine behavior and unsupported-form diagnostics. Preserve
source/engine ownership and avoid hidden preparation or fallback.

Protect native MolSys plus Context/Simulation routes with pytest cases for
selection forms and order, magnitude, units under a non-default policy, unsupported
inputs and scientific source preservation. Compare with analytical forces or an
independent energy-gradient oracle. The scientific owner chooses and implements
the contract; this consumer report does not authorize native changes or publication.

## Prepared implementation — 2026-11-06

**Implemented; contract-tested; bounded parity and numerical checks passed.**
The maintainer's ordered objective now includes #572. Prepared owner code is
`993967a0f361d70cba5f7e5c7c246b0000734550`. Its provider source
accepts native MolSys and supported coordinate/model compositions as well as
existing Context/Simulation inputs. It does not change the Viewer runtime.

### Public contract

- Preserve every prior positional parameter and default. Add keyword-only
  `structure_indices=None` and `platform='CPU'`. None preserves the legacy
  `(n_atoms, 3)` vector or `(n_atoms,)` magnitude result for the first stored
  structure/current engine state. Explicit indices, including one index and
  `'all'`, retain a leading structure axis. Order and repetitions are retained.
- Select atoms **after** complete-model force evaluation. Queries, explicit
  ordered/repeated indices and full Boolean masks filter the output; they never
  remove the environment. This differs deliberately from subsystem energy
  parameterization. Only `element='atom'` is supported; unsupported aggregation
  fails explicitly. Empty axes have defined shapes and force units without
  model construction/evaluation.
- Use OpenMM's raw negative potential gradient, not constraint reactions or
  accelerations. Existing Context/Simulation inputs preserve positions,
  velocities, time, System, integrator and platform. A native read constructs
  one complete context with supported stored requests before configured
  defaults. It never repairs chemistry, adds hydrogens, minimizes or integrates.
- Keep physical units at the engine boundary explicit, then standardize the
  result with the application's PyUnitWizard policy. Periodic models receive
  each structure's row-vector box. Parameterization from native chemistry requires a known
  reference-state association for every requested structure; no implicit state
  switch is performed.
- Refuse unsupported stored construction overrides instead of discarding them.
  Supply a preparameterized Context/Simulation or an aligned System/coordinate
  composition for custom models. A structures-only H5MSM 0.5 plus a supplied
  System does not require invented topology or chemical-state data. That supplied
  System is authoritative for the potential; its fixed default periodic box is
  used when structural data has no boxes. The supplied axes must correspond.
- Apply ArgDigest at the public boundary, conditional DepDigest for OpenMM,
  catalogued SMonitor diagnostics, and optional Ackredit credit for the actual
  executed engine version. No dependency floor or environment is changed.

### Reusable ownership and two shared option defects

The public mechanics function delegates numeric iteration to a private reducer
and the existing ChunkedExecutor. Native coordinate sources read their existing
structures; modular H5MSM projects chemistry or stable query context and one
model structure before streaming. Named interaction analyses are not loaded.
Complete model/axis compatibility stays explicit.

The shared `openmm.Topology -> openmm.System` adapter previously ignored
`switch_distance` and treated explicit `dispersion_correction=False` as an absent
request. A ten-case regression selection recorded nine failures and one pass.
Its initial rejection expectation for zero switching length was corrected
against OpenMM's source; the retained positive control now requires that an
explicit zero actually enable switching. The initial failure total is not a
count of independently established defects.
The repair lives in that existing general converter, not in the force reader:
apply the actual Boolean, enable switching at a scalar finite length satisfying
`0 <= distance < cutoff`, reject NoCutoff/LJPME switching, and apply an explicitly
validated positive finite Ewald tolerance. The zero lower bound follows OpenMM's
own NonbondedForce implementation; it is not a newly invented physical rule.
Invalid shape/value and incompatible-method controls protect the correction.

### Evidence and limits

The [receiving receipt](../../../devtools/data/native_force_reader_receiving_572_20261106.json)
retains final source-file digests, test counts, provider origins and failed-probe
dispositions. The direct checks cover literal two-particle harmonic forces,
an independently constructed alanine model and central energy difference,
nonconsecutive/repeated axes, magnitude/masks/empties, nm/pm and alternate force
units, one complete context with bounded read-only blocks, changing orthogonal/
triclinic boxes, H5MSM/full-reader exclusion, a structures-only H5MSM with an
explicit System, dependency/attribution behavior, and source preservation on
success and nonfinite-coordinate failure.

The new literal harmonic cases under `tests/scientific_truth/molecular_mechanics`
are additional explicitly executed numerical controls. The pre-existing 83-case
registered release certificate on frozen #304 source is unchanged; its receipt
does not certify this newer force implementation. The force API retains its
existing outside-contract stability classification. These bounded tests do not
certify arbitrary chemistry, force fields, GPU/device execution or all periodic
cells. PME comparisons match the first requested box used to initialize the
context; they do not assume an identical FFT grid after arbitrary reinitialization.

Output remains resident. The numerical estimate in [SCALABILITY](../../SCALABILITY.md)
is not a process-RSS or engine-allocation bound. There is no force-output writer,
checkpoint/resume protocol or broad performance superiority claim.

### Remaining ordered integration

The source remains prepared on the dedicated ordered-work branch until #304 and
the preceding issues finish their gates and integration. Do not close #572 out
of order or treat focused checks as exact-candidate release evidence. The User
Guide tutorial, Foundations, Cookbook and course distinguish the native provider
route from the addon method that remains unexposed. Viewer owner receiving and
clean installed qualification remain separate handoffs; no placeholder addon,
release, tag, package promotion or sibling code edit is authorized by this work.

## Resolution — 2026-11-06

The provider-owned native MolSys force contract is implemented and integrated
on main. Its documented complete-environment semantics, structure/atom selection,
magnitudes, supported element scope, units, stored model and PBC settings,
ownership and explicit refusal paths satisfy the original request. Analytical
and independent gradient/Context comparisons, Simulation reuse and non-default
unit controls remain in the native-contract guard; the earlier 2,005 affected
cases, provider-floor and documentation results remain scoped evidence above.
The final joint source selection reruns this guard against integrated code.

No hidden preparation, subsystem model substitution or arbitrary engine fallback
is introduced. The source-ready native capability closes this provider issue;
adding its bound facade and receiving it in a real Viewer remains consumer work
under #421 / uibcdf/molsysviewer#264. Final installed release-pair/platform gates
and scientific expansion remain independent. No release or publication follows.
