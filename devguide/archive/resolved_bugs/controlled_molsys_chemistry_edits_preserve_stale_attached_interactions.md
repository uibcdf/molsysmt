---
summary: Controlled MolSys chemistry edits preserve stale attached interactions
issue: uibcdf/molsysmt#287
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: high
verification: reproduced
area: [form, native, tests]
guard: tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py
normative:
blocked_by: []
supersedes: []
---

# Controlled MolSys chemistry edits preserve stale attached interactions

**Reported:** 2026-10-01, during the interaction lifecycle audit following
uibcdf/molsysmt#285.
**Status:** Resolved; controlled edits now remove obsolete observations and coverage.

## What

An attached ionic analysis remains evaluated after a public formal-charge edit
makes its observed interaction impossible. A Na/Cl pair at 0.3 nm, with charges
+1/-1 and complete declared connectivity, produces one ionic observation.
After `msm.set(molsys, element="atom", selection=[0], formal_charge=0)`, the
attached analysis still has one observation and coverage `[0]`; recalculating
with `msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm", pbc=False)`
returns zero. Both outcomes were executed on provider revision `887828fd9`.

## How

The native MolSys atom- and bond-state form helpers delegate directly to the
chemical authority via Topology. They never invalidate named interactions.
Replacing `MolSys.chemical_states` and editing the structure-to-state mapping
also publish their assignments without an interaction hook. These paths do
not change the atom/frame axis lengths, so attachment validation cannot detect
the mismatch. The geometry-only protection in #285 does not cover them.

## Why

Charge centers, aromatic participants and hydrogen-bond roles depend on chemical
assignments. Retaining evaluated coverage after changing those assignments
can present a chemically obsolete observation as current evidence to consumers.

## What is measured and what is assumed

**Reproduced:** neutralizing the Na atom leaves one stored occurrence but zero
fresh detections. The named analysis is attached through the public native
collection, and the charge edit uses the form-agnostic public setter.
**Inspected:** the related bond, domain-replacement and association paths lack
invalidation. Tests will qualify their exact behavior.
**Design decision:** the analysis metadata does not provide a complete
machine-readable chemical dependency graph. Chemical assignment changes must
therefore invalidate all evaluated frames in all named analyses. Frame-to-state
association edits can be limited to the selected frames. This is conservative
invalidation, not proof that every method depends on every edited attribute.

## What was refuted

- Matching axis lengths establishes index compatibility, not continued chemical
  validity of calculated observations.
- Geometry invalidation alone cannot catch a formal-charge change at fixed
  coordinates.
- Pruning only observations incident to edited atoms misses changed empty
  coverage and chemical effects propagated through compound participants.

## Scope and exclusions

This correction covers public `msm.set` on native MolSys atom-state and
scientific bond-state attributes, owner-level ChemicalStates replacement and
structure-to-state association assignment. Bond identifiers remain labels.
Empty atom/bond selections and label/time edits preserve analyses.

Raw array/DataFrame writes, separate Topology/ChemicalStates aliases, direct
Topology replacement and MolecularMechanics changes require explicit owner
invalidation. No observer protocol, dependency inference, automatic detector,
new result schema or incremental editor is introduced. The broader owner
lifecycle and editor remain tracked by uibcdf/molsysmt#251 and #252.

## Acceptance criteria

1. A public formal-charge edit removes obsolete occurrences and evaluated
   coverage in every named analysis; earlier result/query snapshots survive.
2. Atom aromaticity and scientific bond assignments use the same conservative
   invalidation; bond labels and empty selections preserve current results.
3. ChemicalStates replacement invalidates all frames without losing source maps,
   producer versions or detached provenance.
4. Structure-to-state assignment, including clearing it, invalidates only the
   selected frames; invalid state values fail before assignment.
5. Staging allocation failures preserve chemistry and analyses; uncertain
   failures after a delegate starts leave affected frames unevaluated.
6. Public H5MSM round trips retain the unevaluated/evaluated-empty distinction.
7. The affected User Guide, course, docstrings and normative developer contract
   describe supported mutation routes and explicit owner responsibilities.

## Dependencies and risks

The existing packed-array invalidation makes an independent snapshot. It is
linear in the retained payload, so this correction does not claim efficient
incremental updates. Public signatures and codecs must remain unchanged.

## Provenance

The reproduction ran on 2026-10-01 in the repository development Python
environment, with source commit `887828fd9`. Its exact reproducible scenarios
will be retained in the guard module, rather than a second untested script.

## Resolution — 2026-10-01

**Contract-tested:** the MolSys form atom-state and scientific bond-state
helpers use the same staged owner invalidation as geometry writes. Its private
name is now `_invalidating_interaction_frames`, reflecting the shared ownership
operation. Public signatures and the typed persistence schema are unchanged.
Nonempty chemical assignments invalidate every evaluated frame; bond IDs and
empty selections preserve results. ChemicalStates replacement validates the
shared domains before publishing a replacement with invalidated analyses.

Structure-to-state assignment stages a candidate nullable association before
invalidating selected frames and publishing it. Invalid state indices and
incompatible domain replacements preserve the previous owner state. Invalidation
of every named analysis is allocated before any delegated chemical write;
allocation failure preserves chemistry and results. After a delegate starts,
uncertain partial writes conservatively publish unevaluated frames.

The guard contains **29 regression cases**, covering actual ionic recalculation,
previous views, evaluated-empty coverage, seven atom assignments, eleven
scientific bond fields, label-only and empty selections, domain replacement,
explicit nonreference state editing, repeated/nonconsecutive frames, clearing
associations, invalid inputs, staged allocation failure and partial writes.
The unchanged geometry guard continues to protect #285's frame-local behavior.
A chemically invalidated system round-trips through public H5MSM conversion.

Verification commands and outcomes:

```bash
python -m pytest --receptor=llm \
  tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py \
  --doctest-modules molsysmt/basic/set.py molsysmt/form/molsysmt_MolSys/set.py
# 30 passed (29 regressions and one doctest), 6.63 s.

python -m pytest --receptor=llm \
  tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py \
  tests/form/molsysmt_MolSys/test_geometry_edit_interactions.py \
  tests/native/test_molsys.py tests/native/test_molsys_interactions.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/native/test_chemical_states.py tests/native/test_rich_bond_public_attributes.py \
  tests/form/molsysmt_MolSys/test_set_topological_attributes.py \
  tests/form/molsysmt_Topology/test_chemical_state_attributes.py \
  tests/basic/get/test_explicit_chemical_state.py tests/basic/test_set_contracts.py \
  tests/form/file_h5msm/test_chemical_states_v05_probe.py \
  tests/form/file_h5msm/test_associations_v05_probe.py
# 183 passed, 20.27 s; one expected legacy-format warning.

python -m pytest --receptor=llm tests/interactions \
  tests/form/file_h5msm/test_public_h5msm_v05.py \
  tests/form/molsysmt_InteractionsDict/test_roundtrip.py
# 552 passed, no skips, 123.02 s; 17 intentional tiny-budget memory warnings
# and five legacy-format warnings.

ruff check molsysmt tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py
python devtools/scripts/validate_dependencies.py
python devtools/scripts/validate_public_api_stability.py --base HEAD
python devtools/scripts/devguide_index.py
python devtools/scripts/validate_devguide.py
git diff --check
# All passed; no unauthorized signature drift.

make -C docs html SPHINXOPTS='-q -j 12 -w /tmp/molsysmt-287-sphinx.log'
# Exit 0; existing course heading, directive, cross-reference and toctree
# warnings remain. This does not establish a warning-free documentation build.
```

The six Python fences in the sparse-interaction Cookbook ran sequentially and
passed. Set Toolbox and Common Core Module 10 code cells and outputs were
verified unchanged while their lifecycle prose was updated. Foundations,
Cookbook, public/form docstrings and the normative interaction contract now
state the supported ownership rules. The development environment used Python
3.13.14, NumPy 2.4.6 and Pandas 2.3.3. The timings describe these local runs,
not portable performance guarantees or a complete release qualification.

**Limits retained:** invalidation copies packed arrays, and the correction
neither recalculates scientific observations nor adds incremental editing.
Direct Topology/ChemicalStates aliases, topology replacement, mechanics and raw
array/table writes remain explicit owner responsibilities, tracked by the
broader #251/#252 lifecycle work.
