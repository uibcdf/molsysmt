---
summary: Mechanical platform validation rejects documented backend names.
issue: uibcdf/molsysmt#559
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [api, argdigest, convert, deps, diagnostics]
guard: tests/molecular_mechanics/test_platform_contract.py
normative:
blocked_by: []
supersedes: []
---

# Mechanical execution platform contract

## What

On native main `8c266129320799bd4da8802ec27653642f45ba21`, the shared
platform digester admits only CPU/CUDA, while the energy APIs document Reference
and OpenCL. The System-to-Context adapter also resolves only CPU/CUDA strings;
merely broadening the digester would still pass other strings to a constructor
that requires an engine platform object. Simulation construction has a separate
platform lookup and must share the repaired selection semantics.

## How

Linux/Python 3.14.7/OpenMM 8.6.1, bundled Trp-Cage structure 0. The runtime
registry contains Reference, CPU and CUDA. Public CPU energy succeeds at about
-1233.257 kJ/mol; Reference and OpenCL fail with ArgumentError. A top-level
trusted call still encounters a nested public conversion's platform validation.
The separate constructor problem is established by inspecting its two-branch
CPU/CUDA translation, not by claiming that trusted top-level calls reach it.

## Why and intended outcome

Platform choice must reach its owning engine without a consumer bypass or
fallback. Keep the public mechanics vocabulary inclusive of future engines:
general digestion validates a nonempty string, while engine-specific known
names, registered plugins and availability belong in the engine adapter.

Use a shared OpenMM resolver for Context and Simulation construction. Admit
installed plugin names dynamically; retain the known OpenMM platform vocabulary
only for distinguishing an unavailable installation from an unknown name. A
registered platform is not proof that its driver/device can construct a context;
preserve subsequent native execution errors. Dependency absence remains a
separate DepDigest outcome.

## Acceptance and exclusions

- Real Reference Context/Simulation and native energy calculations, preserving
  actual selected platform identity and source input.
- CPU/Reference energy and unit parity with an explicit numerical tolerance.
- Invalid formats, unknown names and known-but-unregistered names have distinct
  appropriate native diagnostics; failed device initialization remains an
  engine execution error rather than a dependency/platform-absence rewrite.
- No GPU hardware or new device/method is required. Use bounded controlled
  registry/failure cases alongside actual installed Reference/CPU routes.
- Existing Context/Simulation inputs keep their platform; the argument selects
  newly constructed contexts and is not an instruction to migrate existing ones.
- Public signatures/defaults, scientific definitions and unit policy remain;
  no new runtime dependency, compiled kernel, H5MSM schema or scientific credit.
- Align docstrings, Foundations, Toolbox, Cookbook and course. Consumer: PR #543
  / uibcdf/molsysviewer#264; the wrapper delegates provider diagnostics.

## Resolution and receiving — 2026-11-05

**Contract-tested / bounded numerical parity.** General platform digestion now
requires a nonempty string, preserving the exact name. It carries no OpenMM
vocabulary or optional-engine import. Shared Context/Simulation construction
resolves names through the OpenMM-owned resolver and actual registry. Installed
plugin names are admitted dynamically. The engine-specific known vocabulary
(Reference, CPU, CUDA, OpenCL, HIP, Metal) classifies absent registrations; it
does not advertise hardware execution or restrict installed external plugins.

Malformed values raise ArgumentError; unknown names raise ArgumentChoiceError;
recognized unregistered names raise the catalog-backed
ExecutionPlatformUnavailableError (MSM-ERR-PLATFORM-001), retaining engine,
requested name, registered names and caller. The exception is imported directly
by internal consumers and is not injected into legacy public module namespaces
through wildcard exports. Actual driver/device/context failures propagate as
engine errors. Missing selected dependencies retain DepDigest diagnostics.
There is no platform substitution after a failed explicit choice.

All public mechanics platform callers were audited: total energy, nonbonded
energy, minimization, and the Context/Simulation adapter chains. Selected OpenMM
execution paths and discovery utilities now have explicit lazy dependency
boundaries. Discovery retains its signatures and legacy output contracts:
verbose=True prints and returns None; verbose=False returns names; loading_failures
prints and returns None. Docstrings now describe those actual outcomes.

Existing Context/Simulation inputs keep their actual platform. The argument
selects new contexts and does not request migration of a supplied one. Native
Context/Simulation objects expose actual platform identity; quantity result
formats are unchanged. Effective-recipe/provenance extension remains the
separate #582 proposal rather than a new output schema in this correction.

### Numerical and contract controls

Actual Reference Context and Simulation construction are checked alongside
native total energy, flat-selection nonbonded energy and independent
minimization. Source coordinates and unit policy remain unchanged. No GPU
execution is required or claimed. Device failure is a controlled constructor
failure on a genuinely registered CPU route; the exact original error survives.
A controlled plugin registry tests name extensibility without claiming a custom
plugin executed science. Actual absent-platform tests prefer OpenCL, selecting
another absent known platform when necessary.

CPU/Reference parity uses bundled alanine dipeptide, structure 0, for vacuum,
OBC1 and OBC2 with the existing physical settings. The threshold is 1e-3 kJ/mol
absolute plus 1e-6 relative, allowing backend precision/reduction rounding in
this small case. The measured absolute differences are respectively
3.038549427003545e-5, 2.5645671669849435e-5 and
2.1368431148971467e-5 kJ/mol. This is neither bitwise equivalence nor a general
GPU/large-system precision claim. Exact selected-platform identity assertions
also protect against a silent backend substitution.

Receiving passes **1,784 affected tests**, **293 published-minimum-support
cases**, **570 documentation/governance/doctest controls** and the executed
four-cell discovery/Reference tutorial. Suites overlap. The focused final
platform contract has 20 cases. Five other edited notebooks preserve all
original executable cells, outputs and metadata. Foundations, Toolbox,
Cookbook, course, engine adapter docs and public docstrings are aligned.

### Corrected development checks and scope

The red guard has three ordinary Reference calls failing at argument digestion.
An intermediate decorator patch initially placed a dependency import too late;
its NameError was caught and the import fixed before the successful receiving.
One broad test command named a nonexistent tests/form/openmm_System directory;
that invalid selection executed no tests and is not passing evidence. The
corrected command is retained in the receipt. Full Ruff checking and formatting
passed; one formatting omission in the preceding resource test was normalized
without changing assertions.

No public signature/default, physical force-field/model definition, unit policy,
compiled kernel, dependency floor, H5MSM schema or new scientific attribution
is introduced. This is execution selection, not a new scientific criterion.
[OpenMM platform properties](https://docs.openmm.org/latest/userguide/library/04_platform_specifics.html)
and its local source informed the engine boundary; the original physical model
and its existing Ackredit construction attribution remain unchanged.

See the [receiving receipt](../../../devtools/data/platform_receiving_559_20261105.json)
for exact commands, source hashes, versions, numerical observations and limits.
Hosted execution, installed/platform artifacts and release qualification remain
separate. The next native reports are #561 and #562, before PR #543 expansion
receiving; no new tag, Release, promotion or full release matrix is launched.
