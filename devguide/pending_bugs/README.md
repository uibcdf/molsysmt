# Pending Bugs

This directory contains unresolved defect reports. Entries are evidence and work
queues, not normative specifications.

A report should contain a reproduction or concrete inspection evidence, affected
public behavior, severity, likely cause, and acceptance tests. When a defect is
fixed, add regression tests, update the relevant normative guide, and remove or
archive the report in the same change.

The presence of a report takes precedence over an unqualified historical claim
that the affected surface is fully verified.

A report is filed and closed under [reporting_protocol.md](../reporting_protocol.md):
every entry carries front matter, is tracked by an issue, and closes only when it
names the test that fails if the defect returns. The triage below is generated from
that front matter -- edit the entries, not this list.

## Current triage

<!-- generated: devguide_index -->

### Blocked (1)

- [`xdist_re_renders_catalog_warnings_on_the_controller.md`](xdist_re_renders_catalog_warnings_on_the_controller.md) — [#158](https://github.com/uibcdf/molsysmt/issues/158) — Under pytest-xdist the controller rebuilds catalog warnings as cls(rendered_text), so the template renders around its own output a second time. *(low, reproduced)*
  Blocked by pytest-dev/pytest-xdist#1372.

### Partially resolved (2)

- [`form_attributes_declared_without_getters.md`](form_attributes_declared_without_getters.md) — [#139](https://github.com/uibcdf/molsysmt/issues/139) — Forms declare attributes for which no getter or pipe can deliver a value. *(medium, measured)*
- [`sphinx_warning_baseline_and_api_reference_debt.md`](sphinx_warning_baseline_and_api_reference_debt.md) — [#144](https://github.com/uibcdf/molsysmt/issues/144) — The documentation build carries a large accepted warning population that hides new warnings. *(low, measured)*

<!-- /generated -->

Severity within a group still depends on the affected public workflow. Confirmed
bugs require a regression test; suspected bugs require a minimal reproduction
before implementation.

Documentation bugs have their own queue in [`docs/`](docs/README.md).

## Recently closed

`cross_repo_test_reads_a_removed_molsysviewer_attribute.md` was reported and archived on
2026-08-07. Two cross-repo tests read `MolSysView._message_history`, which MolSysViewer
replaced with a narrower `_shape_history` and a `scene_history` model. They already
recorded the edited molecular system handed to `apply_system_edit` and then ignored it,
so the fix was to assert on that instead: it is the contract this side of the boundary
owns. Renaming the attribute was deliberately not done — `_shape_history` is not the same
thing, so the tests would have passed asserting something else.


`public_functions_silently_ignore_unknown_keywords.md` was reported and archived on
2026-08-07. A typo in a keyword argument was silent in 22 of the 26 public callables and
uncatalogued in the other four: a one-letter slip in `structure_indices` returned all
5,000 structures of a trajectory instead of the three requested. The cause was a binding
step making a policy decision — ArgDigest discarded any keyword outside the signature
before the layer designed to judge it could see it — which also made ArgDigest more
permissive than Python itself. Fixed upstream in ArgDigest 0.10.0 by adding the axis the
defect was a symptom of, the function argument contract, and declared here by pointing
at MolSysMT's own attribute catalogue. Two claims in the original triage were wrong and
are corrected in the archived report: `contains` and `is_composed_of` implement
deliberate no-criterion branches. One further defect was found while reading them —
`get_label` declares `**kwargs` and never uses it.

`dihedral_quartets_with_blocks_raises_on_ragged_blocks.md` was reported and archived
on 2026-08-03. `get_dihedral_quartets(with_blocks=True)` pushed a ragged collection of
atom-index sets through `np.array` and raised on every real system. The blocks are now
returned as the list they always were. Three of T4 lysozyme's 161 phi quartets yield a
single block instead of two, and they are the prolines: the ring survives the cut.

`structural_attribute_resolution_ignores_the_structure_axis.md` was reported and
archived on 2026-08-03, together with
`iterator_without_explicit_attributes_fails_for_partial_forms.md`, which turned out
to be one of its symptoms. A composite molecular system had no structure axis of its
own: the same two files listed the other way round converted to one structure
instead of twenty, silently, and `get` returned structural series of contradictory
lengths for one system. The axis is now the largest structure count among the items
carrying structural data, only items spanning it may deliver a structural attribute,
and the existing last-matching-item tie-break applies among those. This completes on
the structure axis the consistency contract the library already enforced on the atom
axis. The precedence policy for *topological* attributes remains open, recorded
against decision 1 of `pending_proposals/attribute_centric_molecular_system_model.md`.

`docs_styler_zebra_striping_lost_with_myst_nb_1_4.md` was reported and archived on
2026-08-03. `msm.info()` returned a `Styler`, and a `Styler` emits no HTML class,
so once MyST-NB 1.4 dropped its class-agnostic pandas rule no theme rule could
reach the table. `info()` now tags it `dataframe` — the class pandas itself emits
from `DataFrame.to_html()` — which restores the striping, repairs a dark-mode
fallback that was painting the output as an inverted light box, and does so for
the whole suite from one line. Verified on a rebuilt page, not predicted.

Because `docs/conf.py:79` sets `nb_execution_mode = "off"`, 61 of the 62 notebooks
holding `msm.info()` output still store pre-fix HTML; re-executing them is
documentation work, and the archived report records the exact command and why the
staleness check in `docs/execute_notebooks.py` will not flag them.

`viewer_json_conversion_deep_copies_twice.md` was reported and archived on
2026-07-31. `MolSys → ViewerJSON` read two fresh, local, discarded intermediates
through the default deep-copying `to_dict()`; reading them with `copy=False`
takes the reported 5,000-structure case from 1.67 s to 0.32 s. The isolation the
copy appeared to provide is guarded by an explicit non-aliasing test, which stays
green with the copy restored — that is what shows it was redundant rather than
load-bearing.

`course_module_numbering_overlaps.md` was archived on 2026-07-29 after the two
remaining Common Core narrative references were replaced with stable semantic
links and a full Sphinx build completed. The 156-notebook structural contract
remains guarded by `devtools/scripts/validate_course.py`.

Four reports filed on 2026-07-24 during the Rust port described defects in the
Numba implementation. Segment D removed that implementation, and the Rust kernels
that replaced it implement the correct behaviour, so the reports were archived on
2026-07-28 with a resolution note under `../archive/resolved_bugs/`:
`dihedral_angles_broadcast_mismatch_pbc.md`, `sasa_is_orthogonal_typo.md`,
`wrap_to_mic_triclinic_not_minimum_image.md`, and
`principal_axes_eigenvector_sign_unspecified.md`.

A report is not closed merely because the implementation it describes was deleted:
each archived note records where the correct behaviour now lives and which test
guards it. Where no test does, that gap is tracked in
[`rust_migration_documentation_and_test_residue.md`](../archive/resolved_proposals/rust_migration_documentation_and_test_residue.md)
rather than left implicit.
