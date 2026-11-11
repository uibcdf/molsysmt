---
summary: Expose native terminal-completion maps and generation evidence
issue: uibcdf/molsysmt#558
status: resolved
opened: 2026-11-10
closed: 2026-11-10
verification: measured
area: [build, chemical-states, metadata]
guard: tests/build/add_missing_terminal_cappings/test_generation_report.py
normative:
blocked_by: []
supersedes: []
---

# Native terminal-completion maps and evidence

## What

Add an optional detached result/report to native terminal completion, preserving
the existing default molecular-system return. DockingMT and PeptideMT need
provider-owned correspondence after insertions in group order, together with
operation-scoped evidence. This is useful pre-1.0 work, not an additional
release gate. This document records source inspection and the proposed scope;
the implemented interface and its receiving evidence are recorded below.

## How

At source `50af447ad94e7ac8e481e63e6b3837a0833d51ad`:

- `build.add_missing_terminal_cappings` runs heavy-atom repair, OXT insertion,
  N-bound H placement and optional ACE/NME group insertion. It returns no report
  and does not append a completion-history record.
- `build._native_placers.append_atoms_to_molsys` computes exact `old_to_new`
  positions after sorting. `rebuild_molsys_with_new_groups` also computes the
  correspondence. Both currently discard it at their return boundary.
- `carry_structures_through_atom_change` already implements intersection/strict
  attribute policies and diagnostics. Expansion transports chemical fields and
  stable membership, invalidates named analyses and can drop force-field atom
  parameters. Capture these actual dispositions instead of inventing values.
- `build.add_terminal_atoms` already returns a detached report and appends it
  through `_private.preparation_history.append_report`. That history is typed
  transport evidence in H5MSM, with indices in the original operation domain.
- `basic.compose_atom_maps` already composes forward/inverse maps and generated
  atoms without matching names, IDs or coordinates.

### Proposed implementation order

1. Extend the private expansion/rebuild boundary to optionally return its exact
   map and changes. Preserve existing callers and expose the same evidence to
   heavy-atom repair; terminal completion must compose its real substeps.
2. Add keyword-only `return_report=False` to terminal completion, with the
   existing hydrogen-addition result convention when true:
   `{'molecular_system': output, 'report': report}`. Add the existing
   `attribute_policy='intersection'` contract and pass it through every native
   expansion. Validate the new public inputs through ArgDigest and preserve
   SMonitor diagnostics. Non-native inputs still use the form-agnostic boundary.
3. Define `molsysmt.terminal_completion@1`: original and output counts, int64
   forward/inverse maps with `-1` for generated atoms, generated output indices,
   all introduced bonds in an explicitly declared output domain, selected source
   atoms/groups, examined structures/state, parameters, actual placement rules
   and template identities, units, MolSysMT producer version, field losses,
   invalidated analyses and unassessed outcomes. Retain stage-local maps and
   generation evidence, without copying coordinates into the report. Record
   placement provenance and applicable existing Ackredit references faithfully.
4. Extend the existing map normalizer for that report. Do not label general
   reconstruction as `terminal_attachment@1`: its current creation validator
   requires exactly one source parent per added atom, whereas a cap or repaired
   side chain may contain new-to-new bonds. Preserve these bonds and their
   actual stage axes instead of fabricating source parents.
5. Append one detached operation envelope to the returned ChemicalStates,
   including unchanged outcomes, while retaining earlier history verbatim.
   Preserve the operation-domain meaning through extraction and H5MSM. Keep
   unsupported reconstruction and unknown chemistry explicit.
6. Update the docstring, User Guide, preparation Cookbook and course together
   with the public regression tests below. A complete optional report initially
   covers `engine='MolSysMT'`. If another engine cannot provide exact
   correspondence, reject that optional report before running it; retain its
   existing default behavior rather than guess an identity map.

## Why

Group-ordered insertions change old atom positions. The source algorithm already
knows that mapping; consumers should not reconstruct it through labels or
geometric matching. Reported geometry generation does not assign a complete
chemical state, select a protonation hypothesis or certify preparation quality.

The issue supplies a 1HSG two-chain observation: 1,514 input atoms become 1,516,
with OXT at output indices 757 and 1,515. That is consumer evidence, not a new
local measurement. PeptideMT's subsequent 1YCR messages are read-only template
coverage observations, not terminal-completion acceptance.

## Acceptance criteria

- Verify a hand-specified multichain insertion map and compose it across heavy
  repair, OXT/H placement and cap insertion. Cover generated-to-generated bonds.
- Check observed coordinates through the returned map, under nm and nondefault
  length units, including multiple structures and nonconsecutive selections.
- Cover no-op/empty selections, partial and ambiguous assessment, unsupported
  attributes, strict-policy failures and unchanged source objects/files.
- Preserve old history, append a distinct completion record, detach returned
  arrays, and transport both history and maps through native persistence.
- Check default return/form compatibility, optional dependency behavior and
  public map composition. Scientific geometry quality remains separately
  assessed; atom counts alone cannot satisfy these guards.

## Scope and risks

No new reconstruction algorithm, terminal chemistry assignment, provider
dependency or format version is required by this proposal. Avoid coordinate
copies for evidence: the extra persistent data should be maps and bounded
per-stage metadata. Existing operation history must not be rewritten into a
current-axis map. Do not broaden PDBFixer claims without provider evidence.

After provider contract tests, request bounded receiving through the owning
DockingMT and PeptideMT issues. Their existing observations are not acceptance
of the future report. No new consumer request or implementation deadline is
created by this local plan.

## Implementation and receiving — 2026-11-10

**Contract-tested:** both public build tools accept keyword-only
`return_report=False`. The default molecular-system return is retained. The
optional dictionary contains **native MolSys**, including for another supported
input form, so the exact maps bind to its actual atom order. Terminal completion
also accepts the existing intersection/strict attribute policy and forwards it
through heavy repair, local atom insertion and cap-group reconstruction.
PDBFixer report/strict requests are rejected before executing that provider.
ArgDigest validates the new public flags; private helpers have no decorators.
The two intentional compatible signature extensions have explicit #558 entries
in the API registry.

The helper maps come directly from the actual insertion/rebuild ordering.
`terminal_completion@1` and `heavy_atom_completion@1` retain int64 forward/inverse
maps, generated output indices and IDs, output-domain introduced bonds, selected
source groups/atoms, all examined structures, the selected state identity,
parameters, canonical nm geometry, producing software, field losses and analysis
invalidation. Detailed steps retain local axes, actual template resource/hash,
anchors and placement criteria. New-to-new cap bonds have no fabricated source
parent. `compose_atom_maps` accepts these reports and rejects inconsistent
generation indices and output bond bounds. Maps require memory proportional to
atom/edge counts and the bounded number of steps; reports contain no coordinates.
No large-system performance benchmark is claimed.

Native terminal completion archives its operation without rewriting previous
history. A requested heavy-repair report archives its own actual substep; the
terminal report retains that nested evidence. Requested empty selections receive
identity maps and an unchanged record; the existing default empty-selection copy
is preserved. Typed reports survive default H5MSM 1.0 and extraction/reordering
with their original operation indices. No format version or chemical store was
added. Strict failures preserve the source; intersection warnings and actual
losses remain visible. Named analyses become unevaluated after expansion.

The fit uses the existing Rust quaternion alignment, not a new Kabsch/SVD
implementation. Its criterion is credited to
[Horn (1987)](https://doi.org/10.1364/JOSAA.4.000629) only when a fit executes.
References remain in reports without Ackredit; tracking uses the existing lazy
Ackredit/DepDigest boundary and respects host configuration. OXT reflection,
local sp3 H placement and planar cap rules have separate descriptive method
names. These estimated coordinates do not certify complete chemistry, sterics,
rotamers, environmental protonation or an energy minimum.

### Validation

The final source selection passes **227 cases**, zero failures/errors/skips,
including **23 new report cases and three module doctests**. It combines terminal
completion, heavy repair, terminal attachment, native placers, map composition
and scientific-attribution controls. Run:

```bash
python -m pytest --receptor=llm -n2 \
  tests/build/add_missing_terminal_cappings \
  tests/build/add_missing_heavy_atoms tests/build/add_terminal_atoms \
  tests/build/test_native_placers.py tests/basic/test_compose_atom_maps.py \
  tests/topology/test_correspondence_attribution.py \
  tests/interactions/test_scientific_attribution.py \
  --doctest-modules molsysmt/build/add_missing_terminal_cappings.py \
  molsysmt/build/add_missing_heavy_atoms.py molsysmt/basic/compose_atom_maps.py
```

Earlier failed receiving is retained locally. The first 221-case selection had
two failures from an older fixture installing a plain NumPy structure/state
array, which current H5MSM correctly rejects. The fixture now declares the same
explicit binding with native nullable Int64 storage. A public-setter experiment
invalidated its deliberately preexisting analysis; it was not retained. The
existing state/bond/coordinate/analysis assertions remain intact, and the final
full selection above passes. No storage validation was relaxed.

A final compatibility guard exposed an incidental restriction from internally
requesting a report on every no-op. It now protects the original unchanged
multistate default-copy route; explicit reporting still requires one selected
state. Its failed and passing attempts are retained. The final complete
selection above includes that guard.

The exact original 1HSG bytes, SHA-256
`d430675c358060808ef614002cfdcfcfa824714d89f1240adf5749d2ba60fed2`, are bundled as
a deterministic 39,388-byte gzip test fixture. **The old issue's raw-reader
precondition is no longer sufficient:** current declared-only input has no
stored N-CA-C backbone graph. Both chains are correctly reported unassessed,
with unchanged atoms/coordinates. After the separate, explicit
`infer_covalent_bonds(..., structure_indices=0)` operation, completion adds two
OXT at 757/1,515 to the 1,514-atom input. The returned exact map proves bitwise
preservation of observed coordinates and input immutability. B-factor/occupancy
losses are recorded. This is correspondence receiving, not a docking receptor
or biological preparation acceptance. The first probe's outdated-count
assertion failed for this missing-backbone reason; that observation is recorded
here rather than presented as an accepted control.

Environment: Linux/Python 3.14.7, public PyUnitWizard 0.29.2 and reference ABI3
SHA-256 `4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.
The complete run used two workers in a CPU-quota-200%, memory-high/max-3/4-GiB
user scope with no swap. Sampled host available memory stayed above 11 GiB
during combined receiving; sampled memory-pressure averages remained low
(zero at most checkpoints). No unrelated
process was stopped. This is source qualification, not installed release evidence.

Ruff, all 254 public docstrings, API registry/signature checks, optional-import
validation, the three modified notebook schemas and all 156 course notebooks'
structural contracts pass. Notebook edits change only Markdown, preserving
code, outputs and metadata. User Guide, Foundations, Cookbook and the course
describe report axes, history and limits. Client receiving remains with
DockingMT/PeptideMT through their existing owning issues; this provider delivery
does not claim their acceptance or introduce a new release gate.

Complete HTML receiving succeeds with typed `autosummary_generate=False` and
notebook execution disabled. Eight rendered User Guide/course/API pages were
inspected for the new contracts and both Cookbook anchors. Four existing RST
title-underline warnings remain. The first conservative HTML attempt reached
its 180-second scope limit and also exposed a string-valued CLI override;
that failed attempt is retained. The corrected two-worker build passed without
those override warnings and did not rewrite source RST files. The final API
wording was refreshed separately. The executable Cookbook block also passes.
