---
summary: Force-field resource lookups expose mutable registry lists.
issue: uibcdf/molsysmt#560
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [api, deps]
guard: tests/molecular_mechanics/test_get_engine_forcefield.py::test_caller_edits_do_not_change_registry_or_later_results
normative:
blocked_by: []
supersedes: []
---

# Force-field resource result ownership

## What

On source `ea4086c7297a7ecf1757648ebd3c5bd44e440c7f`,
`molecular_mechanics.get_engine_forcefield()` returns the registry's list itself.
Its docstring also incorrectly promises a constructed engine object. The function
is a resource-name lookup, with 71 registered engine/force-field/model entries.

## How

Reproduced on Linux/Python 3.14.7/OpenMM 8.6.1. Repeated AMBER14/TIP3P
lookups return the identical object, also identical to that registry entry.
Appending `task-owned-missing-forcefield.xml` makes an independent public
conversion of bundled Trp-Cage to `openmm.System` fail with a missing-file
`ValueError`. Restoring the list in `finally` restores successful construction
of a 304-particle system. This is matched-model evidence; no incorrect energy
or effect on a different registry entry is claimed.

## Why

Editing a caller's metadata result must not alter independent calculations or
another caller's result. The consumer relationship is PR #543 and
uibcdf/molsysviewer#264. No downstream copy or registry compensation is needed
once native ownership is corrected.

## Intended repair and acceptance

- Return an independent list of immutable resource-name strings on every call,
  including valid trusted delegation. A shallow copy is sufficient for this
  contract; do not deep-copy engine objects or change resource definitions.
- Preserve registry values, ordering and implicit-solvent-before-water-model
  precedence. Retain the current public signature and list return type.
- Apply the normal ArgDigest public boundary and existing SMonitor diagnostics
  for invalid names/combinations. Metadata lookup does not require or prove
  OpenMM/LEaP availability; keep actual engine checks at execution boundaries.
- Exercise all 71 registered entries, caller/registry isolation, real bounded
  public OpenMM construction after local editing, and supported dependency floors.
- Correct the docstring and Foundations/Toolbox/Cookbook/course explanation.
  A returned model label does not certify that the files are installed or that
  the downstream engine has configured the scientific model completely.

## Scope and evidence

This is an output-ownership and metadata-contract correction. No force-field
parameters, registry definitions, energies, dependency floors, compiled kernels,
chemical-state assignments or file-format schemas change. No new scientific
algorithm is implemented, so this patch creates no additional Ackredit event.

## Resolution and receiving — 2026-11-05

**Contract-tested.** Every valid call returns a new list. The entries contain
immutable strings, so a shallow list copy provides complete output isolation;
there is no reason to copy or cache a constructed engine object. The registered
resource file remains byte-identical to the base, SHA-256
`7a3bdfde9f98ade07da681f4ca31e3fafb53ac587502ce4bcd31a4b697feb6ce`.
The signature, successful resource order and model precedence are unchanged.

The previously undecorated public helper now uses ArgDigest and SMonitor's
signal/catalog argument diagnostics. Existing digesters normalize engine/water
names; missing combinations produce native choice diagnostics. The public
skip flag is checked as a literal boolean, also at the older supported
ArgDigest boundary. No engine DepDigest guard is appropriate for this pure
metadata operation; the test models absent engines with the real dependency
checker and fails any attempt to import them. Execution retains its owning
engine dependency boundary.

Receiving passes **984 affected tests**, **169 cases with published minimum
support payloads**, and **569 documentation/governance/doctest controls**.
These suites overlap. The all-entry ownership guard checks original values,
independent lists, caller replacement/appending/clearing, unchanged registry
and fresh lookup, for both normal and valid trusted calls. Real bounded
Trp-Cage parameterization after a caller-local missing XML append retains 304
particles and all reference masses, constraints and individual force payloads.
Force enumeration order is not a physical identity test.

The expanded resource tutorial executes all seven code cells. Foundations,
Toolbox, Cookbook, Module 20, docstrings and the manifest are aligned. The
Cookbook and course edits preserve all existing code, outputs and metadata.
No heavy simulation or network access is needed by the new examples. The
initial notebook execution was sandbox-denied when opening a local Jupyter
socket; the same command succeeded with the authorized execution boundary.

### Corrected test assumptions

The first red ownership run fails the object-alias assertion on the original
implementation (xdist stops at the requested first-failure boundary). An interim
parameterization assertion incorrectly guessed 153 constraints; direct
inspection of the unchanged baseline gives 150. The final guard compares actual
baseline constraint parameters and per-force serialized payloads, rather than
keeping a guessed count or assuming whole-system XML order is deterministic.
All final counts above apply after that correction.

### Separate scientific limitation

AMBER14/OBC1 metadata currently lists only the protein XML. A real conversion
builds no generalized-Born force; this preexisting physical-model contract is
now owned by **uibcdf/molsysmt#580**, with its
[pending record](amber14_obc1_conversion_omits_implicit_solvent_force.md).
This ownership correction does not redefine that model or certify implicit
solvent. It does not require a new scientific Ackredit event; any subsequent
scientific implementation must evaluate its attribution independently.

Commands, file hashes, dependency origins and boundaries are retained in the
[receiving receipt](../../../devtools/data/forcefield_resources_receiving_560_20261105.json).
These are local source results. Hosted, installed/platform and release gates
remain separate; no tag, Release, promotion or extra matrix is launched.
