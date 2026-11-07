---
summary: Periodic fixed-state hydrogen addition calls a retired MIC helper signature.
issue: uibcdf/molsysmt#621
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [build, pbc]
guard: tests/build/add_missing_hydrogens/test_fixed_state.py::test_periodic_mic_pose_validation_preserves_physical_units
normative:
blocked_by: []
supersedes: []
---

# Periodic fixed-state H validation calls the old MIC signature

## What

With a periodic box, public fixed-state hydrogen addition raises
`TypeError: _minimum_image_vector() takes 2 positional arguments but 3 were given`
before validating a compact input pose. Three existing public tests reproduce:

```bash
python -m pytest --receptor=llm -n 12 tests/build/add_missing_hydrogens/test_fixed_state.py::test_observed_benzene_template_aromatic_only_bonds_gain_six_hydrogens tests/build/add_missing_hydrogens/test_fixed_state.py::test_periodic_compact_pose_box_and_frame_link_and_split_rejection tests/build/add_missing_hydrogens/test_fixed_state.py::test_real_est_retains_pose_and_five_cip_centers_through_h5msm
```

## How

`fixed_hydrogens._validate_pose` still computes an inverse and supplies
`(vector, box, inverse)` to the reconstruction helper. Phase-two correction
`3eb720444b97f77f9325acf52f55114ece0b5f9e` changed that private helper to use
the general Rust MIC primitive with `(vector, box)`. The caller was missed.
The source blame identifies the signature change and the unchanged consumer;
this is a regression of that correction, not a new Pandas or RDKit defect.

## Why

The existing supported periodic fixed-state preparation workflow fails, including
the deposited EST pose and aromatic-only graph controls. A compact ligand must
be accepted and a split ligand must receive the declared structural diagnostic
before publication, with source coordinates, chemical assignments and box intact.
Admit this correction under #334's included-workflow correctness rule without
another algorithm, capability, backend or progress-weight expansion.

## Measured evidence and limits

Found during #524's expanded public preparation receiving on exact unpacked
Pandas 3.1.0. That first 253-case attempt has 244 passes and nine failures:
six are a newly authored test's invalid MolSys.n_atoms lookup; the other three
are this independent TypeError. A subsequent default-Pandas selection has the
same three failures and six passing placement controls. Python 3.14.7, existing
Linux development prefix; no environment or backend is replaced.

The complete issue inventory immediately before this finding contains 552
issues and no equivalent MIC-signature report. #318 concerns an older
aromatic-only graph premise; #607's original periodic geometry issue is closed.
Preserve those records rather than reopening one to hide the new regression.

## Correction and acceptance

Update the consumer to the existing general MIC helper's supported signature
and remove the obsolete inverse calculation. Preserve finite/shape/box checks,
compact-versus-split semantics, units and source independence. No compatibility
shim that accepts an ignored third argument is needed for a private helper.

Qualify all three existing failures plus rotated/skewed cells, compact/split
poses and nondefault application units. Receive the broader fixed-state/native
placement and periodic profiles. Keep molecular method attribution unchanged;
this repair changes the call boundary, not the scientific placement formula.
Record original failures, exact source/backend identities, final native exits,
publication and issue closeout. Installed/platform/graphical gates stay separate.

## Final local receiving — 2026-11-06

Source `2804f7954fa14be72844bf6a30c37988f2dad71b` updates the missed caller and
removes its obsolete inverse calculation. Twelve new public periodic controls
fail on the original signature and pass after the correction. The complete
directed fixed-state/placement selection passes 60 cases. Combined preparation,
chemical-owner, PBC and vector receiving passes 965 cases on exact Pandas 3.1.0.
A separate public-floor parser/preparation/doctest profile passes 133 cases;
affected documentation passes 543, and registered scientific execution passes
97 cases across 64 nodes. Profiles overlap and have distinct evidence scopes.

The public docstring, fixed-state User Guide and course Module 12 now state
full row-vector compactness and physical-unit invariance. Module 12 retains all
code, outputs, cell IDs and metadata; only one Markdown cell changes. Original
RDKit/Ackredit method attribution is unchanged. Source preservation, metadata,
empty/reversed typed bond controls and explicit warning policies remain covered
by their owning tests rather than another validation implementation.

The [receiving receipt](../../../devtools/data/periodic_fixed_state_hydrogens_receiving_621_20261106.json)
binds all five source/test/documentation files, unchanged compiled backend,
commands, original failures, actual terminal exits and evidence limits.
The scientific certificate is correctly dirty-source development evidence,
not release-eligible. No environment or backend is replaced. Public delivery
and board closure follow independent source verification; #524 and all final
installed/platform/graphical gates remain due. Accepted plan progress stays 40%.

All fourteen fast source/metadata gates pass, as do the affected Ruff lint/format
and regenerated queue-index checks. No new remote workflow is dispatched. Four
pre-existing human autosummary edits remain outside this delivery.
