---
summary: OpenMM solvate silently ignores explicit ion counts.
issue: uibcdf/molsysmt#575
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [build, units, tests]
guard: tests/build/solvate/test_explicit_ion_counts.py::test_openmm_applies_explicit_ion_counts
normative:
blocked_by: []
supersedes: []
---

# OpenMM solvate silently ignores explicit ion counts

## What

On main `8486ea59cdca48de30abf3e66484c11fd843da59`, the issue's
`AlaValPro` reproduction completes successfully with zero ions after requesting
two sodium and two chloride ions at zero salt concentration. The source has 43
atoms and remains unchanged; the returned system has 208 atoms. Python 3.14.7,
OpenMM 8.6.1, NumPy 2.4.6. The process exits zero. This independently reproduces
the incoming report rather than inferring it from the consumer's test.

## How

All three OpenMM solvent-construction branches omit the two count arguments.
The native branch has a water-replacement algorithm, but its random placement
has no public seed and its distance checks do not use periodic images.

## Why

A successful preparation can silently return a composition different from the
explicit request. MolSysViewer delegates preparation to this public API.

## Accepted implementation scope

Diego approved a reusable `build.add_ions` operation and its use by the OpenMM
solvation route. Separate count resolution, charge evidence and geometric
placement. Replace complete water molecules, use shared periodic neighbor
primitives, expose a reproducible seed and bounded attempts, preserve the source,
and retain operation-scoped atom maps and attribution. Start with one structure,
one chemical state and the existing nine monovalent species. No force-field
parameters or partial charges are invented for new ions.

Explicit counts mean added populations, not desired final populations. A mixed
explicit/neutralizing request must actually permit neutralization. Salt pairs
are additional to that base population, using the explicitly documented
water-count concentration convention. Charge-dependent requests must identify
their charge source; a pH-7 group reference is not an implicit system charge.

OpenMM can construct water with `neutralize=False` and zero ionic strength,
then delegate ion placement. PDBFixer's public route lacks that control: its
unsupported explicit counts must be rejected before construction rather than
silently ignored. Preserve its ordinary supported default route.

## References and limitations

Audited OpenMM source: `ba0aa236ac4d07241382869604c4d2ea58c4f3f5`,
`wrappers/python/openmm/app/modeller.py`, `_addIons`. PDBFixer source:
`5e658a4fb8d2b90d65ca8408c845cbf104ce7099`, public `addSolvent` delegates to
OpenMM. Native placement is inspired by random whole-water replacement; it is
not a faithful reproduction of every provider criterion and does not equilibrate
the system. Credit methodological inspiration separately from executed software.

## Acceptance criteria

- Exact zero/positive counts and supported mixtures; invalid values rejected.
- Charge-dependent requests with neutral, positive and negative totals; unknown
  charge rejected and no implicit tabulated chemical assignment.
- Whole-water removal, valid old/new atom maps, source independence and explicit
  named-interaction treatment.
- Seed reproducibility, bounded failure, periodic distances and equivalent units.
- Actual OpenMM solvent construction honors explicit counts; ordinary supported
  neutralization and concentration retain their declared behavior.
- Public validation, optional dependencies, diagnostics, attribution, User Guide,
  Cookbook, Foundations and course reflect the bounded contract.

## Evidence status

The fix is **Implemented** and **Contract-tested**. Equivalent length units and
native/MDTraj inputs have **Parity-tested** fixtures. Integer charge balance and
minimum periodic exclusion distances have **Scientifically validated** finite
analytical fixtures in the governed Scientific Truth suite. This does not
validate equilibrium, force-field quality, final ionic strength or optimal
packing. No placement benchmark is claimed.

## Resolution

`build.add_ions` now owns monovalent random whole-water replacement. It uses
existing Rust-backed sparse neighbor queries, including periodic images, and
native removal/addition policies. No dense water-pair distance matrix, new
dependency, file-format version or compiled kernel was introduced. Supported
species have known formal charges; partial charges/force-field parameters are
not fabricated. Complete known charged waters and cross-molecule covalent water
bonds fail before editing. Named analyses are remapped and conservatively
invalidated after actual atom changes; independent zero-addition copies retain
coverage.

Native `solvate` delegates its old placement block to this operation, with its
legacy original-solute pH-7 charge approximation explicitly recorded. OpenMM
explicit counts or a seed select water-only provider construction followed by
native replacement; mixed neutralization uses the original OpenMM force-field
charge. Unseeded default OpenMM neutralization/concentration retains the provider
algorithm. PDBFixer rejects explicit counts (including zero) or a seed before
solvent construction; its ordinary default route remains exercised.

The detached `molsysmt.ion_replacement@1` report retains method, parameters, seed,
actual counts, charge origin, producer versions, typed source/output atom maps
and bibliography. `basic.compose_atom_maps` accepts it directly. ChemicalStates
preparation history persists it through H5MSM 0.5 with the original operation's
axes. This does not introduce MolecularMechanics persistence. Ackredit credits
the pinned OpenMM source as methodological inspiration and actual OpenMM use
separately from native execution. Canonical software records prevent conflicts
when reused in a session with other MolSysMT scientific tools.

The guard inspects the actual ion species/populations returned by the public
OpenMM route for 0/0, 2/2, 1/0 and 0/1 requests, and checks source coordinates.
It fails if count arguments are merely forwarded or silently ignored. Additional
guards independently parameterize charged returned systems and sum their charge,
enumerate lattice images, replace four-site waters completely and test report
round trips, unit policy, source independence and bounded rejection.

## Receiving checks — 2026-11-05

- **212 passed**: ion addition, all solvation tests, water boxes, density queries,
  atom-map composition, named-analysis/H5MSM workflow, analytic ion truth and
  Ackredit diagnostics; Pytest Receptor 1.2.1, four workers.
- **77 passed**: published ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0
  and Ackredit 0.9.0 payloads; two workers. Only the known editable pytest-entry
  point is disabled (`-p no:smonitor`, #524), not runtime diagnostics.
- **156 passed**: native copies, independent chemical union, atom addition,
  structural-observation policy, analysis coupling and preparation history.
- **601 passed**: notebook schema/headings, public API docs, course, stability,
  scientific-evidence and docstring guards. Native doctests: **2 passed**.
- New tutorial: all five code cells executed. New course cell and cookbook cell
  executed with their prerequisites. Every pre-existing cell/output/metadata in
  those two lessons is preserved; the solvation tutorial changes prose only.
- Ruff, dependency scan/contract audit, API/stability, Scientific Truth registry,
  course and developer-guide validators pass. The routine hosted smoke for the
  prior `8486ea59c` checkpoint passes (run 42118274443); the new delivery still
  needs its own hosted inspection and is not release-candidate qualification.

The [machine-readable receipt](../../../devtools/data/ion_replacement_receiving_575_20261105.json)
records commands, versions, source hashes and limitations. Counts above are
separate, overlapping suites, not a claim of unique aggregate coverage.

## Findings corrected during implementation

An initial small-box fixture supplied a rank-2 box to a rank-3 native setter;
the fixture was corrected. Another fixture attempted to mutate the read-only
analysis mapping; it now uses its public setter. Native partial charges are
numeric canonical-e storage, not quantities: the reader now honors that owner
contract. The initial attribution used a conflicting short software title;
canonical shared citation records resolve it. A new test also found that
concentration digestion unnecessarily required an application concentration
standard. These two preparation boundaries now validate dimensions and convert
explicitly to molar without changing the caller's presentation policy.

## Remaining independent work

OpenMM label handling #574 is unchanged. PR #543 advanced to
`c0149a2d6147380046768b9211cf11b7b63ebeda` during this receiving; it must consume
the new native main and replace its limitation expectation with actual count
checks. New #578 reports an independent empty-view default defect; #576 and #572
remain capability proposals. No new detector, general protonation algorithm,
equilibration protocol, release/tag or package promotion is part of this fix.
