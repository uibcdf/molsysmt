---
summary: AMBER14 OBC1 conversion builds no implicit-solvent force.
issue: uibcdf/molsysmt#580
status: open
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [api, convert]
guard:
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
