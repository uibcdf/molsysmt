---
summary: Nonbonded energy overwrites the first partition when the second selection is flat.
issue: uibcdf/molsysmt#561
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [api, diagnostics, selection, tests, units]
guard: tests/molecular_mechanics/get_non_bonded_potential_energy/test_get_non_bonded_potential_energy.py
normative:
blocked_by: []
supersedes: []
---

# Nonbonded partition selection contract

## What

At main 50854766d86817bba352c8c843931237595cf134, nested/flat
nonbonded selections fail because the second-axis normalization overwrites the
first axis. An ordinary public Reference call reproduces the reported TypeError;
no consumer wrapper or digestion bypass is involved.

The inverse map also keeps only one partition per atom, so it cannot correctly
account for repeated or overlapping partitions within an axis. The engine's
System is modified during evaluation, including when supplied by a caller's
Context. Empty lists are incorrectly classified as nested by a general helper's
vacuous all() result. These observations require scoped numerical and ownership
controls alongside the one-line assignment repair.

## How

Linux/Python 3.14.7/OpenMM 8.6.1, bundled alanine dipeptide, structure 0.
The red ordinary-public mixed-partition guard fails with TypeError at the first
inverse-map loop (1 failed, exit 1, 4.16 s). Rows are [3,4,5] and [0,1,2];
the second axis is [10,11,12].

## Why and intended contract

- Flat/flat returns one energy; if either axis is partitioned, return an energy
  matrix with rows in selection order and columns in selection_2 order.
- Resolve indices using the existing public selector. Validate once after
  resolution, before constructing or changing an engine model.
- Deduplicate indices inside a set without changing caller data. Preserve
  repeated partitions and support shared members within one axis.
- Reject shared atoms between axes: the existing E(A union B)-E(A)-E(B)
  decomposition requires disjoint A and B. Do not invent an overlap definition.
- Empty sets give typed zero entries; [] is a flat empty set, while [[], []]
  explicitly requests two partitions. Internal energy without selection_2
  accepts one flat selection; reject an otherwise ambiguous partition request.
- Reuse the public System copy tool for a temporary engine model. Preserve
  caller parameters, force groups, coordinates, actual platform and unit policy.

## Acceptance and limits

Compare every matrix entry to an independent scalar call for four nesting
combinations, unequal counts, single partitions, selection strings and supported
numeric syntax routes. Cover empty, repeated, overlapping and invalid inputs,
noncanonical unit policy, source preservation and actual CPU/Reference execution.
Keep the existing optimized partition evaluator; extend its inverse map to all
memberships rather than replacing it with a Python call per matrix cell.

These are bounded NoCutoff parity controls, not new scientific validation of
periodic electrostatics, arbitrary custom force models, binding free energies or
whole-trajectory evaluation. The current API evaluates the constructed/retained
engine context, without a new structure-axis argument. No new public signature,
dependency floor, compiled primitive, physical model or attribution criterion.

Consumer: PR #543 / uibcdf/molsysviewer#264. Keep the addon a native wrapper.

## Resolution and receiving — 2026-11-05

**Contract-tested / bounded engine parity.** The two inputs are normalized
independently after public selector resolution. Flat sets remain flat for scalar
output; either explicit partition axis retains a matrix dimension. Empty [] is
one flat set, and explicit empty partitions retain their positions. Index
repetition within a set is removed without editing input. The inverse maps now
retain every partition membership, preserving repeated/overlapping partitions
within either axis and the original exception order in each calculation.

Shared atoms between axes and partitioned internal-energy requests without a
second selection receive native conflict diagnostics. This does not introduce a
new physical definition for overlapping interaction sets. One standard OpenMM
NonbondedForce is required and identified by class, independently of its name.
Missing/multiple standard forces are rejected explicitly. Other force groups
are separated in the temporary copy so they cannot contaminate the requested
standard-force energy. OpenMM-specific handling stays within the selected
engine branch; no engine class enters native stored mechanics data.

System cloning reuses the public copy tool rather than introducing a second
copy implementation. It prevents edits to supplied Context/Simulation source
parameters and force groups. The current source-context cell is set in the
copied System before constructing its temporary context. A two-particle
CutoffPeriodic control distinguishes a 3 nm current cell from 2 nm stored
defaults: its 1.3 nm separation is outside the 1 nm cutoff, while the incorrect
stored cell would wrap it to 0.7 nm. This verifies current-box preservation,
not every periodic-electrostatics decomposition.

The existing optimized partition evaluation remains: one temporary engine model
per call, shared single-set evaluations and matrix pair evaluations. There is no
new public call/context per matrix cell. Inverse-map storage follows actual
partition memberships; the requested matrix remains dense. The extra System
copy scales with that engine model, not the coordinate history. No speed/RAM
benchmark or new compiled implementation is claimed.

### Diagnostics and corrected controls

The native SMonitor catalog now exposes an argument conflict's supplied reason
to users, QA and agents, instead of suggesting that the two energy axes are
always mutually exclusive. The existing unsupported-method template names the
requested method. Codes/classes and runtime floors are unchanged. Guards check
these concrete explanations and preserve standard selection diagnostics.

Two initial test assumptions were corrected rather than changing runtime units
or numbers to satisfy them. An empty row/column does not imply that every other
matrix entry is zero; nonempty entries are compared to their scalar calls.
PyUnitWizard's loaded_libraries is lazy-backend inventory, not user policy, so
policy controls exclude only that field while checking every remaining policy
field and the actual noncanonical energy unit. This also repairs an order
sensitivity in the preceding platform guard. The initial broad run had one
such assertion failure (1 failed, 1,816 passed); the final full affected run
passes after this test correction.

### Final evidence and documentation

- **1,818 affected tests**, exit 0, 130.15 s.
- **326 published-support-floor cases**, exit 0, 20.39 s; runtime SMonitor remains
  active while its unrelated editable pytest entry point is excluded under #524.
- **569 documentation/governance/doctest cases**, exit 0, 21.31 s; the final
  function doctest is also rerun (1 passed, exit 0, 3.92 s).
- The eight-cell nonbonded tutorial executes on the final source (14.2 s), with
  a 3-by-3 matrix and its equivalent 3-by-1 mixed call. The original complex,
  pair-energy, matrix, marginal-sum and visualization concepts are retained.
  The example deliberately uses three groups per protein; full lists remain
  an explicit larger request. The pre-generated full-analysis visualization
  is distinguished from that bounded numerical subset.

Suites overlap. The 36-case function module covers all four nesting combinations,
unequal/singleton counts, numeric MolSysMT/MDTraj syntax routes, MolSysMT
partition strings, repeats/within-axis overlaps, typed empty entries, invalid
indices/deep nesting, across-axis conflict, internal energy, custom force-group
isolation, unsupported force counts, source ownership and current-box retention.
Reference matrix entries match independent scalar calls at absolute 1e-8 kJ/mol
plus relative 1e-10; CPU group-string parity uses 1e-5 plus 1e-6. Actual energy
units are checked under an angstrom/kcal session policy.

Docstrings, Foundations, Toolbox, Cookbook and the two course modules that use
this function now explain shape, units, ownership and model meaning. The course
clarifies that one interaction energy does not establish binding free energy or
physical stability. All executable cells, outputs and metadata of those two
course pages and the Cookbook are unchanged. Their complete network/preparation
scenarios remain unqualified here, including ligand placement/parameterization.

No public signature/default, dependency floor, H5MSM schema or compiled kernel
changes. No new scientific criterion or Ackredit event is introduced; this
repairs the existing decomposition rather than proposing a new method. Optional
execution dependency boundaries and units still use DepDigest/PyUnitWizard,
public inputs use ArgDigest and structured diagnostics use SMonitor.
[The receipt](../../../devtools/data/nonbonded_partitions_receiving_561_20261105.json)
retains exact commands, hashes, observed versions and limits. Hosted, installed
and release qualification remain separate. Next: #562, then the newly reported
#583/#584 and PR #543 expansion receiving, without a new tag or release here.
