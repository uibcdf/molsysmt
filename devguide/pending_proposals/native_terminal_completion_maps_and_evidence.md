---
summary: Expose native terminal-completion maps and generation evidence
issue: uibcdf/molsysmt#558
status: active
opened: 2026-11-10
closed:
verification: inspected
area: [build, chemical-states, metadata]
guard:
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
the reporting interface is not implemented yet.

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
