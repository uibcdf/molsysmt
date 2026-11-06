---
summary: AMBER14 OBC1 conversion builds no implicit-solvent force.
issue: uibcdf/molsysmt#580
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [api, convert]
guard: tests/form/openmm_Topology/test_implicit_solvent.py
normative:
blocked_by: []
supersedes: []
---

# AMBER14 OBC1 conversion omits implicit-solvent force

## What

The public conversion to `openmm.System` accepts AMBER14 with
`implicit_solvent='OBC1'` but constructs no generalized-Born solvent force.
The registered resource list is `['amber14-all.xml']`, identical to the vacuum
resource list. This preexisting definition is unchanged by #560's independent
list-return correction.

## How

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], structure_indices=0)
system = msm.convert(molsys, to_form='openmm.System', forcefield='AMBER14',
                     implicit_solvent='OBC1')
print([force.__class__.__name__ for force in system.getForces()])
```

Observed force types, disregarding their order: HarmonicBondForce,
HarmonicAngleForce, PeriodicTorsionForce, NonbondedForce and CMMotionRemover.
No GBSAOBCForce or CustomGBForce is present. Construction succeeds with 304
particles. The current metadata tutorial previously described solvent labels
as automatically including complementary parameters; #560 corrects that claim
and explicitly distinguishes resource lookup from physical configuration.

## Why

A silently admitted physical model can mislead energy or simulation consumers.
No production energy discrepancy is measured here and no impact on explicit
water parameterization is alleged. Review actual engine construction rather
than treating a model name or nonempty metadata list as sufficient evidence.
Related consumer scope: #421 / PR #543 and uibcdf/molsysviewer#264.

## Refuted and unassessed claims

- The initial issue scaffold said the two systems match vacuum. Resource names
  do match; raw complete XML serializations need not: OpenMM force enumeration
  can differ. This report therefore makes no byte-identity assertion.
- No energy, force or dynamical solvent-response comparison has yet run.
- Whether OBC1 labels on other AMBER and LEaP entries select the intended variant
  remains unassessed, not implicitly certified by their resource names.

## Acceptance

1. Determine supported force-field/implicit-solvent combinations from engine
   documentation/source and scientific references, with Ackredit attribution
   where a scientific implementation is adopted.
2. Either construct the explicitly requested model correctly or reject an
   unsupported combination before returning a misleading system. Do not
   silently choose vacuum, a different OBC variant or another force field.
3. Add bounded real-engine controls verifying the actual solvent force and
   independently justified response/parameters, plus unsupported combinations,
   units, public conversion and source preservation. A returned filename alone
   is not the scientific guard.
4. Align model metadata, docstrings, User Guide and course; communicate the
   supported execution contract to the Viewer mechanics consumer. Treat #560's
   output-ownership guarantee as independent and preserve it.

## Provenance

2026-11-05, Linux, Python 3.14.7, OpenMM 8.6.1. Source base
`ea4086c7297a7ecf1757648ebd3c5bd44e440c7f` with the #560 working patch;
`molsysmt/molecular_mechanics/forcefields.py` and OpenMM converter bodies are
unchanged from that base. This is **Reproduced** behavior and an open scientific
contract review, not a newly qualified method or an automatic release deferral.

## Source review — 2026-11-05

OpenMM checkout `ba0aa236ac4d07241382869604c4d2ea58c4f3f5` and installed
8.6.1 both provide `implicit/obc1.xml`. The official
[implicit-solvent guide](https://docs.openmm.org/latest/userguide/application/02_running_sims.html#implicit-solvent)
identifies OBC I as Amber igb=2 and OBC II as igb=5. The OBC1 XML delegates to
GBSAOBC1Force; old *_obc.xml files instantiate GBSAOBCForce, whose Reference
kernel explicitly uses ObcTypeII. A real seven-entry audit finds no solvent
force for AMBER14 and the OBC II class for all six legacy AMBER entries.

The intended correction selects the explicit OBC1 XML for the seven already
registered OpenMM AMBER fields. Preserve supported explicit-water/vacuum paths,
solvent argument precedence and the independent-list guarantee. LEaP entries
remain topology-preparation metadata, not promises to set a later igb option.
Do not introduce unreviewed new model names or CHARMM solvent combinations.

OBC1 construction must use a permitted nonbonded method. The official XML admits
NoCutoff, CutoffNonPeriodic and CutoffPeriodic and rejects Ewald/PME/LJPME.
The missing default for a direct OpenMM topology must choose NoCutoff even if
box metadata exists. Explicit incompatible methods need a native diagnostic.

Scientific method citation: Onufriev, Bashford and Case (2004), DOI
10.1002/prot.20033. The method will be executed by OpenMM's shipped XML, not a
new MolSysMT reimplementation. Credit successful construction through the
existing optional Ackredit adapter; metadata lookup and refused construction
must not credit a completed scientific method.

## Resolution and bounded verification — 2026-11-05

The maintainer refined the plan to make OBC1 and OBC2 explicit physical choices
and keep the mechanics API inclusive of other engines. Both variants are now
registered for the seven existing OpenMM AMBER fields. Each engine adapter
owns resource and constraint translations; no OpenMM object or XML is stored
as native mechanics state. No additional CHARMM/LEaP calculation is claimed.
LEaP retains its preparation-resource metadata. The unused legacy private
registry now shares the public table instead of carrying a competing copy.

The shared conversion boundary resolves supported declared mechanical options
in this order: explicit keyword (including None), stored source setting,
library default. Newly read stored settings are validated at the adapter
boundary; source objects are not edited. The public signature is unchanged.
An implicit-model request selects no cutoff by default even with a box;
unsupported OBC PME/Ewald/LJPME choices raise native diagnostics.

Construction faithfully delegates to OpenMM's shipped model XML and its
standard mbondi2/ACE, dielectric 1/78.5, zero-screening recipe. OBC1 and OBC2
are different variants, not software names. The Onufriev/Bashford/Case paper
and executed engine/version are credited through optional Ackredit only after
successful construction, with contextual model/field/resources. Metadata-only
lookup, rejected construction and reading serialized OpenMM data create no
successful method credit. Absence and provider failure preserve the completed
model, with native tracking diagnostics for failure. Applications own sessions.
OpenMM XML does not carry the separate Ackredit bibliography.

**Contract-tested / parity-tested, plus a bounded frozen-reference check:**

- All fourteen field/model combinations construct the selected GB variant.
  Variant-defining terms distinguish OBC I/II even though both use CustomGBForce.
- The actual public AMBER96/OBC1 unconstrained cutoff conversion matches the
  22-atom upstream force fixture with its original vector thresholds: absolute
  0.1 kJ/mol/nm or relative 1e-4 per atom. Observed maximum absolute difference
  is **0.024868854336030335 kJ/mol/nm**. These tolerances were not relaxed.
- The fixture is pinned to OpenMM ba0aa236..., with original coordinates,
  original source hashes and upstream MIT notice. Its test comment identifies
  AmberPrmtopFile as the comparison route; no new independent Amber executable
  run or complete historical generation metadata is claimed.
- Direct standard-XML Reference-platform energies and forces agree with both
  public variants (energy abs 1e-8 kJ/mol; forces rtol 1e-10, atol 1e-8
  kJ/mol/nm). In the same fixed unconstrained 22-atom NoCutoff AMBER14 fixture,
  energies are vacuum -55.76095949667376, OBC1 -106.7017213530296 and OBC2
  -105.16810801824288 kJ/mol. The OBC2-minus-OBC1 difference is
  1.5336133347867218 kJ/mol. These are model potential energies, not measured
  solvation/binding free energies or a general model-accuracy benchmark.
- Stored choices, explicit None/other-model overrides, invalid stored values,
  box/default behavior, units and optional real Ackredit capture are covered.

Receiving passes **1,817 affected tests**, **234 published-support-floor
controls** and **570 documentation/governance/doctest controls**. Suites overlap.
The ten-cell tutorial executes. Cookbook and course changes retain all original
executable cells, outputs and notebook metadata. Public docstrings, Foundations,
native mechanics documentation, Toolbox and course are aligned. No new runtime
dependency, compiled kernel, native chemistry store or H5MSM version is required.

### Corrections and remaining limits

The initial implementation tried to import a non-exported attribute-list name;
that import failed its first receiving and was replaced with the existing
public attribute catalog. The first reference run also used the existing
hard-coded HBonds construction; this differed from the unconstrained upstream
recipe. #581 corrects the constraint translation, with actual pair/distance
controls. The final frozen-reference test uses explicit None and the original
upstream tolerance. An overlapping diagnostic process saw repaired constraint
counts, not a separately measured red baseline.

Independent dielectric/screening/cutoff tuning is not yet exposed by these
conversion signatures. The native container's broader field vocabulary does
not certify execution of arbitrary stored controls. This is explicitly
documented and the engine-neutral effective-recipe/capability design is owned
by **uibcdf/molsysmt#582**; no automatic new initial-1.0 gate or release deferral
is inferred. Generic dynamics, broad chemistry coverage, other engines and
experimental mechanics persistence remain outside this bounded correction.

The [receiving receipt](../../../devtools/data/implicit_solvent_receiving_580_581_20261105.json)
retains commands, versions, source hashes and outcomes. These are local source
results; exact hosted, installed/platform and release qualification are separate.
