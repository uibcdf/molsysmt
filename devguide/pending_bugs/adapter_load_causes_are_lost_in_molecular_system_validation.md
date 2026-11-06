---
summary: Preserve operational adapter-load causes instead of rejecting valid molecular-system inputs.
issue: uibcdf/molsysmt#601
status: active
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [basic, form, argdigest, diagnostics]
guard: tests/_private/test_adapter_load_diagnostics.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Adapter-load causes and molecular-system validation

## What

PeptideMT reports that a restricted cold CIF adapter load raises an operational
RuntimeError, but public form recognition shows KeyError and conversion finally
blames the molecular_system argument. A valid source cannot be declared invalid
because its adapter/environment could not be inspected. Keep unsupported input,
invalid complementary axes and unverified execution as distinct evidence.

## How

Consumer uibcdf/peptidemt#33 records a blocked h5py host query (uname -p) on
provider ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6. Its unchanged source succeeds
under the consumer's declared startup sequence. This does not request a parser,
scientific protocol, unrestricted subprocess policy or external h5py issue.

Owner inspection after the #600 local source shows that published DepDigest
0.15.1 already retains the original adapter-load exception as KeyError.__cause__
and exposes explicit retry. MolSysMT's assessment broadly turns discovery errors
into unsupported/invalid strings; validation then discards the exception. The
item digester also broadly catches discovery errors. No provider patch or newer
dependency floor is needed to preserve the already available evidence.

## Planned correction and verification

- Keep DepDigest as declaration, visibility, lazy-loading, cache, retry and
  concurrency owner. A private host registry adapter translates only failed
  known-entry loads with an original cause into the existing public
  MolecularSystemVerificationError, preserving the complete Python cause chain.
  Absent/hidden keys retain ordinary mapping behavior.
- Form recognition must preserve operational detector failures as verification
  errors. Assessment retains an explicit undetermined/unverified classification,
  original exception and recognized-form evidence, rather than declaring invalid
  input. Complementary axis/getter failures also retain their original cause.
- Public argument validation chains the verification error to that evidence.
  Genuinely unsupported inputs retain ArgumentError with reason/cause context;
  real incompatible axes retain StructuralInconsistencyError. Item validation
  must not swallow operational errors. An allowed None append target needs no
  form-detection probe.
- Reproduce with the real published registry contract and a bounded cold child
  that blocks one adapter import with the consumer's operational failure marker.
  Verify direct get_form, convert and module lookup, cached failures, explicit
  retry, successful unchanged-source conversion after recovery, structured
  diagnostics, and original input bytes. Add focused assessment/item controls
  and run existing classification, form discovery, argument, conversion and
  #600 model-label guards at a meaningful checkpoint.
- Document the public failure distinction and original-cause inspection in
  docstrings, User Guide/Cookbook/course and native/form guidance. Keep all
  scientific methods, units, source payloads, optional-dependency policy,
  application diagnostics and release authorities unchanged.

## Why

An operational failure is evidence that validation could not finish, not proof
that an input is malformed. Correct classification lets clients repair their
environment or follow their declared startup procedure without a parser fallback
or bypassed validation. The correction belongs at MolSysMT's consumer boundary;
DepDigest's original-cause and retry contract already supplies the needed tools.

## Work order

This is the final item of the maintainer's fifteen-issue goal, following the
completed local #600 source. Publication is batched for #600/#601 and board
closure remains ordered. Main 40bb54d05 already delivers closed #599. No tag,
Release, registry upload, environment installation or provider code edit is
authorized by this diagnostic correction.

## Verified implementation — 2026-11-06

The private host registry adapter delegates all loading/cache/retry semantics to
DepDigest and retains the provider KeyError and original operational exception.
The existing MSM-ERR-SYS-004 diagnostic now displays the reason in the user
profile. Assessment stores exception evidence without comparing or rendering the
exception object as a dataclass field. Regular argument digestion probes once.
Allowed empty and recognized cross-form append targets retain their contract.

The initial seven reproductions all fail before correction and pass after it.
An additional positive append-target guard is included in the current eight-case
module. The integrated boundary/ArgDigest/registry profile passes 774 cases.
Published provider-floor receiving passes 68 cases with ArgDigest 0.14.0,
DepDigest 0.15.1, SMonitor 0.16.0, Ackredit 0.9.0 and PyUnitWizard 0.28.1. Their
import paths and metadata are independently checked; only the incompatible
source-development SMonitor pytest plugin is disabled in this floor profile.
Runtime diagnostics remain active. No provider/environment installation changes.

The first classification extension had a nonexistent test selector (no tests
executed), and the corrected 331-case run exposed one old get_form expectation
for a raw RuntimeError. Its replacement asserts the domain verification error
and the exact original cause; the integrated 774-case run includes this guard.
These attempts remain recorded separately rather than being counted as passes.

The first expanded conversion attempt accidentally included eight marked live
network cases in the restricted sandbox. It was interrupted after 1,397 passes
and five DNS-related failures (1,402 of 1,405 executed); it is not a passing or
complete run. A separate network-enabled rerun passes all eight marked cases.
The local conversion/PDBQT block passes all 1,397 selected cases with the eight
network cases explicitly deselected. No source workaround or changed download policy is used.

Public docstrings, Foundation diagnostics, three basic-tool tutorials, the
conversion Cookbook and course Module 14 explain unverified versus invalid
input. All code cells, outputs, execution counts, cell IDs and notebook metadata
remain unchanged. The complete incremental Sphinx HTML build has no warnings;
all fourteen fast release checks and Ruff pass. These bounded source checks do
not qualify a release, global platform matrix or installed Viewer pair.
