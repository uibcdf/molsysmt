---
summary: Expand and validate formal-charge center recognition
issue: uibcdf/molsysmt#262
status: open
opened: 2026-09-30
closed:
verification: inspected
area: [api, attribute, tests, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Expand and validate formal-charge center recognition

**Reported:** 2026-09-30, following the maintainer's request to track the
limitations of the first experimental charge-center implementation.
**Status:** Open; implementation of these additional rules has not started.

## What

Extend and scientifically validate the selected-state formal-charge definition
of `physchem.get_charge_centers` for phosphate and sulfate groups, aromatic
charge delocalization, and explicitly supported alternative resonance
representations. Define complete participant membership and geometry-reference
atoms without changing the source state or inferring protonation silently.
Track this expansion separately from the first ionic detector in
`uibcdf/molsysmt#261`.

## How

Preserve the modular boundary: connectivity and reusable motif candidates
belong in `topology`; interpreting formal charges and selecting charged
participants belong in `physchem`. Element-specific conveniences can delegate
to these tools when they have a concrete standalone use. The ionic detector
must consume the general result rather than maintain a competing recognizer.

Before coding each rule, specify supported element/connectivity/bond-order
patterns, protonation states, net charge, recognition membership, and atoms
used for a subsequent geometric criterion. Cover both inorganic ions and
covalently substituted groups where explicitly supported. Do not assume that
all oxygen atoms have equivalent roles in every protonation state.

For aromatic systems, delimit the conjugated charged motif explicitly,
including supported fused or connected systems. Aromatic flags alone do not
justify merging every ring or every charged atom in a component. Record which
resonance representations are equivalent under the rule and which remain
unsupported; a changed charge-localization drawing must not change membership
when equivalence is claimed.

Retain typed arrays and offsets for whole and geometry memberships, original
atom indices, units, selected-state association, and evidence. Version changed
recognition rules. Decide and document the behavior for an unrecognized motif:
an atomic or generic formal-charge label must not imply that delocalization
was resolved. Any added coverage metadata needs compatible documentation and
tests before export.

## Why

The implementation delivered in `6b97be702` deliberately groups bounded
carboxyl and guanidine motifs and directly connected charged atoms. Its
docstring explicitly excludes phosphate, sulfate, and aromatic-ion grouping.
Unrecognized delocalized charge can therefore remain localized in an atomic
or generic cluster representation. That representation reports formal-charge
evidence but does not establish complete ionic participant chemistry.

Expanding the general recognizer will support interaction analysis and other
chemical workflows while avoiding family-specific rules. Scientific coverage
must be established before describing the tool as a general ionic classifier
or considering stabilization of its recognition contract.

## What is measured and what is assumed

**Inspected / Implemented:** the current public operation and its declared
limits are in [get_charge_centers.py](../../molsysmt/physchem/get_charge_centers.py).
The rule implementations are
[_charge_centers.py](../../molsysmt/physchem/_charge_centers.py) and
[_functional_group_candidates.py](../../molsysmt/topology/_functional_group_candidates.py).
Experimental status is owned by
[public_api_stability.json](../../devtools/data/public_api_stability.json).

**Existing contract evidence:**
[test_get_charge_centers.py](../../tests/physchem/test_get_charge_centers.py)
contains current-rule chemistry and selection controls. The original delivery
checkpoint and execution results are recorded in the
[ionic implementation proposal](implement_ionic_interactions_with_reusable_molecular_tools.md).
Those tests do not validate the new families proposed here.

**Proposed, not validated:** recognition rules and complete geometric
membership for the new families have not been selected or tested. No new
latency, RAM, coverage, or accuracy measurement is claimed in this record.

## What was refuted

Rejected shortcuts, based on the existing contract rather than comparative
benchmarks:

- Treating every formal-charge atom as a scientifically resolved ionic center
  hides the declared delocalization limitation.
- Combining all charges in a molecule would erase distinct local centers in
  zwitterions and is incompatible with their current tested behavior.
- Matching a residue name, assuming pH, or substituting partial charges changes
  the selected-state formal-charge definition.
- Agreement with a feature matcher or another implementation is not independent
  validation unless participant and charge definitions are first aligned.
- Broadening motif support alone is not sufficient to declare the entire
  experimental API stable.

## Scope and exclusions

This issue covers the formal-charge recognizer, its stated chemical coverage,
scientific evidence, provenance, and documentation. It does not implement
ionic geometry, pi-pi/cation-pi detection, force-field charge assignment,
partial-charge definitions, pH prediction, or energy calculation.

The first bounded ionic method can continue and close under
`uibcdf/molsysmt#261` while this expansion remains open. This issue does not add
a MolSysViewer initial-integration requirement or a new 1.0 release gate.
Release scheduling and any decision to stabilize the public API remain
separate decisions.

## Acceptance criteria

1. Document a bounded support table for phosphate, sulfate, and aromatic charged
   motifs, including supported protonation, substitution, and resonance forms;
   unresolved cases and fallback behavior remain explicit.
2. Add analytical or independently curated, versioned chemistry fixtures with
   expected whole membership, geometry membership, and net charge. State the
   reference rationale; do not generate expectations with the recognizer itself.
3. Test equivalent supported charge-localization/bond-order representations,
   changed chemical states, neutral analogues, nitro/N-oxide negative controls,
   zwitterions, multiple charged sites, and substituted or fused motifs within
   the declared support table. Retain the existing carboxylate/guanidinium guards.
4. Preserve deterministic typed sparse output, unitful charges, source indices,
   rule-version and selected-state evidence. Test nonconsecutive/repeated atom
   selections, empty results, and clear rejection of cut compound centers.
5. Verify native and supported conversion routes preserve the chemistry used by
   the recognizer, including a public H5MSM 0.5 source round trip. Missing
   prerequisites must not silently trigger another definition or parameterization.
6. Update the docstring/doctest, User Guide, Cookbook, and affected Four Paths
   modules. Register applicable scientific evidence with its exact claim scope.
   Experimental status remains until a separate stabilization decision.
7. Close with an addressable chemistry regression guard and maintained coverage
   documentation, then archive this record under the reporting protocol.

## Dependencies and risks

The existing charge-center tool provides the initial foundation; implementation
of the detector is not a blocking dependency. Related work is
`uibcdf/molsysmt#261`. Increasing recognized membership may change which atom
selections cut a center and which reference atoms a downstream detector uses;
rule versions and documentation must make that change visible.

Optional chemistry backends remain optional and lazily loaded. Their feature
definitions or sanitization must not invent unavailable source chemistry or
replace selected-state evidence. No new dependency or compiled kernel is
chosen by this proposal.
