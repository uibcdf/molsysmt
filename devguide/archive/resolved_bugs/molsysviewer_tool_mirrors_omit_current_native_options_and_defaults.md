---
summary: MolSysViewer tool mirrors omit current native options and defaults
issue: uibcdf/molsysmt#710
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [api]
guard: tests/molsysviewer_molsysmt/test_provider_admission_tools.py::test_exact_native_signature_digestion_help_and_namespace
normative:
blocked_by: []
supersedes: []
---

# MolSysViewer tool mirrors omit current native options and defaults

## What

Six existing exact-native-signature cases fail on `01c6266f6`. The addon H5MSM
writers retain 0.5 while their native providers default to 1.0. Heavy-atom repair
omits `return_report`; terminal completion omits both `attribute_policy` and
`return_report`. Run `python -m pytest --receptor=llm
 tests/molsysviewer_molsysmt/test_map_and_file_tools.py
 tests/molsysviewer_molsysmt/test_build_expansion_tools.py
 tests/molsysviewer_molsysmt/test_build_preparation_tools.py`.

## How

Explicit facade signatures in `molsysviewer_molsysmt/_files.py` and `_build.py`
have not followed provider changes. The documentation copier takes the new
native help, but the wrapper still supplies an older default or cannot accept
the new named input. The ordinary facade ArgDigest/SMonitor/native-delegation
boundary already exists and must be preserved.

## Why

The same user operation has different defaults, and clients cannot request the
native reconstruction reports through the documented mirror. This affects the
MolSysMT-owned addon consumed by MolSysViewer; no change in the sibling's code
or renderer is required. Current public providers already implement the options.

## Decision and scope

Align both writers with native default 1.0, keeping explicit 0.5/0.6 choices.
Forward the two repair tools' complete native inputs and return the original
system/report dictionary unchanged. Keep outputs independent, pending-primary
reads, validation, original units/provenance, no scene adoption and no invented
`update_view` argument. Update the guide's former explicit-0.5 description and
its content contract; it records the earlier source state, not the desired
exact-native mirror after the provider transition.

## What was refuted

Relaxing exact-signature guards would conceal API drift. Returning only the
system would lose the requested report. Automatically adopting a reported output
would change an unrelated scene/lifecycle contract. A new detector or provider
release is not needed.

## Acceptance criteria

Existing signature/help/digestion guards pass. Actual writer calls produce 1.0
by default and retain explicit older profiles, including mechanics preservation
or refusal. Report requests pass through once, preserve both maps and original
placement evidence, and leave the source/scene unchanged; invalid native options
still reject. Required addon inventory/preflight tests remain unchanged.

## Provenance

2026-11-11, local Linux/Python 3.14.7, MolSysMT `01c6266f6`, frozen MolSysViewer
`5164f13bb503625dbe65f3b657ab5260feadcb65`, PyUnitWizard 0.29.2,
ArgDigest 0.15.0, DepDigest 0.15.1, SMonitor 0.21.0 and Pytest Receptor 1.2.1.
The complete suite is failed with 49 failures/33,748 passes/16 skips; six
signature failures belong here. Source receiving is not installed qualification.

## Resolution — 2026-11-11

Implementation: `7d07ae00e`.

The two writer defaults now mirror native 1.0; explicit 0.5/0.6 remain
available within their native limits. Both preparation methods forward their
original native options, including reconstruction reports, without unpacking
or adopting the returned dictionary. Existing ArgDigest plans, SMonitor
signals and native engine/dependency/unit/attribution boundaries are retained;
no new dependency or duplicate scientific implementation is introduced.

The relevant 449-case receiving passes with no omissions. Actual report calls
run once under nm and pm policies, preserve the native dictionary identity,
source/output correspondence and retained coordinates, and leave source and
scene unchanged. Twelve actual writer cases exercise both facades across
default 1.0, explicit 1.0 and explicit 0.6 under two quantity policies, while
explicit 0.5 refusals remain guarded. A further overlapping 106-case cohort
receives updated provider signatures/help/doctests and documentation controls.
The primary parametrized guard covers both writers and both preparation
methods; the behavioral tests prevent signature-only conformity. The guide,
paired content contract and Core04 prose now describe the same behavior.

The [polishing receipt](../../../devtools/data/pre_1_0_polishing_receiving_334_20261111.json)
retains original failures, the first focused eight-failure attempt, input/native
identities, resource limits and documentation receiving. The original complete
suite remains failed until a new full corrected-source session succeeds. This
bounded closeout is not installed, graphical, platform or candidate acceptance.
